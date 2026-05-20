import sqlite3
import threading
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from config import AUTO_CONFIRM_SECONDS, HOLD_DURATION_SECONDS

DB_PATH = Path(__file__).resolve().parent / "seats.db"


class SeatStore:
    """
    Seat inventory backed by SQLite (one file = one source of truth).
    Works across threads and multiple server processes on the same machine.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._seat_locks: Dict[Tuple[str, str], threading.Lock] = {}
        self._meta = threading.Lock()
        self._conn = sqlite3.connect(
            str(DB_PATH),
            timeout=30.0,
            check_same_thread=False,
            isolation_level=None,
        )
        self._conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        with self._lock:
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS seats (
                    flight_id TEXT NOT NULL,
                    seat_no TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'AVAILABLE',
                    hold_id TEXT,
                    hold_user TEXT,
                    hold_expires REAL,
                    booking_id TEXT,
                    booked_user TEXT,
                    PRIMARY KEY (flight_id, seat_no)
                )
                """
            )
            count = self._conn.execute(
                "SELECT COUNT(*) AS c FROM seats"
            ).fetchone()["c"]
            if count == 0:
                seeds = [
                    ("F1", "A1"),
                    ("F1", "A2"),
                    ("F1", "A3"),
                    ("F1", "B1"),
                    ("F1", "B2"),
                    ("F2", "C1"),
                    ("F2", "C2"),
                    ("F2", "C3"),
                ]
                self._conn.executemany(
                    """
                    INSERT INTO seats (flight_id, seat_no, status)
                    VALUES (?, ?, 'AVAILABLE')
                    """,
                    seeds,
                )
            self._conn.commit()

    def _now(self) -> float:
        return time.monotonic()

    @staticmethod
    def _norm_seat(seat_no: str) -> str:
        return seat_no.strip().upper()

    def _seat_lock(self, flight_id: str, seat_no: str) -> threading.Lock:
        key = (flight_id, seat_no)
        with self._meta:
            if key not in self._seat_locks:
                self._seat_locks[key] = threading.Lock()
            return self._seat_locks[key]

    def _purge_expired_unlocked(self) -> None:
        now = self._now()
        self._conn.execute(
            """
            UPDATE seats
            SET status = 'AVAILABLE',
                hold_id = NULL,
                hold_user = NULL,
                hold_expires = NULL
            WHERE status = 'HOLD' AND hold_expires IS NOT NULL AND hold_expires <= ?
            """,
            (now,),
        )

    def check_availability(self, flight_id: str) -> List[Tuple[str, str]]:
        flight_id = flight_id.strip()
        with self._lock:
            self._conn.execute("BEGIN IMMEDIATE")
            self._purge_expired_unlocked()
            rows = self._conn.execute(
                """
                SELECT seat_no, status FROM seats
                WHERE flight_id = ?
                ORDER BY seat_no
                """,
                (flight_id,),
            ).fetchall()
            self._conn.commit()
            return [(r["seat_no"], r["status"]) for r in rows]

    def book_seat_complete(
        self, user_id: str, flight_id: str, seat_no: str
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Atomic booking for one seat: HOLD -> wait -> BOOKED.
        Only one client can run this for a given seat at a time.
        """
        seat_no = self._norm_seat(seat_no)
        user_id = user_id.strip()
        flight_id = flight_id.strip()
        seat_mutex = self._seat_lock(flight_id, seat_no)

        if not seat_mutex.acquire(blocking=False):
            return False, "SEAT_ON_HOLD", None

        try:
            hold_id = None
            with self._lock:
                self._conn.execute("BEGIN IMMEDIATE")
                self._purge_expired_unlocked()
                row = self._conn.execute(
                    """
                    SELECT status, hold_user FROM seats
                    WHERE flight_id = ? AND seat_no = ?
                    """,
                    (flight_id, seat_no),
                ).fetchone()

                if row is None:
                    self._conn.execute("ROLLBACK")
                    return False, "INVALID_SEAT", None

                status = row["status"]
                if status == "BOOKED":
                    self._conn.execute("ROLLBACK")
                    return False, "SEAT_ALREADY_BOOKED", None

                if status == "HOLD":
                    self._conn.execute("ROLLBACK")
                    return False, "SEAT_ON_HOLD", None

                hold_id = str(uuid.uuid4())
                expires = self._now() + HOLD_DURATION_SECONDS
                updated = self._conn.execute(
                    """
                    UPDATE seats
                    SET status = 'HOLD',
                        hold_id = ?,
                        hold_user = ?,
                        hold_expires = ?
                    WHERE flight_id = ? AND seat_no = ? AND status = 'AVAILABLE'
                    """,
                    (hold_id, user_id, expires, flight_id, seat_no),
                ).rowcount

                if updated != 1:
                    self._conn.execute("ROLLBACK")
                    return False, "SEAT_ON_HOLD", None

                self._conn.commit()

            time.sleep(AUTO_CONFIRM_SECONDS)

            with self._lock:
                self._conn.execute("BEGIN IMMEDIATE")
                row = self._conn.execute(
                    """
                    SELECT status, hold_id, hold_expires FROM seats
                    WHERE flight_id = ? AND seat_no = ?
                    """,
                    (flight_id, seat_no),
                ).fetchone()

                if (
                    row is None
                    or row["status"] != "HOLD"
                    or row["hold_id"] != hold_id
                    or self._now() >= row["hold_expires"]
                ):
                    self._conn.execute("ROLLBACK")
                    self._release_hold_in_tx(flight_id, seat_no, hold_id)
                    return False, "HOLD_EXPIRED", None

                booking_id = str(uuid.uuid4())
                updated = self._conn.execute(
                    """
                    UPDATE seats
                    SET status = 'BOOKED',
                        booking_id = ?,
                        booked_user = ?,
                        hold_id = NULL,
                        hold_user = NULL,
                        hold_expires = NULL
                    WHERE flight_id = ? AND seat_no = ?
                      AND status = 'HOLD' AND hold_id = ?
                    """,
                    (
                        booking_id,
                        user_id,
                        flight_id,
                        seat_no,
                        hold_id,
                    ),
                ).rowcount

                if updated != 1:
                    self._conn.execute("ROLLBACK")
                    return False, "SEAT_ALREADY_BOOKED", None

                self._conn.commit()
                return True, "CONFIRMED", booking_id

        finally:
            seat_mutex.release()

    def _release_hold_in_tx(
        self, flight_id: str, seat_no: str, hold_id: Optional[str]
    ) -> None:
        if hold_id:
            self._conn.execute(
                """
                UPDATE seats
                SET status = 'AVAILABLE',
                    hold_id = NULL,
                    hold_user = NULL,
                    hold_expires = NULL
                WHERE flight_id = ? AND seat_no = ?
                  AND status = 'HOLD' AND hold_id = ?
                """,
                (flight_id, seat_no, hold_id),
            )
        self._conn.commit()

    def cancel_reservation(
        self, flight_id: str, seat_no: str
    ) -> Tuple[bool, str]:
        seat_no = self._norm_seat(seat_no)
        flight_id = flight_id.strip()

        with self._lock:
            self._conn.execute("BEGIN IMMEDIATE")
            self._purge_expired_unlocked()
            row = self._conn.execute(
                """
                SELECT status FROM seats
                WHERE flight_id = ? AND seat_no = ?
                """,
                (flight_id, seat_no),
            ).fetchone()

            if row is None:
                self._conn.execute("ROLLBACK")
                return False, "INVALID_SEAT"

            status = row["status"]
            if status == "HOLD":
                self._conn.execute(
                    """
                    UPDATE seats
                    SET status = 'AVAILABLE',
                        hold_id = NULL,
                        hold_user = NULL,
                        hold_expires = NULL
                    WHERE flight_id = ? AND seat_no = ? AND status = 'HOLD'
                    """,
                    (flight_id, seat_no),
                )
                self._conn.commit()
                return True, "CANCELLED"

            if status != "BOOKED":
                self._conn.execute("ROLLBACK")
                return False, "NOT_BOOKED"

            self._conn.execute(
                """
                UPDATE seats
                SET status = 'AVAILABLE',
                    booking_id = NULL,
                    booked_user = NULL
                WHERE flight_id = ? AND seat_no = ? AND status = 'BOOKED'
                """,
                (flight_id, seat_no),
            )
            self._conn.commit()
            return True, "CANCELLED"

# booking_service/server.py — gRPC reservation backend (remote procedure calls)

import sys
from concurrent import futures
from pathlib import Path

import grpc

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import generated.booking_pb2 as pb2
import generated.booking_pb2_grpc as pb2_grpc
from booking_service.seat_store import DB_PATH, SeatStore
from config import AUTO_CONFIRM_SECONDS, HOLD_DURATION_SECONDS, RPC_BIND, RPC_PORT

store = SeatStore()


class ReservationService(pb2_grpc.ReservationServiceServicer):

    def CheckAvailability(self, request, context):
        seats = store.check_availability(request.flight_id.strip())
        return pb2.AvailabilityResponse(
            seats=[
                pb2.SeatInfo(seat_no=seat_no, status=status)
                for seat_no, status in seats
            ]
        )

    def BookSeat(self, request, context):
        ok, code, booking_id = store.book_seat_complete(
            request.user_id.strip(),
            request.flight_id.strip(),
            request.seat_no.strip().upper(),
        )
        if ok and booking_id:
            return pb2.BookingResponse(
                success=True,
                message="CONFIRMED",
                booking_id=booking_id,
                hold_id="",
                hold_seconds=0,
            )
        return pb2.BookingResponse(
            success=False,
            message=code,
            booking_id="",
            hold_id="",
            hold_seconds=0,
        )

    def CancelReservation(self, request, context):
        ok, code = store.cancel_reservation(
            request.flight_id.strip(),
            request.seat_no.strip().upper(),
        )
        return pb2.CancelResponse(
            success=ok,
            message=code,
        )


def _bind_port(server, port: int) -> str:
    candidates = [
        f"{RPC_BIND}:{port}",
        f"127.0.0.1:{port}",
        f"localhost:{port}",
    ]
    seen = set()
    for addr in candidates:
        if addr in seen:
            continue
        seen.add(addr)
        if server.add_insecure_port(addr) != 0:
            return addr
    return ""


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ReservationServiceServicer_to_server(
        ReservationService(), server
    )
    bound = _bind_port(server, RPC_PORT)
    if not bound:
        raise RuntimeError(
            f"Could not bind gRPC server on port {RPC_PORT}. "
            "Stop the other process first:\n"
            f'  netstat -ano | findstr ":{RPC_PORT}"\n'
            f"  taskkill /PID <pid> /F"
        )
    server.start()
    print(f"Reservation gRPC server on {bound}")
    print(f"Shared database: {DB_PATH}")
    print(
        f"Booking: hold then confirm after {AUTO_CONFIRM_SECONDS}s "
        f"(max hold {HOLD_DURATION_SECONDS}s)"
    )
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

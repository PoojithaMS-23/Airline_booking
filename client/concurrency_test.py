# Concurrent clients booking the same seat — only one should succeed.

import sys
import threading
import time
from pathlib import Path

import grpc

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import generated.booking_pb2 as pb2
import generated.booking_pb2_grpc as pb2_grpc
from config import AUTO_CONFIRM_SECONDS, RPC_ADDRESS

FLIGHT = "F1"
SEAT = "A1"
CLIENTS = 5
results = []
lock = threading.Lock()


def book_once(client_id: int):
    channel = grpc.insecure_channel(RPC_ADDRESS)
    stub = pb2_grpc.ReservationServiceStub(channel)
    try:
        response = stub.BookSeat(
            pb2.BookingRequest(
                user_id=f"user-{client_id}",
                flight_id=FLIGHT,
                seat_no=SEAT,
            ),
            timeout=30,
        )
        with lock:
            results.append(
                (client_id, response.success, response.message, response.booking_id)
            )
    except grpc.RpcError as err:
        with lock:
            results.append((client_id, False, err.code().name, ""))


def main():
    print(f"Spawning {CLIENTS} concurrent RPC clients -> {RPC_ADDRESS}")
    print(f"Each tries to book {FLIGHT} / {SEAT} (~{AUTO_CONFIRM_SECONDS}s per attempt)\n")

    threads = [
        threading.Thread(target=book_once, args=(i,))
        for i in range(CLIENTS)
    ]
    start = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.time() - start

    successes = [r for r in results if r[1]]
    failures = [r for r in results if not r[1]]

    for client_id, ok, msg, bid in sorted(results):
        print(f"  client-{client_id}: success={ok} message={msg} booking_id={bid or '-'}")

    print(f"\nSummary: {len(successes)} success, {len(failures)} rejected (expected: 1 success)")
    print(f"Elapsed: {elapsed:.1f}s")
    if len(successes) == 1 and len(failures) == CLIENTS - 1:
        print("PASS — seat consistency maintained under concurrent access.")
    else:
        print("UNEXPECTED — check server lock / seat store.")


if __name__ == "__main__":
    main()

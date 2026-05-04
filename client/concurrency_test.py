# client/concurrency_test.py

import grpc
import threading

import generated.booking_pb2 as pb2
import generated.booking_pb2_grpc as pb2_grpc


def book():
    # Each thread creates its own connection (best practice)
    channel = grpc.insecure_channel('localhost:50052')
    stub = pb2_grpc.BookingServiceStub(channel)

    response = stub.BookSeat(pb2.BookingRequest(
        user_id="U",
        flight_id="F1",
        seat_no="A1"
    ))

    print(response.status)


threads = []

# Simulate 2 users
for _ in range(2):
    t = threading.Thread(target=book)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
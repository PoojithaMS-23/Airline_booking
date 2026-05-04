# booking_service/server.py

import grpc
from concurrent import futures
import threading
import random
import uuid

import generated.booking_pb2 as pb2
import generated.booking_pb2_grpc as pb2_grpc

# Seat state storage
seats = {
    "A1": "AVAILABLE",
    "A2": "AVAILABLE",
    "A3": "AVAILABLE"
}

# booking_id → seat mapping
bookings = {}

# Lock for concurrency control
lock = threading.Lock()


class BookingService(pb2_grpc.BookingServiceServicer):

    def BookSeat(self, request, context):
        with lock:
            seat_no = request.seat_no

            # Check availability
            if seats.get(seat_no) != "AVAILABLE":
                return pb2.BookingResponse(
                    status="FAILED"
                )

            # Step 1: Temporarily reserve seat
            seats[seat_no] = "BOOKED"

            # Step 2: Simulate payment outcome
            if random.choice([True, False]):
                # ❌ Payment failed → rollback
                seats[seat_no] = "AVAILABLE"
                return pb2.BookingResponse(
                    status="PAYMENT FAILED"
                )

            # Step 3: Confirm booking
            booking_id = str(uuid.uuid4())
            bookings[booking_id] = seat_no

            return pb2.BookingResponse(
                status=f"SUCCESS | Booking ID: {booking_id}"
            )

    def CancelSeat(self, request, context):
        with lock:
            booking_id = request.booking_id

            # Check if booking exists
            if booking_id not in bookings:
                return pb2.CancelResponse(
                    status="INVALID BOOKING ID"
                )

            seat_no = bookings[booking_id]

            # Release seat
            seats[seat_no] = "AVAILABLE"

            # Remove booking
            del bookings[booking_id]

            return pb2.CancelResponse(
                status="CANCELLED SUCCESSFULLY"
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    pb2_grpc.add_BookingServiceServicer_to_server(
        BookingService(), server
    )

    server.add_insecure_port('[::]:50052')
    server.start()

    print("🚀 Booking Service running on port 50052...")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()
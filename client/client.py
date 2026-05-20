# # Standalone gRPC client — demonstrates remote invocation and marshalling.

# import sys
# from pathlib import Path

# import grpc

# ROOT = Path(__file__).resolve().parent.parent
# sys.path.insert(0, str(ROOT))

# import generated.booking_pb2 as pb2
# import generated.booking_pb2_grpc as pb2_grpc
# from config import RPC_ADDRESS


# def main():
#     channel = grpc.insecure_channel(RPC_ADDRESS)
#     stub = pb2_grpc.ReservationServiceStub(channel)

#     print(f"Connected to {RPC_ADDRESS}\n")

#     flight_id = "F1"
#     avail = stub.CheckAvailability(pb2.AvailabilityRequest(flight_id=flight_id))
#     print(f"Availability ({flight_id}):")
#     for s in avail.seats:
#         print(f"  {s.seat_no}: {s.status}")

#     book = stub.BookSeat(
#         pb2.BookingRequest(user_id="U1", flight_id=flight_id, seat_no="A1")
#     )
#     print(
#         f"\nBook A1: success={book.success} message={book.message} "
#         f"hold={book.hold_id} id={book.booking_id}"
#     )
#     import time
#     time.sleep(6)

#     avail2 = stub.CheckAvailability(pb2.AvailabilityRequest(flight_id=flight_id))
#     print(f"\nAfter booking:")
#     for s in avail2.seats:
#         print(f"  {s.seat_no}: {s.status}")

#     cancel = stub.CancelReservation(
#         pb2.CancelRequest(flight_id=flight_id, seat_no="A1")
#     )
#     print(f"\nCancel A1: success={cancel.success} message={cancel.message}")


# if __name__ == "__main__":
#     main()












import sys
from pathlib import Path

import grpc

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import generated.booking_pb2 as pb2
import generated.booking_pb2_grpc as pb2_grpc
from config import RPC_ADDRESS


def show_availability(stub, flight_id):
    avail = stub.CheckAvailability(
        pb2.AvailabilityRequest(flight_id=flight_id)
    )

    print(f"\nAvailability ({flight_id}):")

    for s in avail.seats:
        print(f"  {s.seat_no}: {s.status}")


def main():
    channel = grpc.insecure_channel(RPC_ADDRESS)

    stub = pb2_grpc.ReservationServiceStub(channel)

    print(f"Connected to {RPC_ADDRESS}")

    flight_id = "F1"

    while True:

        # Show seats
        show_availability(stub, flight_id)

        print("\nOptions:")
        print("1. Book Seat")
        print("2. Cancel Seat")
        print("3. Exit")

        choice = input("\nEnter choice: ")

        # BOOK SEAT
        if choice == "1":

            seat = input("Enter seat number: ")

            user_id = input("Enter user id: ")

            response = stub.BookSeat(
                pb2.BookingRequest(
                    user_id=user_id,
                    flight_id=flight_id,
                    seat_no=seat
                )
            )

            print("\nBooking Result:")
            print(f"Success : {response.success}")
            print(f"Message : {response.message}")

        # CANCEL SEAT
        elif choice == "2":

            seat = input("Enter seat number to cancel: ")

            response = stub.CancelReservation(
                pb2.CancelRequest(
                    flight_id=flight_id,
                    seat_no=seat
                )
            )

            print("\nCancellation Result:")
            print(f"Success : {response.success}")
            print(f"Message : {response.message}")

        # EXIT
        elif choice == "3":

            print("\nExiting client...")
            break

        else:
            print("\nInvalid choice")


if __name__ == "__main__":
    main()
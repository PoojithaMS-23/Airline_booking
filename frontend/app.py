from flask import Flask, render_template, request
import grpc

import generated.booking_pb2 as pb2
import generated.booking_pb2_grpc as pb2_grpc

app = Flask(__name__)


# 🔹 Check Availability
@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    seats = []

    if request.method == "POST":
        action = request.form.get("action")

        # Check seats
        if action == "check":
            channel = grpc.insecure_channel('localhost:50051')
            stub = pb2_grpc.FlightServiceStub(channel)
            res = stub.CheckAvailability(pb2.FlightRequest(flight_id="F1"))
            seats = res.available_seats

        # Book seat
        elif action == "book":
            seat = request.form.get("seat")
            channel = grpc.insecure_channel('localhost:50052')
            stub = pb2_grpc.BookingServiceStub(channel)

            res = stub.BookSeat(pb2.BookingRequest(
                user_id="U1",
                flight_id="F1",
                seat_no=seat
            ))

            message = res.status

        # Cancel booking
        elif action == "cancel":
            booking_id = request.form.get("booking_id")
            channel = grpc.insecure_channel('localhost:50052')
            stub = pb2_grpc.BookingServiceStub(channel)

            res = stub.CancelSeat(pb2.CancelRequest(
                booking_id=booking_id
            ))

            message = res.status

    return render_template("index.html", seats=seats, message=message)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
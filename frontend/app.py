# Web client gateway — HTTP from browsers, remote gRPC to the reservation backend.

import sys
from pathlib import Path

import grpc
from flask import Flask, jsonify, render_template, request

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import generated.booking_pb2 as pb2
import generated.booking_pb2_grpc as pb2_grpc
from config import RPC_ADDRESS, WEB_HOST, WEB_PORT

app = Flask(__name__)


def _stub():
    channel = grpc.insecure_channel(RPC_ADDRESS)
    return pb2_grpc.ReservationServiceStub(channel)


def _fetch_seats(stub, flight_id):
    res = stub.CheckAvailability(pb2.AvailabilityRequest(flight_id=flight_id))
    return [(s.seat_no, s.status) for s in res.seats]


def _grpc_error_message(exc: grpc.RpcError) -> str:
    if exc.code() == grpc.StatusCode.UNAVAILABLE:
        return (
            f"Reservation server is not running on {RPC_ADDRESS}. "
            "Open a separate terminal and run: python booking_service/server.py"
        )
    return f"Server error: {exc.details()}"


@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    seats = []
    flight_id = request.form.get("flight_id", "F1") or request.args.get("flight_id", "F1")
    user_id = request.form.get("user_id", "U1") or request.args.get("user_id", "U1")

    if request.method == "POST":
        action = request.form.get("action")
        stub = _stub()

        try:
            if action == "check":
                flight_id = request.form.get("flight_id", "F1")
                seats = _fetch_seats(stub, flight_id)

            elif action == "book":
                seat = request.form.get("seat", "").strip().upper()
                flight_id = request.form.get("flight_id", "F1")
                user_id = request.form.get("user_id", "U1")
                res = stub.BookSeat(
                    pb2.BookingRequest(
                        user_id=user_id,
                        flight_id=flight_id,
                        seat_no=seat,
                    ),
                    timeout=30,
                )
                seats = _fetch_seats(stub, flight_id)
                if res.success and res.message == "CONFIRMED":
                    message = f"Seat {seat} booked successfully"
                elif res.message == "SEAT_ON_HOLD":
                    message = (
                        f"Seat {seat} is on hold - another user is booking it."
                    )
                elif res.message == "BOOKING_IN_PROGRESS":
                    message = (
                        f"Seat {seat} booking already in progress, please wait."
                    )
                elif res.message == "SEAT_ALREADY_BOOKED":
                    message = f"Seat {seat} is already booked."
                else:
                    message = f"Failed - {res.message}"

            elif action == "cancel":
                seat = request.form.get("seat", "").strip().upper()
                flight_id = request.form.get("flight_id", "F1")
                res = stub.CancelReservation(
                    pb2.CancelRequest(flight_id=flight_id, seat_no=seat)
                )
                seats = _fetch_seats(stub, flight_id)
                if res.success:
                    message = f"Seat {seat} cancelled"
                else:
                    message = f"Failed - {res.message}"

        except grpc.RpcError as exc:
            message = _grpc_error_message(exc)

    return render_template(
        "index.html",
        seats=seats,
        message=message,
        flight_id=flight_id,
        user_id=user_id,
        auto_refresh=bool(seats),
    )


@app.route("/api/flights/<flight_id>/seats", methods=["GET"])
def api_availability(flight_id):
    try:
        stub = _stub()
        res = stub.CheckAvailability(pb2.AvailabilityRequest(flight_id=flight_id))
        return jsonify(
            {
                "flight_id": flight_id,
                "seats": [
                    {"seat_no": s.seat_no, "status": s.status} for s in res.seats
                ],
            }
        )
    except grpc.RpcError as exc:
        return jsonify({"error": _grpc_error_message(exc)}), 503


@app.route("/api/book", methods=["POST"])
def api_book():
    data = request.get_json(force=True)
    stub = _stub()
    res = stub.BookSeat(
        pb2.BookingRequest(
            user_id=data.get("user_id", "guest"),
            flight_id=data.get("flight_id", "F1"),
            seat_no=str(data.get("seat_no", "")).upper(),
        )
    )
    status = 200 if res.success else 409
    return jsonify(
        {
            "success": res.success,
            "message": res.message,
            "booking_id": res.booking_id,
            "hold_id": res.hold_id,
            "hold_seconds": res.hold_seconds,
        }
    ), status


@app.route("/api/cancel", methods=["POST"])
def api_cancel():
    data = request.get_json(force=True)
    stub = _stub()
    res = stub.CancelReservation(
        pb2.CancelRequest(
            flight_id=data.get("flight_id", "F1"),
            seat_no=str(data.get("seat_no", "")).upper(),
        )
    )
    status = 200 if res.success else 404
    return jsonify({"success": res.success, "message": res.message}), status


if __name__ == "__main__":
    print(f"Web gateway http://{WEB_HOST}:{WEB_PORT} -> gRPC {RPC_ADDRESS}")
    print("Start the backend FIRST in another terminal:")
    print("  python booking_service/server.py")
    app.run(host=WEB_HOST, port=WEB_PORT, debug=True, use_reloader=False)

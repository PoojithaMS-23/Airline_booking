# client/client.py
import grpc
import generated.booking_pb2 as pb2
import generated.booking_pb2_grpc as pb2_grpc

channel = grpc.insecure_channel('localhost:50052')
stub = pb2_grpc.BookingServiceStub(channel)

response = stub.BookSeat(pb2.BookingRequest(
    user_id="U1",
    flight_id="F1",
    seat_no="A1"
))

print(response.status)
channel = grpc.insecure_channel('localhost:50051')
stub = pb2_grpc.FlightServiceStub(channel)

response = stub.CheckAvailability(pb2.FlightRequest(flight_id="F1"))

print("Available Seats:", response.available_seats)
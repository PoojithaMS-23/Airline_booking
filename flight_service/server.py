# flight_service/server.py
import os
import sys
import grpc
from concurrent import futures

# Ensure the project root is on sys.path so sibling packages like generated can be imported
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import generated.booking_pb2 as pb2
import generated.booking_pb2_grpc as pb2_grpc

seats = {"A1": "AVAILABLE", "A2": "AVAILABLE"}

class FlightService(pb2_grpc.FlightServiceServicer):
    def CheckAvailability(self, request, context):
        available = [s for s, v in seats.items() if v == "AVAILABLE"]
        return pb2.AvailabilityResponse(available_seats=available)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_FlightServiceServicer_to_server(FlightService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Flight Service running...")
    server.wait_for_termination()

serve()
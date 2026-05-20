# DEPRECATED: Use booking_service/server.py (unified ReservationService).
# This split service is kept only for reference; it is not used by the web client.

import grpc
from concurrent import futures

import generated.booking_pb2 as pb2
import generated.booking_pb2_grpc as pb2_grpc

if __name__ == "__main__":
    print(
        "flight_service is deprecated. Run: python booking_service/server.py"
    )

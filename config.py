import os

RPC_HOST = os.environ.get("RPC_HOST", "localhost")
RPC_PORT = int(os.environ.get("RPC_PORT", "50052"))
RPC_ADDRESS = f"{RPC_HOST}:{RPC_PORT}"

# Bind address for the gRPC server. Use 0.0.0.0 on Windows ([::] often fails).
RPC_BIND = os.environ.get("RPC_BIND", "0.0.0.0")

WEB_HOST = os.environ.get("WEB_HOST", "0.0.0.0")
WEB_PORT = int(os.environ.get("WEB_PORT", "8000"))

# Seat hold: temporary lock while a user is booking
HOLD_DURATION_SECONDS = int(os.environ.get("HOLD_DURATION_SECONDS", "30"))
# Simulate payment / checkout, then auto-confirm the hold
AUTO_CONFIRM_SECONDS = int(os.environ.get("AUTO_CONFIRM_SECONDS", "5"))

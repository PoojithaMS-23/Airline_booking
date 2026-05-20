# Regenerate Python gRPC stubs from proto/booking.proto
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $root
python -m grpc_tools.protoc `
  -I./proto `
  --python_out=./generated `
  --grpc_python_out=./generated `
  proto/booking.proto

# Fix import so stubs work as the `generated` package
$grpcFile = Join-Path $root "generated\booking_pb2_grpc.py"
(Get-Content $grpcFile -Raw) `
  -replace 'import booking_pb2 as booking__pb2', 'from generated import booking_pb2 as booking__pb2' `
  | Set-Content $grpcFile -NoNewline

Write-Host "Generated: generated/booking_pb2.py, generated/booking_pb2_grpc.py"

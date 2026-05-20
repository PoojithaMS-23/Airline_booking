# Reset all seats to AVAILABLE (run when testing from scratch)
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$db = Join-Path $root "booking_service\seats.db"

if (Test-Path $db) {
    Remove-Item $db -Force
    Write-Host "Removed $db - restart booking_service/server.py to re-seed."
} else {
    Write-Host "No database file yet."
}

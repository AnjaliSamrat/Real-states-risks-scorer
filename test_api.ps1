Write-Host ""
Write-Host "========================================"  -ForegroundColor Cyan
Write-Host "  QUICK API TEST" -ForegroundColor Cyan
Write-Host "========================================"  -ForegroundColor Cyan

$passed = 0
$failed = 0

Write-Host ""
Write-Host "[TEST 1] Health Check" -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health"
    if ($health.status -eq "healthy") {
        Write-Host "  PASS - Backend is healthy" -ForegroundColor Green
        $passed++
    }
} catch {
    Write-Host "  FAIL" -ForegroundColor Red
    $failed++
}

Write-Host ""
Write-Host "[TEST 2] Properties Search" -ForegroundColor Yellow
try {
    $props = Invoke-RestMethod -Uri "http://localhost:8000/api/properties/search?address=test"
    Write-Host "  PASS - Found $($props.Count) properties" -ForegroundColor Green
    $passed++
} catch {
    Write-Host "  FAIL" -ForegroundColor Red
    $failed++
}

Write-Host ""
Write-Host "[TEST 3] Weather Data" -ForegroundColor Yellow
try {
    $weather = Invoke-RestMethod -Uri "http://localhost:8000/api/weather/37.7749/-122.4194"
    Write-Host "  PASS - Weather: $($weather.temperature)F, $($weather.description)" -ForegroundColor Green
    $passed++
} catch {
    Write-Host "  FAIL" -ForegroundColor Red
    $failed++
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Passed: $passed | Failed: $failed" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan

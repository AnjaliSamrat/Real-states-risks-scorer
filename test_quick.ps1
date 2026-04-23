# Quick API Test Script
# Tests all currently implemented endpoints

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  QUICK API TEST" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$passed = 0
$failed = 0

# Test 1: Health Check
Write-Host ""
Write-Host "[TEST 1] Health Check" -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health"
    if ($health.status -eq "healthy") {
        Write-Host "  ✓ PASS - Backend is healthy" -ForegroundColor Green
        $passed++
    }
} catch {
    Write-Host "  ✗ FAIL - $($_.Exception.Message)" -ForegroundColor Red
    $failed++
}

# Test 2: Root Endpoint
Write-Host ""
Write-Host "[TEST 2] Root Endpoint" -ForegroundColor Yellow
try {
    $root = Invoke-RestMethod -Uri "http://localhost:8000/"
    Write-Host "  ✓ PASS - $($root.message)" -ForegroundColor Green
    $passed++
} catch {
    Write-Host "  ✗ FAIL - $($_.Exception.Message)" -ForegroundColor Red
    $failed++
}

# Test 3: Properties Search
Write-Host ""
Write-Host "[TEST 3] Properties Search" -ForegroundColor Yellow
try {
    $props = Invoke-RestMethod -Uri "http://localhost:8000/api/properties/search?address=test"
    if ($props.Count -gt 0) {
        Write-Host "  ✓ PASS - Found $($props.Count) properties" -ForegroundColor Green
        Write-Host "    Address: $($props[0].address)" -ForegroundColor Gray
        $passed++
    }
} catch {
    Write-Host "  ✗ FAIL - $($_.Exception.Message)" -ForegroundColor Red
    $failed++
}

# Test 4: Get Specific Property
Write-Host ""
Write-Host "[TEST 4] Get Property Details" -ForegroundColor Yellow
try {
    $prop = Invoke-RestMethod -Uri "http://localhost:8000/api/properties/prop_001"
    Write-Host "  ✓ PASS - Retrieved property $($prop.id)" -ForegroundColor Green
    Write-Host "    Location: $($prop.latitude), $($prop.longitude)" -ForegroundColor Gray
    $passed++
} catch {
    Write-Host "  ✗ FAIL - $($_.Exception.Message)" -ForegroundColor Red
    $failed++
}

# Test 5: Weather Endpoint
Write-Host ""
Write-Host "[TEST 5] Weather Data" -ForegroundColor Yellow
try {
    $weather = Invoke-RestMethod -Uri "http://localhost:8000/api/weather/37.7749/-122.4194"
    Write-Host "  ✓ PASS - Weather: $($weather.temperature)°F, $($weather.description)" -ForegroundColor Green
    $passed++
} catch {
    Write-Host "  ✗ FAIL - $($_.Exception.Message)" -ForegroundColor Red
    $failed++
}

# Test 6: Frontend Server
Write-Host ""
Write-Host "[TEST 6] Frontend Server" -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri "http://localhost:5173" -UseBasicParsing -TimeoutSec 5 | Out-Null
    Write-Host "  ✓ PASS - Frontend is running" -ForegroundColor Green
    $passed++
} catch {
    Write-Host "  ✗ FAIL - Frontend not responding" -ForegroundColor Red
    $failed++
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
$total = $passed + $failed
$rate = if ($total -gt 0) { [math]::Round(($passed / $total) * 100, 1) } else { 0 }

Write-Host "Total Tests: $total" -ForegroundColor White
Write-Host "Passed: $passed" -ForegroundColor Green
Write-Host "Failed: $failed" -ForegroundColor Red
Write-Host "Success Rate: $rate%" -ForegroundColor $(if ($rate -ge 80) { "Green" } else { "Yellow" })

if ($failed -eq 0) {
    Write-Host ""
Write-Host "✓ ALL TESTS PASSED!" -ForegroundColor Green
} else {
    Write-Host ""
Write-Host "⚠ Some tests failed" -ForegroundColor Yellow
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

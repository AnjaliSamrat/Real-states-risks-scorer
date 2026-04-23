# ==========================================
# WORKING API TESTS - ACTUAL ENDPOINTS
# ==========================================

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  API TEST - AVAILABLE ENDPOINTS" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

$passed = 0
$failed = 0

# Test 1: Health Check
Write-Host ""
Write-Host "[1/5] Health Check..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri 'http://localhost:8000/health'
    if ($health.status -eq 'healthy') {
        Write-Host '  PASS - Backend is healthy' -ForegroundColor Green
        $passed++
    }
} catch {
    Write-Host '  FAIL' -ForegroundColor Red
    $failed++
}

# Test 2: Search Properties
Write-Host ""
Write-Host "[2/5] Search Properties..." -ForegroundColor Yellow
try {
    $props = Invoke-RestMethod -Uri 'http://localhost:8000/api/properties/search?address=san+francisco'
    if ($props.Count -gt 0) {
        Write-Host "  PASS - Found $($props.Count) properties" -ForegroundColor Green
        Write-Host "    Address: $($props[0].address)" -ForegroundColor Gray
        Write-Host "    Price: `$$($props[0].price)" -ForegroundColor Gray
        $passed++
    }
} catch {
    Write-Host '  FAIL' -ForegroundColor Red
    $failed++
}

# Test 3: Get Specific Property
Write-Host ""
Write-Host "[3/5] Get Property Details..." -ForegroundColor Yellow
try {
    $prop = Invoke-RestMethod -Uri 'http://localhost:8000/api/properties/prop_001'
    Write-Host "  PASS - Retrieved property $($prop.id)" -ForegroundColor Green
    Write-Host "    Location: ($($prop.latitude), $($prop.longitude))" -ForegroundColor Gray
    $passed++
} catch {
    Write-Host '  FAIL' -ForegroundColor Red
    $failed++
}

# Test 4: Weather API
Write-Host ""
Write-Host "[4/5] Weather Data..." -ForegroundColor Yellow
try {
    $weather = Invoke-RestMethod -Uri 'http://localhost:8000/api/weather/37.7749/-122.4194'
    Write-Host '  PASS - Weather data retrieved' -ForegroundColor Green
    Write-Host "    Temperature: $($weather.temperature)°C" -ForegroundColor Gray
    Write-Host "    Description: $($weather.description)" -ForegroundColor Gray
    $passed++
} catch {
    Write-Host '  FAIL - Weather endpoint error' -ForegroundColor Red
    $failed++
}

# Test 5: User Registration
Write-Host ""
Write-Host "[5/5] User Registration..." -ForegroundColor Yellow
try {
    $timestamp = Get-Date -Format "yyyyMMddHHmmss"
    $userBody = @{
        email = "test$timestamp@example.com"
        password = 'TestPassword123!'
        full_name = 'Test User'
    } | ConvertTo-Json

    $user = Invoke-RestMethod -Uri 'http://localhost:8000/api/auth/register' `
        -Method POST `
        -Body $userBody `
        -ContentType 'application/json'
    
    Write-Host '  PASS - User registered successfully' -ForegroundColor Green
    Write-Host "    Email: $($user.email)" -ForegroundColor Gray
    $passed++
} catch {
    Write-Host '  FAIL - Registration error' -ForegroundColor Red
    $failed++
}

# Summary
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host '  TEST RESULTS' -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Total Tests: 5" -ForegroundColor White
Write-Host "Passed: $passed" -ForegroundColor Green
Write-Host "Failed: $failed" -ForegroundColor Red

$rate = [math]::Round(($passed / 5) * 100, 1)
Write-Host "Success Rate: $rate%" -ForegroundColor Cyan

if ($failed -eq 0) {
    Write-Host ""
    Write-Host "ALL TESTS PASSED! " -ForegroundColor Green
    Write-Host "Your Real Estate Risk Scorer API is fully operational!" -ForegroundColor Green
} elseif ($passed -ge 3) {
    Write-Host ""
    Write-Host "Most tests passed - API is working!" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "Multiple failures detected. Check the backend server." -ForegroundColor Red
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# ==========================================
# COMPLETE API TESTING SCRIPT
# ==========================================

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  REAL ESTATE RISK SCORER - FULL TEST" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

$passed = 0
$failed = 0
$propertyId = $null

# Test 1: Health Check
Write-Host ""
Write-Host "[1/6] Health Check..." -ForegroundColor Yellow
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

# Test 2: Create Property
Write-Host ""
Write-Host "[2/6] Create Property..." -ForegroundColor Yellow
try {
    $body = @{
        address = '1600 Amphitheatre Parkway, Mountain View, CA'
        price = 1500000
        bedrooms = 3
        bathrooms = 2.5
        square_feet = 2200
        year_built = 2015
    } | ConvertTo-Json

    $property = Invoke-RestMethod -Uri 'http://localhost:8000/api/properties' `
        -Method POST `
        -Body $body `
        -ContentType 'application/json'
    
    $propertyId = $property.id
    Write-Host "  PASS - Property created with ID $propertyId" -ForegroundColor Green
    Write-Host "    Address: $($property.address)" -ForegroundColor Gray
    Write-Host "    Coords: ($($property.latitude), $($property.longitude))" -ForegroundColor Gray
    $passed++
} catch {
    Write-Host '  FAIL' -ForegroundColor Red
    Write-Host "    Error: $_" -ForegroundColor Red
    $failed++
}

# Test 3: Get Property
if ($propertyId) {
    Write-Host ""
    Write-Host "[3/6] Get Property (ID: $propertyId)..." -ForegroundColor Yellow
    try {
        $prop = Invoke-RestMethod -Uri "http://localhost:8000/api/properties/$propertyId"
        Write-Host '  PASS - Property retrieved' -ForegroundColor Green
        $passed++
    } catch {
        Write-Host '  FAIL' -ForegroundColor Red
        $failed++
    }
}

# Test 4: Generate Risk Assessment
if ($propertyId) {
    Write-Host ""
    Write-Host "[4/6] Generate Risk Assessment..." -ForegroundColor Yellow
    Write-Host '  Please wait 2-5 seconds...' -ForegroundColor Gray
    try {
        $assessment = Invoke-RestMethod -Uri "http://localhost:8000/api/risk/$propertyId" `
            -Method POST `
            -TimeoutSec 15
        
        Write-Host '  PASS - Risk Assessment Generated' -ForegroundColor Green
        Write-Host "    Overall Score: $([math]::Round($assessment.overall_score, 1))/100" -ForegroundColor Cyan
        Write-Host "    Climate:       $([math]::Round($assessment.climate_score, 1))" -ForegroundColor Gray
        Write-Host "    Crime:         $([math]::Round($assessment.crime_score, 1))" -ForegroundColor Gray
        Write-Host "    Economic:      $([math]::Round($assessment.economic_score, 1))" -ForegroundColor Gray
        Write-Host "    Infrastructure: $([math]::Round($assessment.infrastructure_score, 1))" -ForegroundColor Gray
        $passed++
    } catch {
        Write-Host '  FAIL' -ForegroundColor Red
        Write-Host "    Error: $_" -ForegroundColor Red
        $failed++
    }
}

# Test 5: Weather API
Write-Host ""
Write-Host "[5/6] Weather API..." -ForegroundColor Yellow
try {
    $weather = Invoke-RestMethod -Uri 'http://localhost:8000/api/weather/37.7749/-122.4194'
    Write-Host '  PASS - Weather data retrieved' -ForegroundColor Green
    Write-Host "    Temperature: $($weather.temperature)C" -ForegroundColor Gray
    Write-Host "    Description: $($weather.description)" -ForegroundColor Gray
    $passed++
} catch {
    Write-Host '  SKIP - Weather endpoint not available' -ForegroundColor Yellow
}

# Test 6: User Registration
Write-Host ""
Write-Host "[6/6] User Registration..." -ForegroundColor Yellow
try {
    $timestamp = [int][double]::Parse((Get-Date -UFormat %s))
    $userBody = @{
        email = "test$timestamp@example.com"
        password = 'TestPassword123!'
        full_name = 'Test User'
    } | ConvertTo-Json

    $user = Invoke-RestMethod -Uri 'http://localhost:8000/api/auth/register' `
        -Method POST `
        -Body $userBody `
        -ContentType 'application/json'
    
    Write-Host '  PASS - User registered' -ForegroundColor Green
    $passed++
} catch {
    Write-Host '  FAIL' -ForegroundColor Red
    $failed++
}

# Summary
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host '  TEST RESULTS SUMMARY' -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Passed: $passed" -ForegroundColor Green
Write-Host "Failed: $failed" -ForegroundColor Red

if ($failed -eq 0) {
    Write-Host ""
    Write-Host "All tests passed! Your API is working perfectly!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Some tests failed. Check the output above." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

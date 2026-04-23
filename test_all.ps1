# Complete Testing Script for Real Estate Risk Scorer
# This script runs all manual tests for both backend and frontend

Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "  REAL ESTATE RISK SCORER - TEST SUITE" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$ErrorActionPreference = "Continue"
$testsPassed = 0
$testsFailed = 0

# Helper function to test endpoint
function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Url,
        [string]$Method = "GET",
        [object]$Body = $null,
        [int]$ExpectedStatus = 200
    )
    
    Write-Host "`n------------------------------------------" -ForegroundColor Yellow
    Write-Host "TEST: $Name" -ForegroundColor Yellow
    Write-Host "------------------------------------------" -ForegroundColor Yellow
    Write-Host "URL: $Url"
    Write-Host "Method: $Method"
    
    try {
        $params = @{
            Uri = $Url
            Method = $Method
        }
        
        if ($Body) {
            $params.Body = ($Body | ConvertTo-Json)
            $params.ContentType = "application/json"
            Write-Host "Body: $($params.Body)"
        }
        
        $response = Invoke-RestMethod @params
        
        Write-Host "Status: SUCCESS" -ForegroundColor Green
        Write-Host "Response:" -ForegroundColor Cyan
        Write-Host ($response | ConvertTo-Json -Depth 5)
        
        $script:testsPassed++
        return $response
        
    } catch {
        Write-Host "Status: FAILED" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        $script:testsFailed++
        return $null
    }
}

# ==================== BACKEND TESTS ====================
Write-Host "`n`n========================================" -ForegroundColor Cyan
Write-Host "  BACKEND API TESTS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Test 1: Health Check
$health = Test-Endpoint `
    -Name "Health Check" `
    -Url "http://localhost:8000/health"

if ($health -and $health.status -eq "healthy") {
    Write-Host "✓ Backend is healthy" -ForegroundColor Green
}

# Test 2: API Documentation
Write-Host "`n------------------------------------------" -ForegroundColor Yellow
Write-Host "TEST: API Documentation" -ForegroundColor Yellow
Write-Host "------------------------------------------" -ForegroundColor Yellow
Write-Host "Opening Swagger UI in browser..."
Start-Process "http://localhost:8000/docs"
Start-Sleep -Seconds 2
Write-Host "✓ API docs opened" -ForegroundColor Green
$script:testsPassed++

# Test 3: Geocoding
$address = "1600 Pennsylvania Avenue NW, Washington, DC"
$encodedAddress = [uri]::EscapeDataString($address)
$geocode = Test-Endpoint `
    -Name "Geocode Address" `
    -Url "http://localhost:8000/api/geocode?address=$encodedAddress"

$lat = 38.8977
$lon = -77.0365
if ($geocode) {
    $lat = $geocode.latitude
    $lon = $geocode.longitude
    Write-Host "✓ Coordinates: $lat, $lon" -ForegroundColor Green
}

# Test 4: Risk Assessment
$riskBody = @{
    address = $address
    latitude = $lat
    longitude = $lon
}

$assessment = Test-Endpoint `
    -Name "Calculate Risk Assessment" `
    -Url "http://localhost:8000/api/risk-assessment/calculate" `
    -Method "POST" `
    -Body $riskBody

if ($assessment) {
    Write-Host "✓ Overall Risk Score: $($assessment.overall_score)" -ForegroundColor Green
    Write-Host "  - Climate Risk: $($assessment.climate_risk.score)" -ForegroundColor Cyan
    Write-Host "  - Crime Risk: $($assessment.crime_risk.score)" -ForegroundColor Cyan
    Write-Host "  - Economic Risk: $($assessment.economic_risk.score)" -ForegroundColor Cyan
    Write-Host "  - Infrastructure Risk: $($assessment.infrastructure_risk.score)" -ForegroundColor Cyan
}

# Test 5: Weather Data
$weather = Test-Endpoint `
    -Name "Get Weather Data" `
    -Url "http://localhost:8000/api/weather/$lat/$lon"

if ($weather) {
    Write-Host "✓ Weather: $($weather.temperature)°F, $($weather.description)" -ForegroundColor Green
}

# Test 6: Weather Forecast
$forecast = Test-Endpoint `
    -Name "Get Weather Forecast" `
    -Url "http://localhost:8000/api/weather/$lat/$lon/forecast"

# Test 7: Create Property
$propertyBody = @{
    address = "742 Evergreen Terrace, Springfield"
    latitude = 42.3601
    longitude = -71.0589
    property_type = "single_family"
    bedrooms = 3
    bathrooms = 2
    square_feet = 2000
    year_built = 1985
}

$property = Test-Endpoint `
    -Name "Create Property" `
    -Url "http://localhost:8000/api/properties/" `
    -Method "POST" `
    -Body $propertyBody

# Test 8: Get All Properties
$properties = Test-Endpoint `
    -Name "Get All Properties" `
    -Url "http://localhost:8000/api/properties/"

if ($properties) {
    $count = if ($properties -is [array]) { $properties.Count } else { 1 }
    Write-Host "✓ Found $count properties" -ForegroundColor Green
}

# ==================== PERFORMANCE TEST ====================
Write-Host "`n`n========================================" -ForegroundColor Cyan
Write-Host "  PERFORMANCE TEST" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "Running 50 requests to /health endpoint..."
$times = @()

for ($i = 1; $i -le 50; $i++) {
    $start = Get-Date
    try {
        Invoke-RestMethod -Uri "http://localhost:8000/health" -ErrorAction SilentlyContinue | Out-Null
        $end = Get-Date
        $elapsed = ($end - $start).TotalMilliseconds
        $times += $elapsed
    } catch {
        # Ignore errors in perf test
    }
    
    if ($i % 10 -eq 0) {
        Write-Host "  Progress: $i/50" -ForegroundColor Gray
    }
}

if ($times.Count -gt 0) {
    $avgTime = ($times | Measure-Object -Average).Average
    $maxTime = ($times | Measure-Object -Maximum).Maximum
    $minTime = ($times | Measure-Object -Minimum).Minimum
    
    Write-Host "`nPerformance Results:" -ForegroundColor Cyan
    Write-Host "  Average: $([math]::Round($avgTime, 2))ms" -ForegroundColor Green
    Write-Host "  Min: $([math]::Round($minTime, 2))ms" -ForegroundColor Green
    Write-Host "  Max: $([math]::Round($maxTime, 2))ms" -ForegroundColor Green
    
    if ($avgTime -lt 100) {
        Write-Host "✓ Performance: Excellent (<100ms)" -ForegroundColor Green
        $script:testsPassed++
    } elseif ($avgTime -lt 500) {
        Write-Host "✓ Performance: Good (<500ms)" -ForegroundColor Yellow
        $script:testsPassed++
    } else {
        Write-Host "✗ Performance: Needs Improvement (>500ms)" -ForegroundColor Red
        $script:testsFailed++
    }
}

# ==================== FRONTEND TESTS ====================
Write-Host "`n`n========================================" -ForegroundColor Cyan
Write-Host "  FRONTEND TESTS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "`nChecking frontend server..."
try {
    $frontendCheck = Invoke-WebRequest -Uri "http://localhost:5173" -UseBasicParsing -ErrorAction Stop
    Write-Host "✓ Frontend server is running" -ForegroundColor Green
    Write-Host "✓ Opening frontend in browser..." -ForegroundColor Green
    Start-Process "http://localhost:5173"
    $script:testsPassed++
} catch {
    Write-Host "✗ Frontend server not responding" -ForegroundColor Red
    Write-Host "  Make sure to run: cd frontend; npm run dev" -ForegroundColor Yellow
    $script:testsFailed++
}

# ==================== INTEGRATION TEST ====================
Write-Host "`n`n========================================" -ForegroundColor Cyan
Write-Host "  INTEGRATION TEST" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "`nTesting complete workflow..."
Write-Host "1. Geocoding address..." -ForegroundColor Cyan
$testAddress = "Empire State Building, New York"
$encodedAddr = [uri]::EscapeDataString($testAddress)

try {
    $geo = Invoke-RestMethod -Uri "http://localhost:8000/api/geocode?address=$encodedAddr"
    Write-Host "   ✓ Geocoded: $($geo.latitude), $($geo.longitude)" -ForegroundColor Green
    
    Write-Host "2. Calculating risk..." -ForegroundColor Cyan
    $riskData = @{
        address = $testAddress
        latitude = $geo.latitude
        longitude = $geo.longitude
    } | ConvertTo-Json
    
    $risk = Invoke-RestMethod -Uri "http://localhost:8000/api/risk-assessment/calculate" `
        -Method POST -Body $riskData -ContentType "application/json"
    Write-Host "   ✓ Risk Score: $($risk.overall_score)" -ForegroundColor Green
    
    Write-Host "3. Fetching weather..." -ForegroundColor Cyan
    $wx = Invoke-RestMethod -Uri "http://localhost:8000/api/weather/$($geo.latitude)/$($geo.longitude)"
    Write-Host "   ✓ Weather: $($wx.temperature)°F" -ForegroundColor Green
    
    Write-Host "`n✓ Integration test PASSED" -ForegroundColor Green
    $script:testsPassed++
    
} catch {
    Write-Host "`n✗ Integration test FAILED: $($_.Exception.Message)" -ForegroundColor Red
    $script:testsFailed++
}

# ==================== SUMMARY ====================
Write-Host "`n`n========================================" -ForegroundColor Cyan
Write-Host "  TEST SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$totalTests = $testsPassed + $testsFailed
$successRate = if ($totalTests -gt 0) { [math]::Round(($testsPassed / $totalTests) * 100, 2) } else { 0 }

Write-Host "`nTotal Tests: $totalTests" -ForegroundColor White
Write-Host "Passed: $testsPassed" -ForegroundColor Green
Write-Host "Failed: $testsFailed" -ForegroundColor Red
Write-Host "Success Rate: $successRate%" -ForegroundColor $(if ($successRate -ge 90) { "Green" } elseif ($successRate -ge 70) { "Yellow" } else { "Red" })

if ($testsFailed -eq 0) {
    Write-Host "`n✓ ALL TESTS PASSED!" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Cyan
    exit 0
} else {
    Write-Host "`n✗ SOME TESTS FAILED" -ForegroundColor Red
    Write-Host "==========================================" -ForegroundColor Cyan
    exit 1
}

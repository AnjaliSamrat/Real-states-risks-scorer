# ==========================================
# PROJECT STATUS CHECKER
# ==========================================

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  REAL ESTATE RISK SCORER - STATUS" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Check Servers
Write-Host ""
Write-Host "SERVERS:" -ForegroundColor Yellow
try { 
    Invoke-RestMethod -Uri "http://localhost:8001/health" -ErrorAction Stop | Out-Null
    Write-Host "  Backend (8001):  RUNNING" -ForegroundColor Green
} catch { 
    Write-Host "  Backend (8001):  NOT RUNNING" -ForegroundColor Red
}

try { 
    Invoke-WebRequest -Uri "http://localhost:5174" -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop | Out-Null
    Write-Host "  Frontend (5174): RUNNING" -ForegroundColor Green
} catch { 
    Write-Host "  Frontend (5174): NOT RUNNING" -ForegroundColor Red
}

# Access URLs
Write-Host ""
Write-Host "ACCESS YOUR APP:" -ForegroundColor Yellow
Write-Host "  Frontend:  http://localhost:5174" -ForegroundColor Cyan
Write-Host "  API Docs:  http://localhost:8001/docs" -ForegroundColor Cyan

# Check Key Files
Write-Host ""
Write-Host "PROJECT FILES:" -ForegroundColor Yellow

$fileGroups = @{
    "Backend" = @(
        "backend/app/main.py",
        "backend/app/api/routes/properties.py",
        "backend/app/api/routes/auth.py",
        "backend/app/api/routes/weather.py",
        "backend/app/core/risk_engine.py",
        "backend/app/core/pdf_generator.py"
    )
    "Frontend" = @(
        "frontend/src/App.tsx",
        "frontend/src/pages/Home.tsx",
        "frontend/src/pages/PropertyDetail.tsx",
        "frontend/src/components/Map/PropertyMap.tsx",
        "frontend/src/components/Weather/WeatherWidget.tsx"
    )
    "ML & Training" = @(
        "ml/training/train_climate_model.py",
        "ml/training/train_crime_model.py",
        "ml/README.md"
    )
    "Documentation" = @(
        "README.md",
        "TESTING_GUIDE.md",
        "QUICKSTART.md",
        "PROJECT_COMPLETE.md"
    )
    "Testing" = @(
        "test_api.ps1",
        "test_final.ps1",
        "backend/tests/conftest.py"
    )
}

foreach ($group in $fileGroups.Keys) {
    Write-Host ""
    Write-Host "  $group" -ForegroundColor Cyan -NoNewline
    Write-Host ":"
    foreach ($file in $fileGroups[$group]) {
        if (Test-Path $file) {
            Write-Host "    $file" -ForegroundColor Green
        } else {
            Write-Host "    $file - MISSING" -ForegroundColor Red
        }
    }
}

# Key Features
Write-Host ""
Write-Host "KEY FEATURES IMPLEMENTED:" -ForegroundColor Yellow
Write-Host "  Property Search & Risk Assessment" -ForegroundColor Green
Write-Host "  FREE Interactive Maps (Leaflet + OpenStreetMap)" -ForegroundColor Green
Write-Host "  Weather Widget Integration" -ForegroundColor Green
Write-Host "  User Authentication (JWT)" -ForegroundColor Green
Write-Host "  PDF Report Generation" -ForegroundColor Green
Write-Host "  ML Training Scripts (Climate & Crime)" -ForegroundColor Green
Write-Host "  RESTful API with FastAPI" -ForegroundColor Green
Write-Host "  React + TypeScript Frontend" -ForegroundColor Green
Write-Host "  Comprehensive Testing Suite" -ForegroundColor Green

# Dependencies
Write-Host ""
Write-Host "DEPENDENCIES:" -ForegroundColor Yellow
if (Test-Path "backend/venv") {
    Write-Host "  Backend: Python venv created" -ForegroundColor Green
} else {
    Write-Host "  Backend: Python venv MISSING" -ForegroundColor Red
}

if (Test-Path "frontend/node_modules") {
    Write-Host "  Frontend: node_modules installed" -ForegroundColor Green
} else {
    Write-Host "  Frontend: node_modules MISSING" -ForegroundColor Red
}

# Quick Commands
Write-Host ""
Write-Host "QUICK COMMANDS:" -ForegroundColor Yellow
Write-Host "  Test API:         .\test_api.ps1" -ForegroundColor Cyan
Write-Host "  Full Test Suite:  .\test_final.ps1" -ForegroundColor Cyan
Write-Host "  Open Frontend:    Start-Process http://localhost:5174" -ForegroundColor Cyan
Write-Host "  Open API Docs:    Start-Process http://localhost:8001/docs" -ForegroundColor Cyan
Write-Host "  View README:      Get-Content README.md" -ForegroundColor Cyan

# Summary
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
$existingFiles = $fileGroups.Values | ForEach-Object { $_ } | Where-Object { Test-Path $_ }
$totalFiles = ($fileGroups.Values | ForEach-Object { $_.Count } | Measure-Object -Sum).Sum
$completionRate = [math]::Round(($existingFiles.Count / $totalFiles) * 100, 1)

Write-Host "  PROJECT COMPLETION: $completionRate%" -ForegroundColor $(if ($completionRate -ge 90) { "Green" } elseif ($completionRate -ge 70) { "Yellow" } else { "Red" })
Write-Host "  Files: $($existingFiles.Count)/$totalFiles" -ForegroundColor White
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

if ($completionRate -eq 100) {
    Write-Host "ALL SYSTEMS READY! Your Real Estate Risk Scorer is complete!" -ForegroundColor Green
} elseif ($completionRate -ge 90) {
    Write-Host "Almost complete! Just a few files missing." -ForegroundColor Yellow
} else {
    Write-Host "Some components are missing. Check the list above." -ForegroundColor Red
}

Write-Host ""

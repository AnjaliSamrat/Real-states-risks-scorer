# Quick Test Runner
# Run specific test suites

param(
    [string]$Suite = "all"
)

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  TEST RUNNER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

switch ($Suite) {
    "backend" {
        Write-Host "`nRunning Backend Tests..." -ForegroundColor Yellow
        cd backend
        .\venv\Scripts\activate
        pytest tests/ -v
    }
    
    "api" {
        Write-Host "`nRunning API Manual Tests..." -ForegroundColor Yellow
        cd backend
        .\venv\Scripts\activate
        python tests/test_api_manual.py
    }
    
    "quick" {
        Write-Host "`nRunning Quick Health Check..." -ForegroundColor Yellow
        try {
            $health = Invoke-RestMethod -Uri "http://localhost:8000/health"
            Write-Host "✓ Backend: $($health.status)" -ForegroundColor Green
        } catch {
            Write-Host "✗ Backend: Not running" -ForegroundColor Red
        }
        
        try {
            Invoke-WebRequest -Uri "http://localhost:5173" -UseBasicParsing | Out-Null
            Write-Host "✓ Frontend: Running" -ForegroundColor Green
        } catch {
            Write-Host "✗ Frontend: Not running" -ForegroundColor Red
        }
    }
    
    "all" {
        Write-Host "`nRunning Complete Test Suite..." -ForegroundColor Yellow
        .\test_all.ps1
    }
    
    default {
        Write-Host "`nUsage: .\run_tests.ps1 [suite]" -ForegroundColor Yellow
        Write-Host "`nAvailable suites:" -ForegroundColor Cyan
        Write-Host "  all      - Run all tests (default)" -ForegroundColor Gray
        Write-Host "  backend  - Run backend pytest tests" -ForegroundColor Gray
        Write-Host "  api      - Run API manual tests" -ForegroundColor Gray
        Write-Host "  quick    - Quick health check" -ForegroundColor Gray
    }
}

Write-Host "`n========================================`n" -ForegroundColor Cyan

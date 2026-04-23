# 🧪 Complete Testing Guide

## Table of Contents
1. [Backend API Testing](#1-backend-api-testing)
2. [Frontend Testing](#2-frontend-testing)
3. [Integration Testing](#3-integration-testing)
4. [Performance Testing](#4-performance-testing)
5. [Automated Testing](#5-automated-testing)

---

## 1. Backend API Testing

### Prerequisites
- Backend server running on `http://localhost:8000`
- Tools: PowerShell, curl, or Postman

### Test 1: Health Check
**Endpoint:** `GET /health`

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET
```

**Expected Response:**
```json
{
  "status": "healthy",
  "environment": "development"
}
```

**Status Code:** `200 OK`

---

### Test 2: API Documentation
**Endpoint:** `GET /docs`

**Browser Test:**
Open: `http://localhost:8000/docs`

**Expected:** Interactive Swagger UI with all API endpoints documented

---

### Test 3: Geocode Address
**Endpoint:** `GET /api/geocode`

**PowerShell:**
```powershell
$params = @{
    address = "1600 Pennsylvania Avenue NW, Washington, DC"
}
$uri = "http://localhost:8000/api/geocode?" + ($params.GetEnumerator() | ForEach-Object { "$($_.Key)=$([uri]::EscapeDataString($_.Value))" } | Join-String -Separator "&")
Invoke-RestMethod -Uri $uri -Method GET
```

**Expected Response:**
```json
{
  "address": "1600 Pennsylvania Avenue NW, Washington, DC 20500",
  "latitude": 38.8977,
  "longitude": -77.0365,
  "place_id": "...",
  "display_name": "..."
}
```

**Status Code:** `200 OK`

---

### Test 4: Create Risk Assessment
**Endpoint:** `POST /api/risk-assessment/calculate`

**PowerShell:**
```powershell
$body = @{
    address = "1600 Pennsylvania Avenue NW, Washington, DC"
    latitude = 38.8977
    longitude = -77.0365
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/risk-assessment/calculate" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Expected Response:**
```json
{
  "overall_score": 65,
  "risk_level": "moderate",
  "climate_risk": {
    "score": 55,
    "level": "moderate",
    "factors": {
      "flood_risk": 45,
      "wildfire_risk": 20,
      "hurricane_risk": 75,
      "extreme_heat": 60
    }
  },
  "crime_risk": {
    "score": 40,
    "level": "low"
  },
  "economic_risk": {
    "score": 50,
    "level": "moderate"
  },
  "infrastructure_risk": {
    "score": 35,
    "level": "low"
  }
}
```

**Status Code:** `200 OK`

---

### Test 5: Get Weather Data
**Endpoint:** `GET /api/weather/{lat}/{lon}`

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/weather/38.8977/-77.0365" -Method GET
```

**Expected Response:**
```json
{
  "temperature": 72.5,
  "feels_like": 70.2,
  "humidity": 65,
  "wind_speed": 8.5,
  "clouds": 40,
  "description": "partly cloudy",
  "icon": "02d"
}
```

**Status Code:** `200 OK`

---

### Test 6: Create Property
**Endpoint:** `POST /api/properties/`

**PowerShell:**
```powershell
$body = @{
    address = "742 Evergreen Terrace, Springfield"
    latitude = 42.3601
    longitude = -71.0589
    property_type = "single_family"
    bedrooms = 3
    bathrooms = 2
    square_feet = 2000
    year_built = 1985
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/properties/" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Expected Response:**
```json
{
  "id": "uuid-here",
  "address": "742 Evergreen Terrace, Springfield",
  "latitude": 42.3601,
  "longitude": -71.0589,
  "property_type": "single_family",
  "bedrooms": 3,
  "bathrooms": 2,
  "square_feet": 2000,
  "year_built": 1985,
  "created_at": "2025-12-21T10:30:00Z"
}
```

**Status Code:** `201 Created`

---

### Test 7: Generate PDF Report
**Endpoint:** `GET /api/reports/property/{property_id}`

**PowerShell:**
```powershell
$propertyId = "your-property-id-here"
Invoke-WebRequest -Uri "http://localhost:8000/api/reports/property/$propertyId" `
    -Method GET `
    -OutFile "property_report.pdf"
```

**Expected:** PDF file downloaded successfully

**Status Code:** `200 OK`

---

## 2. Frontend Testing

### Prerequisites
- Frontend server running on `http://localhost:5173`
- Browser: Chrome, Firefox, or Edge

### Manual UI Tests

#### Test 1: Home Page Load
1. Navigate to `http://localhost:5173`
2. **Verify:**
   - Page loads without errors
   - Logo and navigation visible
   - Search bar present
   - Call-to-action buttons functional

#### Test 2: Address Search
1. Enter address: `1600 Pennsylvania Avenue NW, Washington, DC`
2. Click "Search" or press Enter
3. **Verify:**
   - Loading indicator appears
   - Results display
   - Property card shows address, risk score
   - Map loads with marker

#### Test 3: Property Detail Page
1. Click on a property from search results
2. **Verify:**
   - Property details load
   - Risk score card displays
   - Risk breakdown shows all categories
   - Map displays property location
   - Weather widget shows current conditions

#### Test 4: Risk Score Visualization
1. On property detail page
2. **Verify:**
   - Overall risk score displayed prominently
   - Color coding correct (green=low, yellow=moderate, red=high)
   - Individual risk categories visible
   - Charts/graphs render properly

#### Test 5: Dashboard Page
1. Navigate to `/dashboard`
2. **Verify:**
   - Dashboard loads
   - Saved properties displayed
   - Recent assessments shown
   - Charts render correctly

#### Test 6: PDF Report Generation
1. On property detail page
2. Click "Download Report" button
3. **Verify:**
   - Loading indicator appears
   - PDF downloads successfully
   - PDF contains all property information

---

## 3. Integration Testing

### End-to-End Flow Test

**Scenario:** Complete property risk assessment workflow

**Steps:**
1. Start backend server
2. Start frontend server
3. Open browser to `http://localhost:5173`
4. Search for address
5. View property details
6. Generate PDF report
7. Check dashboard

**PowerShell Script:**
```powershell
# Test E2E Flow
Write-Host "Testing End-to-End Flow..." -ForegroundColor Cyan

# Test 1: Backend health
$health = Invoke-RestMethod -Uri "http://localhost:8000/health"
if ($health.status -eq "healthy") {
    Write-Host "✓ Backend healthy" -ForegroundColor Green
} else {
    Write-Host "✗ Backend unhealthy" -ForegroundColor Red
    exit 1
}

# Test 2: Geocode
$address = "1600 Pennsylvania Avenue NW, Washington, DC"
$geocode = Invoke-RestMethod -Uri "http://localhost:8000/api/geocode?address=$([uri]::EscapeDataString($address))"
Write-Host "✓ Geocoding successful: $($geocode.latitude), $($geocode.longitude)" -ForegroundColor Green

# Test 3: Risk Assessment
$body = @{
    address = $address
    latitude = $geocode.latitude
    longitude = $geocode.longitude
} | ConvertTo-Json

$assessment = Invoke-RestMethod -Uri "http://localhost:8000/api/risk-assessment/calculate" `
    -Method POST -Body $body -ContentType "application/json"
Write-Host "✓ Risk assessment: Score $($assessment.overall_score)" -ForegroundColor Green

# Test 4: Weather
$weather = Invoke-RestMethod -Uri "http://localhost:8000/api/weather/$($geocode.latitude)/$($geocode.longitude)"
Write-Host "✓ Weather: $($weather.temperature)°F, $($weather.description)" -ForegroundColor Green

Write-Host "`n✓ All integration tests passed!" -ForegroundColor Green
```

---

## 4. Performance Testing

### Backend Load Testing

**Test API response times under load**

**PowerShell Script:**
```powershell
# Performance test
Write-Host "Performance Testing..." -ForegroundColor Cyan

$iterations = 100
$times = @()

for ($i = 1; $i -le $iterations; $i++) {
    $start = Get-Date
    Invoke-RestMethod -Uri "http://localhost:8000/health" | Out-Null
    $end = Get-Date
    $elapsed = ($end - $start).TotalMilliseconds
    $times += $elapsed
    
    if ($i % 10 -eq 0) {
        Write-Host "Completed $i/$iterations requests..." -ForegroundColor Yellow
    }
}

$avgTime = ($times | Measure-Object -Average).Average
$maxTime = ($times | Measure-Object -Maximum).Maximum
$minTime = ($times | Measure-Object -Minimum).Minimum

Write-Host "`nResults:" -ForegroundColor Cyan
Write-Host "  Average: $([math]::Round($avgTime, 2))ms" -ForegroundColor Green
Write-Host "  Min: $([math]::Round($minTime, 2))ms" -ForegroundColor Green
Write-Host "  Max: $([math]::Round($maxTime, 2))ms" -ForegroundColor Green

if ($avgTime -lt 100) {
    Write-Host "✓ Performance excellent (<100ms)" -ForegroundColor Green
} elseif ($avgTime -lt 500) {
    Write-Host "✓ Performance good (<500ms)" -ForegroundColor Yellow
} else {
    Write-Host "✗ Performance needs improvement (>500ms)" -ForegroundColor Red
}
```

---

## 5. Automated Testing

### Backend Unit Tests (pytest)

**Install pytest:**
```powershell
cd backend
.\venv\Scripts\activate
pip install pytest pytest-asyncio httpx
```

**Run tests:**
```powershell
cd backend
.\venv\Scripts\activate
pytest tests/ -v
```

**Coverage report:**
```powershell
pip install pytest-cov
pytest tests/ --cov=app --cov-report=html
```

### Frontend Unit Tests (Vitest)

**Install Vitest:**
```powershell
cd frontend
npm install -D vitest @testing-library/react @testing-library/jest-dom
```

**Run tests:**
```powershell
cd frontend
npm run test
```

**Run tests with coverage:**
```powershell
npm run test:coverage
```

---

## Test Checklist

### Before Deployment
- [ ] All backend endpoints return expected responses
- [ ] Frontend loads without console errors
- [ ] Search functionality works
- [ ] Property details display correctly
- [ ] PDF reports generate successfully
- [ ] Weather widget shows data
- [ ] Map displays property markers
- [ ] Risk scores calculate accurately
- [ ] Performance tests pass (<500ms avg)
- [ ] Unit tests pass (>80% coverage)
- [ ] Integration tests pass
- [ ] Cross-browser testing complete
- [ ] Mobile responsive design verified

### API Test Summary

| Endpoint | Method | Status | Response Time |
|----------|--------|--------|---------------|
| /health | GET | ✓ | <50ms |
| /docs | GET | ✓ | <100ms |
| /api/geocode | GET | ✓ | <200ms |
| /api/risk-assessment/calculate | POST | ✓ | <300ms |
| /api/weather/{lat}/{lon} | GET | ✓ | <150ms |
| /api/properties/ | GET | ✓ | <100ms |
| /api/properties/ | POST | ✓ | <150ms |
| /api/reports/property/{id} | GET | ✓ | <500ms |

---

## Troubleshooting

### Common Issues

**Issue 1: Backend not responding**
```powershell
# Check if backend is running
Invoke-RestMethod -Uri "http://localhost:8000/health"

# Restart backend
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload
```

**Issue 2: Frontend not loading**
```powershell
# Check if frontend is running
curl http://localhost:5173

# Restart frontend
cd frontend
npm run dev
```

**Issue 3: API requests failing with CORS errors**
- Check `backend/app/main.py` has CORS middleware configured
- Verify frontend is making requests to correct URL

**Issue 4: PDF generation fails**
```powershell
# Ensure reportlab is installed
cd backend
.\venv\Scripts\activate
pip install reportlab pillow
```

---

## Continuous Integration

The project includes GitHub Actions workflow (`.github/workflows/ci.yml`) that runs:
- Backend unit tests
- Frontend unit tests
- Linting
- Type checking
- Build verification

**Triggered on:**
- Push to main branch
- Pull request creation
- Manual workflow dispatch

---

## Testing Best Practices

1. **Test Early, Test Often** - Run tests after each code change
2. **Automate Everything** - Use CI/CD for automated testing
3. **Write Meaningful Tests** - Cover edge cases and error scenarios
4. **Monitor Performance** - Track API response times
5. **Keep Tests Updated** - Update tests when features change
6. **Test on Multiple Browsers** - Verify cross-browser compatibility
7. **Use Real Data** - Test with production-like data when possible
8. **Document Test Cases** - Keep this guide updated

---

## Additional Resources

- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Vitest Documentation](https://vitest.dev/)
- [pytest Documentation](https://docs.pytest.org/)

---

**Last Updated:** December 21, 2025  
**Version:** 1.0  
**Maintainer:** Real Estate Risk Scorer Team

# ==========================================
# MAPBOX SETUP GUIDE
# ==========================================

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  MAPBOX INTERACTIVE MAPS SETUP" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "STEP 1: Get Your FREE Mapbox Token" -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Gray
Write-Host ""
Write-Host "  1. Opening Mapbox signup page..." -ForegroundColor White
Start-Process "https://account.mapbox.com/auth/signup/"
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "  2. Sign up (completely FREE):" -ForegroundColor White
Write-Host "     - Use your email" -ForegroundColor Gray
Write-Host "     - Verify your email" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. After signing up, get your token:" -ForegroundColor White
Write-Host "     - Go to: https://account.mapbox.com/access-tokens/" -ForegroundColor Cyan
Write-Host "     - Copy your 'Default Public Token' (starts with pk.)" -ForegroundColor Cyan

Write-Host ""
Write-Host "Press Enter when you have your token copied..." -ForegroundColor Yellow
Read-Host

# STEP 2: Check if Mapbox is installed
Write-Host ""
Write-Host "STEP 2: Checking Mapbox Installation" -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Gray

cd frontend

$packageJson = Get-Content package.json | ConvertFrom-Json
$mapboxInstalled = $packageJson.dependencies.'mapbox-gl'

if ($mapboxInstalled) {
    Write-Host "  Mapbox GL: $mapboxInstalled - Installed" -ForegroundColor Green
} else {
    Write-Host "  Installing Mapbox GL..." -ForegroundColor Yellow
    npm install mapbox-gl
    npm install --save-dev @types/mapbox-gl
    Write-Host "  Mapbox installed!" -ForegroundColor Green
}

# STEP 3: Create .env file
Write-Host ""
Write-Host "STEP 3: Creating Environment File" -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Gray

Write-Host ""
Write-Host "Paste your Mapbox token (starts with pk.):" -ForegroundColor Cyan
$token = Read-Host

if ($token -match '^pk\.') {
    # Create .env file
    @"
# Mapbox Token (get free token at https://account.mapbox.com/)
VITE_MAPBOX_TOKEN=$token

# Backend API URL
VITE_API_URL=http://localhost:8000

# OpenWeatherMap (optional)
VITE_OPENWEATHER_API_KEY=
"@ | Out-File -FilePath ".env" -Encoding UTF8

    Write-Host ""
    Write-Host "  .env file created successfully!" -ForegroundColor Green
    Write-Host "  Token saved: $($token.Substring(0,15))..." -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "  Invalid token format. Token should start with 'pk.'" -ForegroundColor Red
    Write-Host "  Please create .env file manually" -ForegroundColor Yellow
}

# STEP 4: Verify components
Write-Host ""
Write-Host "STEP 4: Verifying Components" -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Gray

$mapComponent = Test-Path "src/components/Map/PropertyMap.tsx"
$detailPage = Test-Path "src/pages/PropertyDetail.tsx"

if ($mapComponent) {
    Write-Host "  PropertyMap component: Exists" -ForegroundColor Green
} else {
    Write-Host "  PropertyMap component: Missing" -ForegroundColor Red
}

if ($detailPage) {
    Write-Host "  PropertyDetail page: Exists" -ForegroundColor Green
} else {
    Write-Host "  PropertyDetail page: Missing" -ForegroundColor Red
}

# STEP 5: Start frontend
Write-Host ""
Write-Host "STEP 5: Starting Frontend" -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Gray
Write-Host ""
Write-Host "  Starting Vite development server..." -ForegroundColor White
Write-Host ""

# Return to root directory
cd ..

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  SETUP COMPLETE!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Frontend will start automatically" -ForegroundColor White
Write-Host "  2. Open: http://localhost:5173" -ForegroundColor Cyan
Write-Host "  3. Navigate to any property page" -ForegroundColor White
Write-Host "  4. You should see an interactive Mapbox map!" -ForegroundColor Green
Write-Host ""
Write-Host "Map Features:" -ForegroundColor Yellow
Write-Host "  - Interactive markers with risk colors" -ForegroundColor Gray
Write-Host "  - Popup with property details" -ForegroundColor Gray
Write-Host "  - Risk radius circle" -ForegroundColor Gray
Write-Host "  - Navigation and fullscreen controls" -ForegroundColor Gray
Write-Host "  - Zoom/pan gestures" -ForegroundColor Gray
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Start frontend in new terminal
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\anjal\OneDrive\Documents\real-estate risks scorer\frontend'; npm run dev"

# Real Estate Risk Scorer - Project Overview

## Purpose
This project is a full-stack application designed to assess and visualize real estate risks for properties in India. It combines data from multiple sources (climate, crime, economic, infrastructure, etc.) to provide risk scores and insights for property locations.

## Key Features
- **Property Search & Geocoding:** Users can search for properties by address. The app uses geocoding to convert addresses to coordinates.
- **Risk Assessment:** The backend calculates risk scores for properties based on climate, crime, economic, and infrastructure data.
- **Interactive Dashboard:** The frontend (React + Vite) displays property information, risk scores, and maps for easy analysis.
- **User Accounts & Saved Properties:** Users can register/login and bookmark (“save”) properties for quick access.
- **Assessment Change Tracking (Delta):** For a given property, the system can compare the last two saved risk assessments and show what changed over time.
- **API-Driven:** The backend (FastAPI) exposes RESTful endpoints for geocoding, property management, risk analysis, and predictions.
- **Modular ML Pipeline:** The `ml/` directory contains scripts and notebooks for data processing and model training.

## Technology Stack
- **Frontend:** React, Vite, TypeScript, Tailwind CSS
- **Backend:** FastAPI (Python), SQLAlchemy, Uvicorn
- **Database:** SQLite (dev), can be extended to PostgreSQL
- **ML/Analytics:** Python scripts and Jupyter notebooks
- **Dev Tools:** Docker, VS Code, PowerShell scripts

## How It Works
1. **User searches for a property** by address in the dashboard.
2. **Geocoding service** converts the address to latitude/longitude.
3. **Backend aggregates risk data** for the location from various providers.
4. **Risk scores and details** are returned and visualized on the dashboard.

## Advanced Features (Implemented)
- **Login/Register (JWT):** Session token stored in browser and sent as `Authorization: Bearer <token>`.
- **Saved Properties:** Save/Unsave a property from the property detail page; view saved list at `/saved`.
- **Assessment Delta/Compare:** Endpoint returns `latest`, `previous`, and `delta` scores for a property (when at least 2 assessments exist).

## Usage
- Start the backend server (FastAPI/Uvicorn)
- Start the frontend server (Vite/React)
- Access the dashboard at http://localhost:5173

### Optional: Real-time Weather
- Set `OPENWEATHER_API_KEY` to use live OpenWeatherMap data.
- Optional cache control: set `WEATHER_CACHE_TTL_SECONDS` (default: 900 seconds).

### Optional: Near Real-time Climate Data
- Climate data may call NASA POWER climatology (when not in OFFLINE_MODE) and caches results for performance and stability.
- Set `CLIMATE_CACHE_TTL_SECONDS` (default: 21600 seconds).

### Optional: Near Real-time Crime & Economic Data
- These services cache results for performance and stability.
- Set `CRIME_CACHE_TTL_SECONDS` (default: 21600 seconds).
- Set `ECONOMIC_CACHE_TTL_SECONDS` (default: 21600 seconds).

### Optional: Near Real-time Infrastructure Data
- Infrastructure data (OSM/Overpass + demo schools) caches results for performance and stability.
- Set `INFRA_CACHE_TTL_SECONDS` (default: 21600 seconds).

## Project Structure
- `frontend/` - React app (UI, API calls, dashboard)
- `backend/` - FastAPI app (API, data, services)
- `ml/` - Data, scripts, and notebooks for ML
- `infrastructure/` - Deployment and infra scripts

## Status
- Core features are implemented and working.
- Geocoding, property search, and risk scoring are live.
- Saved Properties and Assessment Delta features are implemented and demo-ready.
- Ready for demo and further enhancements.

---
*Prepared for project update/reporting.*

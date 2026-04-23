# Real Estate Risk Scorer — Demo Checklist (For Review)

## 1) Quick Start (Local)
- Backend: start Uvicorn (FastAPI) on `http://127.0.0.1:8001`
- Frontend: start Vite on `http://localhost:5173`

## 2) What to Show in Demo (3–5 minutes)
1. Open the Dashboard UI (`http://localhost:5173`).
2. (Optional) Login / Register, then show the Saved tab.
2. Search a known address (example: `Patna`).
3. Confirm geocoding suggestions appear.
4. Select a suggestion / property location on map.
5. Open a property detail page.
6. Click **Save** and confirm it appears in **Saved Properties**.
7. Generate a risk report (once).
8. Generate a second risk report (same property) and show the **Change since last assessment** (delta) card.

## 3) Key Project Value
- One dashboard to assess property risk using multiple data sources.
- API-driven design: frontend and backend are decoupled.
- Extensible: can add more data sources or ML models.

## 4) Validation (What’s Verified)
- Backend health endpoint returns OK.
- Frontend proxy routes `/api/*` requests to backend.
- Backend predict endpoint tests: `5 passed`.
- Backend risk assessment delta tests pass.
- Frontend production build succeeds.

## 5) Notes / Limitations (Current)
- Data is not fully real-time by default; real-time requires scheduled refresh + caching.
- Some external services (like geocoding) depend on network availability.

### Real-time Weather (Optional)
- Set `OPENWEATHER_API_KEY` to enable live weather.
- Control refresh rate using `WEATHER_CACHE_TTL_SECONDS` (default: 900).

### Near Real-time Climate (Optional)
- Control refresh rate using `CLIMATE_CACHE_TTL_SECONDS` (default: 21600).

### Near Real-time Crime/Economic (Optional)
- Control refresh rate using `CRIME_CACHE_TTL_SECONDS` and `ECONOMIC_CACHE_TTL_SECONDS` (default: 21600).

### Near Real-time Infrastructure (Optional)
- Control refresh rate using `INFRA_CACHE_TTL_SECONDS` (default: 21600).

---
Prepared for demo/review.

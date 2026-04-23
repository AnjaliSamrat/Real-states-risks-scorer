# Real Estate Risk Scorer

AI-powered platform for comprehensive property investment risk assessment.

## Features

- 🌍 **Climate Risk Analysis** - Flood zones, wildfires, earthquakes, sea level rise
- 🔒 **Crime & Safety** - Violent crime, property crime, trends analysis
- 💰 **Economic Indicators** - Unemployment, income, job growth
- 🏗️ **Infrastructure Scoring** - Transit, schools, hospitals, walkability
- 🤖 **ML Predictions** - Trained models for risk forecasting
- 📊 **Interactive Dashboard** - Real-time weather, risk visualizations
- 📄 **PDF Reports** - Professional assessment reports
- ✅ **Benchmarks & Regression Tests** - Reproducible India benchmark suite (see `docs/BENCHMARKS.md`)

## Tech Stack

**Backend:**
- FastAPI (Python)
- PostgreSQL + PostGIS
- Redis (caching)
- Scikit-learn (ML)
- ReportLab (PDF generation)

**Frontend:**
- React + TypeScript
- Tailwind CSS
- TanStack Query
- Recharts
- Lucide Icons

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Train ML Models

```bash
cd ml/training
python train_climate_model.py
python train_crime_model.py
```

## API Endpoints

- `POST /api/risk-assessment/analyze` - Analyze property risk
- `POST /api/predict/growth` - Predict county home-value growth (ML)
- `POST /api/predict/risk` - Predict county risk category (ML)
- `GET /api/predict/schema` - Get required feature schemas (ML)
- `GET /api/predict/health` - Check model artifacts are loadable (ML)
- `GET /api/properties/{id}` - Get property details
- `GET /api/weather/{lat}/{lon}` - Current weather
- `POST /api/auth/login` - User authentication
- `GET /docs` - Interactive API documentation

## Calibration & Validation

- Uses a deterministic India benchmark suite (offline regression checks) to keep scoring stable across changes.
- See `docs/BENCHMARKS.md` for the latest baseline table and how to regenerate it.

### ML Prediction Examples

Get required feature names/order for each model:

```bash
curl -X GET "http://127.0.0.1:8001/api/predict/schema"
```

Health check (verifies model files exist and can be loaded):

```bash
curl -X GET "http://127.0.0.1:8001/api/predict/health"
```

Example response:

```json
{
	"status": "healthy",
	"models": {
		"time_aware_gbr": "ok",
		"static_rf": "ok",
		"risk": "ok"
	}
}
```

Predict 12-month forward growth (time-aware model):

```bash
curl -X POST "http://127.0.0.1:8001/api/predict/growth?model=time_aware_gbr" \
	-H "Content-Type: application/json" \
	-d "{\"features\":{\"zhvi\":350000,\"zhvi_fwd\":365000,\"zhvi_lag_12m\":330000,\"zhvi_lag_12m_pct_change\":0.06,\"poverty_population\":8000,\"total_population\":250000,\"median_income\":65000,\"log_median_income\":11.082143,\"log_total_population\":12.42922,\"poverty_rate\":0.12,\"income_per_capita_proxy\":260}}"
```

Predict risk category (static classifier):

```bash
curl -X POST "http://127.0.0.1:8001/api/predict/risk" \
	-H "Content-Type: application/json" \
	-d "{\"features\":{\"median_income\":65000,\"log_median_income\":11.082143,\"total_population\":250000,\"log_total_population\":12.42922,\"poverty_population\":8000,\"poverty_rate\":0.12,\"income_per_capita_proxy\":260,\"poverty_x_log_income\":1.329857,\"poverty_x_log_pop\":1.491506,\"zhvi_start\":280000,\"log_zhvi_start\":12.542545}}"
```

## Deployment

### Render.com (Recommended)

1. Push code to GitHub
2. Connect repository to Render
3. Render will auto-detect `render.yaml`
4. Deploy with one click

### Docker

```bash
docker-compose up -d
```

## Environment Variables

Create `.env` file in backend/:

```
DATABASE_URL=postgresql://user:password@localhost:5432/realestate
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
OPENWEATHER_API_KEY=your-api-key
```

## Project Structure

```
real-estate-risk-scorer/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/      # API routes
│   │   ├── core/     # Risk engine, PDF gen
│   │   ├── services/ # External API integrations
│   │   └── models/   # DB models, ML models
│   └── tests/
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
├── ml/               # Machine learning
│   ├── training/     # Model training scripts
│   ├── notebooks/    # Jupyter notebooks
│   └── data/
├── infrastructure/   # Terraform, K8s
└── docs/            # Documentation
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

MIT License - see LICENSE file

## Data Sources

- **Climate:** FEMA, NOAA, NASA FIRMS, USGS
- **Crime:** FBI UCR API
- **Economic:** US Census Bureau, BLS
- **Infrastructure:** OpenStreetMap
- **Weather:** OpenWeatherMap

## Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/real-estate-risk-scorer](https://github.com/yourusername/real-estate-risk-scorer)

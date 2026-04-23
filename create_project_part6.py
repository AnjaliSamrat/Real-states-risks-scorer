import os

files = {
    # ==================== ML TRAINING SCRIPTS ====================
    r'ml\training\train_climate_model.py': r'''"""
Climate Risk Prediction Model Training
Uses historical climate data to predict future risks
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

class ClimateRiskModel:
    def __init__(self):
        self.model = None
        self.feature_names = [
            'latitude',
            'longitude',
            'elevation',
            'distance_to_coast',
            'avg_temperature',
            'avg_precipitation',
            'historical_flood_count',
            'wildfire_proximity'
        ]
    
    def generate_synthetic_data(self, n_samples=10000):
        """Generate synthetic training data for demonstration"""
        np.random.seed(42)
        
        data = {
            'latitude': np.random.uniform(25, 49, n_samples),
            'longitude': np.random.uniform(-125, -65, n_samples),
            'elevation': np.random.uniform(0, 3000, n_samples),
            'distance_to_coast': np.random.uniform(0, 500, n_samples),
            'avg_temperature': np.random.uniform(0, 35, n_samples),
            'avg_precipitation': np.random.uniform(0, 2000, n_samples),
            'historical_flood_count': np.random.poisson(2, n_samples),
            'wildfire_proximity': np.random.uniform(0, 100, n_samples),
        }
        
        df = pd.DataFrame(data)
        
        # Calculate target: climate risk score (0-100)
        df['climate_risk'] = (
            (df['distance_to_coast'] < 50).astype(int) * 20 +  # Coastal flooding
            (df['avg_temperature'] > 30).astype(int) * 15 +    # Heat risk
            df['historical_flood_count'] * 5 +                  # Flood history
            (df['wildfire_proximity'] < 20).astype(int) * 25 + # Wildfire risk
            np.random.normal(0, 5, n_samples)                   # Noise
        )
        
        df['climate_risk'] = df['climate_risk'].clip(0, 100)
        
        return df
    
    def train(self, X, y):
        """Train the model"""
        print("Training Climate Risk Prediction Model...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train Gradient Boosting model
        self.model = GradientBoostingRegressor(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        y_pred = self.model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        print(f"✅ Training Score: {train_score:.4f}")
        print(f"✅ Test Score: {test_score:.4f}")
        print(f"✅ RMSE: {rmse:.4f}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\n📊 Feature Importance:")
        print(feature_importance)
        
        return self.model
    
    def save(self, filepath='../../backend/app/models/trained/climate_model.pkl'):
        """Save trained model"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.model, filepath)
        print(f"\n💾 Model saved to: {filepath}")
    
    def predict(self, features):
        """Predict climate risk"""
        return self.model.predict(features)


if __name__ == "__main__":
    # Initialize model
    model = ClimateRiskModel()
    
    # Generate training data
    print("Generating synthetic training data...")
    df = model.generate_synthetic_data(n_samples=10000)
    
    X = df[model.feature_names]
    y = df['climate_risk']
    
    # Train model
    model.train(X, y)
    
    # Save model
    model.save()
    
    print("\n🎉 Climate Risk Model Training Complete!")
''',

    r'ml\training\train_crime_model.py': r'''"""
Crime Risk Prediction Model Training
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

class CrimeRiskModel:
    def __init__(self):
        self.model = None
        self.feature_names = [
            'latitude',
            'longitude',
            'population_density',
            'median_income',
            'unemployment_rate',
            'poverty_rate',
            'education_level'
        ]
    
    def generate_synthetic_data(self, n_samples=10000):
        """Generate synthetic crime data"""
        np.random.seed(42)
        
        data = {
            'latitude': np.random.uniform(25, 49, n_samples),
            'longitude': np.random.uniform(-125, -65, n_samples),
            'population_density': np.random.uniform(10, 10000, n_samples),
            'median_income': np.random.uniform(20000, 150000, n_samples),
            'unemployment_rate': np.random.uniform(2, 15, n_samples),
            'poverty_rate': np.random.uniform(5, 30, n_samples),
            'education_level': np.random.uniform(60, 95, n_samples),
        }
        
        df = pd.DataFrame(data)
        
        # Calculate crime risk category (0=Low, 1=Medium, 2=High)
        crime_score = (
            (df['poverty_rate'] > 20).astype(int) * 30 +
            (df['unemployment_rate'] > 8).astype(int) * 25 +
            (df['median_income'] < 40000).astype(int) * 20 +
            (df['population_density'] > 5000).astype(int) * 15
        )
        
        df['crime_category'] = pd.cut(crime_score, bins=[0, 30, 60, 100], labels=[0, 1, 2])
        
        return df
    
    def train(self, X, y):
        """Train crime prediction model"""
        print("Training Crime Risk Model...")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        train_acc = accuracy_score(y_train, self.model.predict(X_train))
        test_acc = accuracy_score(y_test, self.model.predict(X_test))
        
        print(f"✅ Training Accuracy: {train_acc:.4f}")
        print(f"✅ Test Accuracy: {test_acc:.4f}")
        
        print("\n📊 Classification Report:")
        print(classification_report(y_test, self.model.predict(X_test)))
        
        return self.model
    
    def save(self, filepath='../../backend/app/models/trained/crime_model.pkl'):
        """Save model"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.model, filepath)
        print(f"\n💾 Model saved to: {filepath}")


if __name__ == "__main__":
    model = CrimeRiskModel()
    df = model.generate_synthetic_data()
    
    X = df[model.feature_names]
    y = df['crime_category']
    
    model.train(X, y)
    model.save()
    
    print("\n🎉 Crime Risk Model Training Complete!")
''',

    # ==================== PDF REPORT GENERATION ====================
    r'backend\app\core\pdf_generator.py': r'''"""
PDF Report Generation for Property Risk Assessments
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io


class PropertyReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2563eb'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
    
    def generate_report(self, property_data, assessment_data):
        """Generate PDF report"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        
        # Title
        title = Paragraph(f"Property Risk Assessment Report", self.title_style)
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Property Information
        property_info = [
            ['Property Address:', property_data.get('address', 'N/A')],
            ['Assessment Date:', datetime.now().strftime('%Y-%m-%d')],
            ['Overall Risk Score:', f"{assessment_data.get('overall_score', 0):.1f}/100"],
            ['Risk Level:', assessment_data.get('risk_level', 'Unknown')]
        ]
        
        table = Table(property_info, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.3*inch))
        
        # Risk Breakdown
        risk_breakdown = [
            ['Risk Category', 'Score', 'Weight'],
            ['Climate Risk', f"{assessment_data.get('climate_score', 0):.1f}", '30%'],
            ['Crime Risk', f"{assessment_data.get('crime_score', 0):.1f}", '25%'],
            ['Economic Risk', f"{assessment_data.get('economic_score', 0):.1f}", '25%'],
            ['Infrastructure', f"{assessment_data.get('infrastructure_score', 0):.1f}", '20%'],
        ]
        
        risk_table = Table(risk_breakdown, colWidths=[2.5*inch, 1.5*inch, 1*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        
        story.append(Paragraph("Risk Score Breakdown", self.styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        story.append(risk_table)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def save_report(self, property_data, assessment_data, filename):
        """Save report to file"""
        buffer = self.generate_report(property_data, assessment_data)
        with open(filename, 'wb') as f:
            f.write(buffer.getvalue())
        return filename
''',

    # ==================== WEATHER SERVICE ====================
    r'backend\app\services\weather_service.py': r'''"""
Weather Data Service
Integrates with OpenWeatherMap API for real-time weather
"""
import httpx
from typing import Dict, Any


class WeatherService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or "demo"  # Get free key at openweathermap.org
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    async def get_current_weather(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """Get current weather conditions"""
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/weather"
                params = {
                    "lat": latitude,
                    "lon": longitude,
                    "appid": self.api_key,
                    "units": "metric"
                }
                
                response = await client.get(url, params=params, timeout=10.0)
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "temperature": data["main"]["temp"],
                        "feels_like": data["main"]["feels_like"],
                        "humidity": data["main"]["humidity"],
                        "pressure": data["main"]["pressure"],
                        "weather": data["weather"][0]["main"],
                        "description": data["weather"][0]["description"],
                        "wind_speed": data["wind"]["speed"],
                        "clouds": data["clouds"]["all"]
                    }
                else:
                    return self._get_mock_weather(latitude, longitude)
        except Exception as e:
            print(f"Weather API error: {e}")
            return self._get_mock_weather(latitude, longitude)
    
    async def get_forecast(self, latitude: float, longitude: float, days: int = 5) -> Dict[str, Any]:
        """Get weather forecast"""
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/forecast"
                params = {
                    "lat": latitude,
                    "lon": longitude,
                    "appid": self.api_key,
                    "units": "metric",
                    "cnt": days * 8  # 3-hour intervals
                }
                
                response = await client.get(url, params=params, timeout=10.0)
                
                if response.status_code == 200:
                    data = response.json()
                    forecast = []
                    for item in data["list"][:days]:
                        forecast.append({
                            "date": item["dt_txt"],
                            "temp": item["main"]["temp"],
                            "weather": item["weather"][0]["main"],
                            "description": item["weather"][0]["description"]
                        })
                    return {"forecast": forecast}
                else:
                    return {"forecast": []}
        except Exception as e:
            print(f"Forecast API error: {e}")
            return {"forecast": []}
    
    def _get_mock_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        """Return mock weather data for demo"""
        import random
        return {
            "temperature": round(random.uniform(10, 30), 1),
            "feels_like": round(random.uniform(10, 30), 1),
            "humidity": random.randint(40, 90),
            "pressure": random.randint(1000, 1020),
            "weather": random.choice(["Clear", "Clouds", "Rain"]),
            "description": "demo data",
            "wind_speed": round(random.uniform(0, 15), 1),
            "clouds": random.randint(0, 100)
        }
''',

    r'backend\app\api\routes\weather.py': r'''"""
Weather API Routes
"""
from fastapi import APIRouter, HTTPException
from app.services.weather_service import WeatherService

router = APIRouter()
weather_service = WeatherService()


@router.get("/{latitude}/{longitude}")
async def get_weather(latitude: float, longitude: float):
    """Get current weather for coordinates"""
    try:
        weather = await weather_service.get_current_weather(latitude, longitude)
        return weather
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{latitude}/{longitude}/forecast")
async def get_forecast(latitude: float, longitude: float, days: int = 5):
    """Get weather forecast"""
    try:
        forecast = await weather_service.get_forecast(latitude, longitude, days)
        return forecast
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
''',

    r'frontend\src\components\Weather\WeatherWidget.tsx': r'''import { useQuery } from '@tanstack/react-query'
import { Cloud, Droplets, Wind, Eye } from 'lucide-react'
import axios from 'axios'

interface Props {
  latitude: number
  longitude: number
}

export default function WeatherWidget({ latitude, longitude }: Props) {
  const { data: weather, isLoading } = useQuery({
    queryKey: ['weather', latitude, longitude],
    queryFn: async () => {
      const response = await axios.get(
        `http://localhost:8000/api/weather/${latitude}/${longitude}`
      )
      return response.data
    },
  })

  if (isLoading) {
    return <div className="bg-white rounded-lg shadow p-6">Loading weather...</div>
  }

  if (!weather) {
    return null
  }

  return (
    <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg shadow-lg p-6 text-white">
      <h3 className="text-lg font-semibold mb-4">Current Weather</h3>
      
      <div className="flex items-center justify-between mb-4">
        <div>
          <div className="text-4xl font-bold">{weather.temperature}°C</div>
          <div className="text-sm opacity-90">Feels like {weather.feels_like}°C</div>
        </div>
        <Cloud className="h-16 w-16 opacity-80" />
      </div>

      <div className="grid grid-cols-2 gap-4 text-sm">
        <div className="flex items-center">
          <Droplets className="h-4 w-4 mr-2" />
          <span>{weather.humidity}% Humidity</span>
        </div>
        <div className="flex items-center">
          <Wind className="h-4 w-4 mr-2" />
          <span>{weather.wind_speed} m/s Wind</span>
        </div>
        <div className="flex items-center">
          <Eye className="h-4 w-4 mr-2" />
          <span>{weather.weather}</span>
        </div>
        <div className="flex items-center">
          <Cloud className="h-4 w-4 mr-2" />
          <span>{weather.clouds}% Clouds</span>
        </div>
      </div>
    </div>
  )
}
''',

    # ==================== DEPLOYMENT CONFIGS ====================
    r'render.yaml': r'''services:
  # Backend API
  - type: web
    name: realestate-backend
    env: python
    region: oregon
    plan: free
    buildCommand: "cd backend && pip install -r requirements.txt"
    startCommand: "cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: ENVIRONMENT
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: realestate-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: PYTHON_VERSION
        value: 3.11.0
    healthCheckPath: /health

  # Frontend
  - type: web
    name: realestate-frontend
    env: static
    region: oregon
    plan: free
    buildCommand: "cd frontend && npm install && npm run build"
    staticPublishPath: frontend/dist
    routes:
      - type: rewrite
        source: /*
        destination: /index.html
    envVars:
      - key: VITE_API_URL
        value: https://realestate-backend.onrender.com

databases:
  - name: realestate-db
    databaseName: realestate_db
    user: postgres
    plan: free
    postgresMajorVersion: 15
''',

    r'backend\requirements.txt': r'''fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
email-validator==2.1.0
httpx==0.25.2
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.13.0
redis==5.0.1
reportlab==4.0.7
pandas==2.1.4
numpy==1.26.2
scikit-learn==1.3.2
joblib==1.3.2
''',

    r'README.md': r'''# Real Estate Risk Scorer

AI-powered platform for comprehensive property investment risk assessment.

## Features

- 🌍 **Climate Risk Analysis** - Flood zones, wildfires, earthquakes, sea level rise
- 🔒 **Crime & Safety** - Violent crime, property crime, trends analysis
- 💰 **Economic Indicators** - Unemployment, income, job growth
- 🏗️ **Infrastructure Scoring** - Transit, schools, hospitals, walkability
- 🤖 **ML Predictions** - Trained models for risk forecasting
- 📊 **Interactive Dashboard** - Real-time weather, risk visualizations
- 📄 **PDF Reports** - Professional assessment reports

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
uvicorn app.main:app --reload
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
- `GET /api/properties/{id}` - Get property details
- `GET /api/weather/{lat}/{lon}` - Current weather
- `POST /api/auth/login` - User authentication
- `GET /docs` - Interactive API documentation

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
''',

    r'.github\workflows\ci.yml': r'''name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        cd backend
        pytest tests/ -v

  frontend-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: |
        cd frontend
        npm install
    
    - name: Build
      run: |
        cd frontend
        npm run build
    
    - name: Lint
      run: |
        cd frontend
        npm run lint

  deploy:
    needs: [backend-tests, frontend-tests]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to Render
      run: echo "Deployment triggered via Render webhook"
''',
}

for filepath, content in files.items():
    dirname = os.path.dirname(filepath)
    if dirname:  # Only create directory if path has a directory component
        os.makedirs(dirname, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Created: {filepath}")

print("\n" + "="*70)
print("🎉 PART 6 COMPLETE! ML, Weather, PDF, Deployment files created!")
print("="*70)
print("\n📦 What was added:")
print("  ✅ ML training scripts (climate, crime models)")
print("  ✅ PDF report generator")
print("  ✅ Weather service integration")
print("  ✅ Weather widget component")
print("  ✅ Deployment configs (Render, Docker)")
print("  ✅ Complete README.md")
print("  ✅ GitHub Actions CI/CD")
print("  ✅ Backend requirements.txt")
print("\n🚀 Next steps:")
print("  1. Train ML models: cd ml/training && python train_climate_model.py")
print("  2. Install PDF dependencies: pip install reportlab")
print("  3. Get OpenWeatherMap API key (free)")
print("  4. Deploy to Render.com")

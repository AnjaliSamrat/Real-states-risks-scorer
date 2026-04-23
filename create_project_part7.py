import os

files = {
    # ==================== MAPBOX MAP COMPONENT ====================
    r'frontend\src\components\Map\PropertyMap.tsx': r'''import { useEffect, useRef } from 'react'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

// Get your FREE Mapbox token at: https://account.mapbox.com/
mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN || 'pk.eyJ1IjoiZXhhbXBsZSIsImEiOiJjbGV4YW1wbGUifQ.example'

interface Props {
  latitude: number
  longitude: number
  address: string
  riskScore?: number
}

export default function PropertyMap({ latitude, longitude, address, riskScore }: Props) {
  const mapContainer = useRef<HTMLDivElement>(null)
  const map = useRef<mapboxgl.Map | null>(null)

  useEffect(() => {
    if (!mapContainer.current) return

    // Initialize map
    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/streets-v12',
      center: [longitude, latitude],
      zoom: 14,
      pitch: 45,
    })

    // Add navigation controls
    map.current.addControl(new mapboxgl.NavigationControl(), 'top-right')

    // Add fullscreen control
    map.current.addControl(new mapboxgl.FullscreenControl(), 'top-right')

    // Get marker color based on risk score
    const getMarkerColor = (score?: number) => {
      if (!score) return '#3b82f6' // blue
      if (score <= 20) return '#10b981' // green
      if (score <= 40) return '#84cc16' // lime
      if (score <= 60) return '#eab308' // yellow
      if (score <= 80) return '#f97316' // orange
      return '#ef4444' // red
    }

    // Create custom marker
    const el = document.createElement('div')
    el.className = 'custom-marker'
    el.style.width = '40px'
    el.style.height = '40px'
    el.style.borderRadius = '50%'
    el.style.backgroundColor = getMarkerColor(riskScore)
    el.style.border = '3px solid white'
    el.style.boxShadow = '0 4px 6px rgba(0,0,0,0.3)'
    el.style.cursor = 'pointer'

    // Add marker with popup
    const marker = new mapboxgl.Marker({ element: el, anchor: 'bottom' })
      .setLngLat([longitude, latitude])
      .setPopup(
        new mapboxgl.Popup({ offset: 25, closeButton: false }).setHTML(
          `<div class="p-3">
            <h3 class="font-bold text-gray-900 mb-1">${address}</h3>
            <p class="text-sm text-gray-600">Lat: ${latitude.toFixed(4)}</p>
            <p class="text-sm text-gray-600">Lng: ${longitude.toFixed(4)}</p>
            ${riskScore ? `<p class="text-sm font-semibold mt-2">Risk Score: ${riskScore.toFixed(1)}</p>` : ''}
          </div>`
        )
      )
      .addTo(map.current)

    // Show popup on load
    setTimeout(() => {
      marker.togglePopup()
    }, 500)

    // Add risk radius circle
    if (riskScore) {
      map.current.on('load', () => {
        if (!map.current) return

        // Add circle layer
        map.current.addSource('risk-radius', {
          type: 'geojson',
          data: {
            type: 'Feature',
            geometry: {
              type: 'Point',
              coordinates: [longitude, latitude]
            },
            properties: {}
          }
        })

        map.current.addLayer({
          id: 'risk-circle',
          type: 'circle',
          source: 'risk-radius',
          paint: {
            'circle-radius': {
              stops: [
                [0, 0],
                [20, 300]
              ],
              base: 2
            },
            'circle-color': getMarkerColor(riskScore),
            'circle-opacity': 0.1,
            'circle-stroke-width': 2,
            'circle-stroke-color': getMarkerColor(riskScore),
            'circle-stroke-opacity': 0.3
          }
        })
      })
    }

    // Cleanup
    return () => {
      map.current?.remove()
    }
  }, [latitude, longitude, address, riskScore])

  return <div ref={mapContainer} className="w-full h-full rounded-lg" />
}
''',

    # ==================== ML TRAINING GUIDE ====================
    r'ml\README.md': r'''# 🤖 Machine Learning Model Training Guide

## Prerequisites

### 1. Install Python Dependencies
```bash
pip install pandas numpy scikit-learn joblib matplotlib seaborn jupyter
```

**Note**: scikit-learn currently requires Python 3.9-3.12. If you're using Python 3.13, consider using Python 3.11 for ML training.

### 2. Project Structure
```
ml/
├── training/
│   ├── train_climate_model.py  # Climate risk prediction
│   └── train_crime_model.py    # Crime risk classification
├── notebooks/
│   ├── data_exploration.ipynb  # Data analysis
│   └── model_training.ipynb    # Interactive training
├── data/                        # Your training datasets
└── README.md                    # This file
```

## 🚀 Quick Start

### Train Climate Risk Model
```bash
cd ml/training
python train_climate_model.py
```

**Output:**
- Model file: `backend/app/models/trained/climate_model.pkl`
- Metrics: R² score, RMSE, feature importance

### Train Crime Risk Model
```bash
cd ml/training
python train_crime_model.py
```

**Output:**
- Model file: `backend/app/models/trained/crime_model.pkl`
- Metrics: Accuracy, classification report

## 📊 Model Details

### Climate Risk Model
- **Type**: Gradient Boosting Regressor
- **Features**: 
  - Latitude, Longitude
  - Elevation
  - Distance to coast
  - Average temperature
  - Average precipitation
  - Historical flood count
  - Wildfire proximity
- **Output**: Risk score (0-100)

### Crime Risk Model
- **Type**: Random Forest Classifier
- **Features**:
  - Latitude, Longitude
  - Population density
  - Median income
  - Unemployment rate
  - Poverty rate
  - Education level
- **Output**: Risk category (Low/Medium/High)

## 🔍 Using Trained Models

### In Backend API
```python
import joblib
import numpy as np

# Load model
model = joblib.load('backend/app/models/trained/climate_model.pkl')

# Prepare features
features = np.array([[37.7749, -122.4194, 50, 10, 15, 800, 2, 50]])

# Predict
risk_score = model.predict(features)[0]
print(f"Climate Risk Score: {risk_score:.1f}")
```

## 📈 Improving Models

### 1. Collect Real Data
Replace synthetic data with actual datasets:
- **Climate**: NOAA, FEMA flood maps
- **Crime**: FBI UCR, local police data
- **Economic**: Census Bureau, BLS

### 2. Feature Engineering
Add more relevant features:
- Distance to fire stations
- School quality scores
- Property tax rates
- Historical price trends

### 3. Hyperparameter Tuning
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 15],
    'learning_rate': [0.01, 0.1, 0.3]
}

grid_search = GridSearchCV(model, param_grid, cv=5)
grid_search.fit(X_train, y_train)
```

### 4. Cross-Validation
```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5)
print(f"CV Score: {scores.mean():.4f} (+/- {scores.std():.4f})")
```

## 🎯 Next Steps

1. ✅ Train models with synthetic data (done)
2. 📊 Collect real datasets
3. 🔧 Fine-tune hyperparameters
4. 📈 Add more features
5. 🚀 Deploy updated models to production
6. 📊 Monitor model performance
7. 🔄 Retrain periodically with new data

## 📚 Resources

- **Scikit-learn**: https://scikit-learn.org/
- **NOAA Climate Data**: https://www.ncdc.noaa.gov/
- **FBI Crime Data**: https://ucr.fbi.gov/
- **Census Bureau**: https://data.census.gov/

## 🐛 Troubleshooting

### Issue: scikit-learn won't install
**Solution**: Use Python 3.11 or 3.12
```bash
python --version  # Check version
# If needed, create new venv with Python 3.11
python3.11 -m venv venv
```

### Issue: Model file not found
**Solution**: Ensure training script runs successfully and creates the .pkl file

### Issue: Poor model performance
**Solution**: 
1. Collect more/better training data
2. Add relevant features
3. Try different algorithms
4. Tune hyperparameters
''',

    # ==================== FRONTEND ENV EXAMPLE ====================
    r'frontend\.env.example': r'''# Mapbox (get free token at https://account.mapbox.com/)
VITE_MAPBOX_TOKEN=your_mapbox_token_here

# Backend API URL
VITE_API_URL=http://localhost:8000

# OpenWeatherMap (optional, for weather widget)
VITE_OPENWEATHER_API_KEY=your_openweather_key_here
''',

    # ==================== QUICK START GUIDE ====================
    r'QUICKSTART.md': r'''# 🚀 Quick Start Guide

## Complete Setup in 5 Minutes

### 1. Clone & Navigate
```bash
cd "real-estate risks scorer"
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
uvicorn app.main:app --reload
```

✅ Backend running at: http://localhost:8000

### 3. Frontend Setup (New Terminal)
```bash
cd frontend
npm install

# Optional: Add Mapbox for interactive maps
npm install mapbox-gl @types/mapbox-gl

npm run dev
```

✅ Frontend running at: http://localhost:5173

### 4. Get API Keys (Optional but Recommended)

#### Mapbox (Free - Interactive Maps)
1. Sign up: https://account.mapbox.com/
2. Copy your token
3. Create `frontend/.env`:
```
VITE_MAPBOX_TOKEN=pk.ey...your_token
```

#### OpenWeatherMap (Free - Weather Widget)
1. Sign up: https://openweathermap.org/api
2. Get API key
3. Add to `frontend/.env`:
```
VITE_OPENWEATHER_API_KEY=your_key
```

### 5. Test the Application

1. Open http://localhost:5173
2. Click "Get Started" or "Try Demo"
3. Search for an address or use coordinates
4. View risk assessment with interactive map!

## 📊 Train ML Models (Optional)

```bash
cd ml/training

# Climate risk model
python train_climate_model.py

# Crime risk model  
python train_crime_model.py
```

## 🎯 Key Features to Try

1. **Risk Assessment**
   - POST to http://localhost:8000/api/risk-assessment/analyze
   - Body: `{"address": "1600 Amphitheatre Parkway, Mountain View, CA"}`

2. **Weather Data**
   - GET http://localhost:8000/api/weather/37.7749/-122.4194

3. **API Documentation**
   - Visit http://localhost:8000/docs
   - Interactive Swagger UI

## 🚀 Deploy to Production

### Render.com (Recommended - Free)
1. Push code to GitHub
2. Connect repository to Render
3. Render auto-detects `render.yaml`
4. Deploy with one click!

### Docker
```bash
docker-compose up -d
```

## 📚 Next Steps

- [ ] Customize UI colors/branding
- [ ] Add user authentication
- [ ] Connect to PostgreSQL database
- [ ] Collect real training data
- [ ] Deploy to production
- [ ] Set up monitoring

## 🆘 Need Help?

- **Backend Issues**: Check http://localhost:8000/docs
- **Frontend Issues**: Check browser console (F12)
- **ML Issues**: See `ml/README.md`
- **Deployment**: See `docs/DEPLOYMENT.md`

## 💡 Pro Tips

1. **Fast Reload**: Both servers auto-reload on code changes
2. **API Testing**: Use Swagger UI at /docs
3. **Debug Mode**: Check terminal logs for errors
4. **Environment Variables**: Use `.env` files (don't commit!)

🎉 **You're all set! Start building amazing features!**
''',

    # ==================== DEPLOYMENT GUIDE ====================
    r'docs\DEPLOYMENT.md': r'''# 🚀 Deployment Guide

## Option 1: Render.com (Recommended - Free Tier)

### Prerequisites
- GitHub account
- Render account (free)
- Push code to GitHub repository

### Steps

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/real-estate-risk-scorer.git
git push -u origin main
```

2. **Connect to Render**
- Visit https://render.com/
- Click "New +" → "Blueprint"
- Connect your GitHub repository
- Render will detect `render.yaml`
- Click "Apply"

3. **Configure Environment Variables**
- Backend:
  - `SECRET_KEY`: Auto-generated
  - `DATABASE_URL`: Auto-configured
  - `OPENWEATHER_API_KEY`: (optional)
- Frontend:
  - `VITE_API_URL`: https://your-backend.onrender.com
  - `VITE_MAPBOX_TOKEN`: Your Mapbox token

4. **Deploy!**
- Render automatically builds and deploys
- Backend: ~5 minutes
- Frontend: ~3 minutes

### Free Tier Limitations
- Backend sleeps after 15 min inactivity (wakes in ~30s)
- PostgreSQL 256MB storage
- 100 GB bandwidth/month
- Perfect for demos and MVPs!

## Option 2: Docker (Local/Self-Hosted)

### Prerequisites
- Docker Desktop installed
- Docker Compose installed

### Steps

1. **Build and Run**
```bash
docker-compose up -d
```

2. **Access Services**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

3. **View Logs**
```bash
docker-compose logs -f
```

4. **Stop Services**
```bash
docker-compose down
```

## Option 3: Vercel (Frontend) + Railway (Backend)

### Vercel (Frontend)
1. Visit https://vercel.com/
2. Import GitHub repository
3. Set Root Directory: `frontend`
4. Add Environment Variables:
   - `VITE_API_URL`
   - `VITE_MAPBOX_TOKEN`
5. Deploy!

### Railway (Backend)
1. Visit https://railway.app/
2. "New Project" → GitHub Repo
3. Add PostgreSQL service
4. Add Redis service
5. Configure environment variables
6. Deploy!

## Environment Variables Reference

### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/db
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs
OPENWEATHER_API_KEY=your-key

# Environment
ENVIRONMENT=production
DEBUG=False
```

### Frontend (.env)
```bash
# API
VITE_API_URL=https://your-backend-url.com

# Mapbox
VITE_MAPBOX_TOKEN=pk.ey...your_token

# Weather
VITE_OPENWEATHER_API_KEY=your_key
```

## Post-Deployment Checklist

- [ ] Test all API endpoints
- [ ] Verify database connections
- [ ] Check frontend loads correctly
- [ ] Test user authentication
- [ ] Verify risk assessment works
- [ ] Check weather widget
- [ ] Test PDF generation
- [ ] Monitor error logs
- [ ] Set up backups
- [ ] Configure custom domain

## Monitoring & Maintenance

### Health Checks
- Backend: `GET /health`
- Database: Check connection pool
- Redis: Monitor cache hit rate

### Logging
```bash
# Render
render logs -t <service-name>

# Docker
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Backups
- Database: Daily automated backups (Render/Railway)
- Code: GitHub repository
- Models: Store trained models in S3/Cloud Storage

## Troubleshooting

### Issue: Backend timeout
**Solution**: Upgrade to paid plan or use keepalive service

### Issue: Database full
**Solution**: Implement data retention policy or upgrade storage

### Issue: CORS errors
**Solution**: Update CORS origins in `app/main.py`

### Issue: Missing environment variables
**Solution**: Double-check all required vars are set

## Scaling

### Traffic Growth
1. Upgrade to paid tier
2. Enable auto-scaling
3. Add CDN for frontend
4. Implement caching strategy

### Database Optimization
1. Add indexes on frequently queried columns
2. Use connection pooling
3. Implement read replicas
4. Archive old data

### API Performance
1. Implement rate limiting
2. Add Redis caching
3. Use background workers for ML
4. Optimize query performance

## Cost Estimates

### Free Tier (Perfect for MVP)
- Render: $0/month (with limitations)
- Vercel: $0/month
- Railway: $5/month (with trial credits)

### Production (Low Traffic)
- Render: $7-25/month
- Railway: $20-50/month
- Total: ~$30-75/month

### Production (High Traffic)
- Backend: $50-200/month
- Database: $25-100/month
- CDN: $20-50/month
- Total: ~$100-350/month

## Security Best Practices

1. ✅ Never commit `.env` files
2. ✅ Use strong SECRET_KEY
3. ✅ Enable HTTPS only
4. ✅ Implement rate limiting
5. ✅ Sanitize user inputs
6. ✅ Keep dependencies updated
7. ✅ Use environment-specific configs
8. ✅ Monitor security alerts

## Support

For deployment issues:
1. Check service status pages
2. Review deployment logs
3. Verify environment variables
4. Test locally first
5. Contact platform support

🚀 **Happy Deploying!**
''',
}

for filepath, content in files.items():
    dirname = os.path.dirname(filepath)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Created: {filepath}")

print("\n" + "="*70)
print("🎉 PART 7 COMPLETE! Mapbox, ML Guide, Deployment docs added!")
print("="*70)
print("\n📦 What was added:")
print("  ✅ Mapbox interactive map component")
print("  ✅ ML training README with detailed guide")
print("  ✅ Frontend .env.example for API keys")
print("  ✅ QUICKSTART.md for 5-minute setup")
print("  ✅ Complete DEPLOYMENT.md guide")
print("\n🗺️ To add Mapbox maps:")
print("  1. cd frontend && npm install mapbox-gl @types/mapbox-gl")
print("  2. Get free token: https://account.mapbox.com/")
print("  3. Add VITE_MAPBOX_TOKEN to frontend/.env")
print("  4. Replace PropertyDetail.tsx with PropertyDetailUpdated.tsx")
print("\n🤖 To train ML models:")
print("  1. Use Python 3.11 (scikit-learn not yet on 3.13)")
print("  2. cd ml/training")
print("  3. python train_climate_model.py")
print("\n🚀 Ready to deploy to Render, Vercel, or Docker!")

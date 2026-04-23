# 🚀 Quick Start Guide

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
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

✅ Backend running at: http://localhost:8001

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
   - POST to http://localhost:8001/api/risk-assessment/analyze
   - Body: `{"address": "1600 Amphitheatre Parkway, Mountain View, CA"}`

2. **Weather Data**
   - GET http://localhost:8001/api/weather/37.7749/-122.4194

3. **API Documentation**
   - Visit http://localhost:8001/docs
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

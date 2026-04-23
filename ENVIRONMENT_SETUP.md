# Environment Variables Configuration Guide

## Frontend Environment Variables

### For Local Development (frontend/.env)
```env
VITE_API_URL=http://localhost:8001
VITE_OPENWEATHER_API_KEY=your_optional_key_here
```

### For Production/Netlify (Configure in Netlify Dashboard)
```env
VITE_API_URL=https://your-backend-url.onrender.com
VITE_OPENWEATHER_API_KEY=your_optional_key_here
```

**How to set in Netlify:**
1. Go to Site settings → Environment variables
2. Add each variable with Key-Value pairs
3. Click "Save"
4. Trigger a new deployment

---

## Backend Environment Variables

### For Local Development (backend/.env)
```env
DATABASE_URL=sqlite:///./real_estate_risk_scorer.db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-change-this-in-production
OPENWEATHER_API_KEY=your_openweather_api_key
CORS_ALLOW_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### For Production (Render/Railway)
```env
# Database (Render provides PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/database

# Redis (Render provides Redis)
REDIS_URL=redis://host:6379

# Security - Generate a strong secret key
SECRET_KEY=your-very-secure-random-secret-key-here

# Weather API (optional)
OPENWEATHER_API_KEY=your_api_key_here

# CORS - Add your Netlify domain
CORS_ALLOW_ORIGINS=https://your-site-name.netlify.app,https://your-custom-domain.com

# Server configuration
PORT=8001
HOST=0.0.0.0
```

---

## Generating Secure SECRET_KEY

Run this in Python:
```python
import secrets
print(secrets.token_urlsafe(32))
```

Or use OpenSSL:
```bash
openssl rand -base64 32
```

---

## CORS Configuration

The backend is configured to read CORS origins from `CORS_ALLOW_ORIGINS` environment variable.

**Important:** After deploying frontend to Netlify, update backend environment:
```env
CORS_ALLOW_ORIGINS=https://your-netlify-site.netlify.app
```

---

## Optional API Keys

### OpenWeatherMap (For Weather Widget)
1. Sign up at https://openweathermap.org/api
2. Free tier: 1,000 calls/day
3. Add to both frontend and backend .env files

### Mapbox (Optional - Project uses free OpenStreetMap)
Not required! The project uses free Leaflet + OpenStreetMap instead.

---

## Database Setup for Production

### Using PostgreSQL (Recommended for Production)

1. **On Render.com:**
   - Create a new PostgreSQL database
   - Copy the Internal Database URL
   - Add to backend environment as `DATABASE_URL`

2. **Database Migration:**
   ```bash
   # The app will auto-create tables on startup
   # Or use Alembic for migrations:
   cd backend
   alembic upgrade head
   ```

### Using SQLite (Development Only)
SQLite file is already configured for local development. For production, switch to PostgreSQL.

---

## Verification Checklist

- [ ] Frontend .env configured for local development
- [ ] Backend .env configured for local development
- [ ] Both services start without errors locally
- [ ] Frontend can communicate with backend (API calls work)
- [ ] Production environment variables prepared for deployment
- [ ] SECRET_KEY generated (strong random string)
- [ ] CORS_ALLOW_ORIGINS includes production frontend URL

---

## Testing Environment Configuration

Test that environment variables are loaded correctly:

### Frontend Test:
```bash
cd frontend
npm run dev
# Open browser console and check:
# console.log(import.meta.env.VITE_API_URL)
```

### Backend Test:
```bash
cd backend
python -c "from app.core.config import settings; print(f'API URL: {settings.DATABASE_URL}')"
```

---

## Quick Reference

| Variable | Frontend | Backend | Required | Default |
|----------|----------|---------|----------|---------|
| VITE_API_URL | ✅ | ❌ | Yes | http://127.0.0.1:8001 |
| DATABASE_URL | ❌ | ✅ | Yes | sqlite:///./real_estate_risk_scorer.db |
| REDIS_URL | ❌ | ✅ | No | redis://localhost:6379 |
| SECRET_KEY | ❌ | ✅ | Yes | (must be set) |
| OPENWEATHER_API_KEY | ✅ | ✅ | No | None |
| CORS_ALLOW_ORIGINS | ❌ | ✅ | No | localhost:5173 |

---

Need help? Check NETLIFY_DEPLOYMENT.md for deployment instructions.

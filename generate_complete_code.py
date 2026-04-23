"""Complete Real Estate Risk Scorer Code Generator"""

import os
from pathlib import Path

def write_file(filepath, content):
    """Write content to file, creating directories as needed"""
    p = Path(filepath)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.strip(), encoding='utf-8')
    print(f"✓ Generated: {filepath}")

# Dictionary of files to generate
files = {}

# ROOT FILES
files['docker-compose.yml'] = r'''version: '3.8'

services:
  postgres:
    image: postgis/postgis:15-3.3
    container_name: realestate-postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: realestate_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: realestate-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  backend:
    build: ./backend
    container_name: realestate-backend
    environment: 
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/realestate_db
      - REDIS_URL=redis://redis:6379/0
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    depends_on:
      - postgres
      - redis
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    container_name: realestate-frontend
    environment:
      - VITE_API_URL=http://localhost:8000
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - backend

volumes:
  postgres_data: 
  redis_data:
'''

files['.gitignore'] = r'''__pycache__/
*.pyc
venv/
env/
node_modules/
dist/
.env
.env.local
*.log
.DS_Store
*.db
.pytest_cache/
.coverage
'''

files['README.md'] = r'''# Real Estate Risk Scorer

AI-powered real estate investment risk analysis platform.

## Features
- Geospatial Analysis
- Climate Risk Assessment
- Crime Data Integration
- Economic Indicators
- Infrastructure Scoring

## Quick Start

```bash
docker-compose up --build
```

Visit:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/docs
'''

# BACKEND FILES
files['backend/Dockerfile'] = r'''FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
'''

files['backend/requirements.txt'] = r'''fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
requests==2.31.0
pandas==2.1.3
numpy==1.26.2
scikit-learn==1.3.2
pytest==7.4.3
'''

files['backend/.env.example'] = r'''ENVIRONMENT=development
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/realestate_db
REDIS_URL=redis://localhost:6379/0
GOOGLE_MAPS_API_KEY=your-key
ALLOWED_ORIGINS=http://localhost:5173
'''

files['backend/app/main.py'] = r'''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import properties, risk_assessment, auth, reports

app = FastAPI(
    title="Real Estate Risk Scorer API",
    version="1.0.0",
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(properties.router, prefix="/api/properties", tags=["Properties"])
app.include_router(risk_assessment.router, prefix="/api/risk-assessment", tags=["Risk Assessment"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])

@app.get("/")
async def root():
    return {"message": "Real Estate Risk Scorer API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
'''

files['backend/app/core/config.py'] = r'''from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "dev-secret-key"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/realestate_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173"]
    
    class Config:
        env_file = ".env"

settings = Settings()
'''

files['backend/app/api/routes/properties.py'] = r'''from fastapi import APIRouter, Query
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

class PropertyResponse(BaseModel):
    id: str
    address: str
    latitude: float
    longitude: float
    price: Optional[float] = None

@router.get("/search", response_model=List[PropertyResponse])
async def search_properties(
    address: Optional[str] = Query(None),
    radius: float = Query(5.0)
):
    return [{
        "id": "prop_001",
        "address": "123 Main St, San Francisco, CA",
        "latitude": 37.7749,
        "longitude": -122.4194,
        "price": 1200000
    }]

@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(property_id: str):
    return {
        "id": property_id,
        "address": "123 Main St, San Francisco, CA",
        "latitude": 37.7749,
        "longitude": -122.4194,
        "price": 1200000
    }
'''

files['backend/app/api/routes/risk_assessment.py'] = r'''from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, Optional

router = APIRouter()

class RiskAssessmentRequest(BaseModel):
    property_id: Optional[str] = None
    address: Optional[str] = None
    latitude: float
    longitude: float

class RiskScore(BaseModel):
    overall_score: float
    climate_risk: float
    crime_risk: float
    economic_risk: float
    infrastructure_score: float
    details: Dict[str, Any]

@router.post("/analyze", response_model=RiskScore)
async def analyze_risk(request: RiskAssessmentRequest):
    return {
        "overall_score": 68.5,
        "climate_risk": 35.2,
        "crime_risk": 42.8,
        "economic_risk": 28.5,
        "infrastructure_score": 75.3,
        "details": {
            "climate": {"flood_zone": False, "wildfire_risk": "Low"},
            "crime": {"violent_crime_rate": 4.2, "property_crime_rate": 18.5},
            "economic": {"unemployment_rate": 3.5, "median_income": 95000},
            "infrastructure": {"transit_score": 82, "school_rating": 8}
        }
    }
'''

files['backend/app/api/routes/auth.py'] = r'''from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from jose import jwt

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "demo@example.com" or form_data.password != "demo":
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, "secret-key", algorithm="HS256")
'''

files['backend/app/api/routes/reports.py'] = r'''from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class ReportRequest(BaseModel):
    property_id: str
    include_charts: bool = True

@router.post("/generate")
async def generate_report(request: ReportRequest):
    return {
        "report_id": "rpt_001",
        "status": "generating",
        "estimated_time": 30
    }

@router.get("/{report_id}/status")
async def get_report_status(report_id: str):
    return {
        "report_id": report_id,
        "status": "completed",
        "download_url": f"/api/reports/{report_id}/download"
    }

@router.get("/{report_id}/download")
async def download_report(report_id: str):
    raise HTTPException(status_code=501, detail="Not implemented yet")
'''

files['backend/scripts/init.sql'] = r'''CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS properties (
    id SERIAL PRIMARY KEY,
    address TEXT NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    price DECIMAL(12, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS risk_assessments (
    id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES properties(id),
    overall_score DECIMAL(5, 2),
    climate_risk DECIMAL(5, 2),
    crime_risk DECIMAL(5, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''

# FRONTEND FILES
files['frontend/Dockerfile'] = r'''FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
'''

files['frontend/package.json'] = r'''{
  "name": "real-estate-risk-scorer-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.2",
    "leaflet": "^1.9.4",
    "react-leaflet": "^4.2.1",
    "recharts": "^2.10.3"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "typescript": "^5.3.3",
    "vite": "^5.0.8"
  }
}
'''

files['frontend/.env.example'] = r'''VITE_API_URL=http://localhost:8000
'''

files['frontend/vite.config.ts'] = r'''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true
  }
})
'''

files['frontend/tsconfig.json'] = r'''{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
'''

files['frontend/tsconfig.node.json'] = r'''{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
'''

files['frontend/index.html'] = r'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Real Estate Risk Scorer</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
'''

files['frontend/src/main.tsx'] = r'''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
'''

files['frontend/src/App.tsx'] = r'''import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import PropertyDetail from './pages/PropertyDetail'
import Dashboard from './pages/Dashboard'
import Login from './pages/Login'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/property/:id" element={<PropertyDetail />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
'''

files['frontend/src/index.css'] = r'''* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
'''

files['frontend/src/pages/Home.tsx'] = r'''import { useState } from 'react'

export default function Home() {
  const [address, setAddress] = useState('')

  const handleSearch = async () => {
    console.log('Searching for:', address)
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>Real Estate Risk Scorer</h1>
      <div style={{ marginTop: '20px' }}>
        <input
          type="text"
          placeholder="Enter property address..."
          value={address}
          onChange={(e) => setAddress(e.target.value)}
          style={{ padding: '10px', width: '300px', marginRight: '10px' }}
        />
        <button onClick={handleSearch} style={{ padding: '10px 20px' }}>
          Search
        </button>
      </div>
    </div>
  )
}
'''

files['frontend/src/pages/PropertyDetail.tsx'] = r'''export default function PropertyDetail() {
  return <div><h1>Property Detail Page</h1></div>
}
'''

files['frontend/src/pages/Dashboard.tsx'] = r'''export default function Dashboard() {
  return <div><h1>Dashboard Page</h1></div>
}
'''

files['frontend/src/pages/Login.tsx'] = r'''export default function Login() {
  return <div><h1>Login Page</h1></div>
}
'''

files['frontend/src/services/api.ts'] = r'''import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000'
})

export default api
'''

# Generate all files
for filepath, content in files.items():
    write_file(filepath, content)

print("\n" + "="*60)
print("✅ CODE GENERATION COMPLETE!")
print("="*60)
print(f"\nGenerated {len(files)} files")
print("\nNext steps:")
print("  1. Copy backend/.env.example to backend/.env")
print("  2. Copy frontend/.env.example to frontend/.env")
print("  3. Run: docker-compose up --build")
print("  4. Visit http://localhost:5173")

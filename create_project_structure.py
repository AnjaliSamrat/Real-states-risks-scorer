import os
from pathlib import Path

def ensure_dir(p):
    os.makedirs(p, exist_ok=True)

# Root directories and substructure
directories = [
    "backend/app/api/routes",
    "backend/app/api/middleware",
    "backend/app/core",
    "backend/app/models/trained",
    "backend/app/services",
    "backend/app/utils",
    "backend/tests/test_api",
    "backend/tests/test_core",
    "backend/tests/test_services",
    "backend/alembic",
    "backend/scripts",
    "frontend/public",
    "frontend/src/components/Map",
    "frontend/src/components/Search",
    "frontend/src/components/Dashboard",
    "frontend/src/components/Reports",
    "frontend/src/pages",
    "frontend/src/hooks",
    "frontend/src/services",
    "frontend/src/store",
    "frontend/src/types",
    "frontend/src/utils",
    "ml/notebooks",
    "ml/training",
    "ml/data",
    "infrastructure/terraform",
    "infrastructure/kubernetes",
    "infrastructure/monitoring",
    "docs",
    ".github/workflows",
]

for d in directories:
    ensure_dir(d)

# Python package __init__ files for backend
python_packages = [
    "backend/app/__init__.py",
    "backend/app/api/__init__.py",
    "backend/app/api/routes/__init__.py",
    "backend/app/api/middleware/__init__.py",
    "backend/app/core/__init__.py",
    "backend/app/models/__init__.py",
    "backend/app/services/__init__.py",
    "backend/app/utils/__init__.py",
    "backend/tests/__init__.py",
]

for p in python_packages:
    Path(p).write_text("# package init\n")

# placeholder files mapping
placeholders = {
    "backend/app/main.py": "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef root():\n    return {'status':'ok'}\n",
    "backend/app/config.py": "# Environment configuration\n",
    "backend/app/dependencies.py": "# Dependency injection container\n",
    "backend/app/api/routes/properties.py": "# Properties routes\n",
    "backend/app/api/routes/risk_assessment.py": "# Risk assessment routes\n",
    "backend/app/api/routes/auth.py": "# Authentication routes\n",
    "backend/app/api/routes/reports.py": "# Reports routes\n",
    "backend/app/api/middleware/auth.py": "# Authentication middleware\n",
    "backend/app/api/middleware/rate_limit.py": "# Rate limiting middleware\n",
    "backend/app/core/risk_engine.py": "# Main risk scoring logic\n",
    "backend/app/core/data_fetcher.py": "# External API calls\n",
    "backend/app/core/ml_models.py": "# ML model predictions\n",
    "backend/app/core/pdf_generator.py": "# Report generation\n",
    "backend/app/models/database.py": "# SQLAlchemy models\n",
    "backend/app/models/schemas.py": "# Pydantic schemas\n",
    "backend/app/services/climate_service.py": "# Climate data service\n",
    "backend/app/services/crime_service.py": "# Crime data service\n",
    "backend/app/services/economic_service.py": "# Economic data service\n",
    "backend/app/services/cache_service.py": "# Caching service\n",
    "backend/app/utils/geocoding.py": "# Geocoding utilities\n",
    "backend/app/utils/spatial.py": "# Spatial data utilities\n",
    "backend/app/utils/validators.py": "# Data validators\n",
    "backend/tests/test_api/test_routes.py": "# tests for API routes\n",
    "backend/tests/test_core/test_risk_engine.py": "# tests for core logic\n",
    "backend/tests/test_services/test_services.py": "# tests for services\n",
    "backend/requirements.txt": "fastapi\nuvicorn\nrequests\nSQLAlchemy\n",
    "backend/Dockerfile": "# Backend Dockerfile placeholder\n",
    "backend/docker-compose.yml": "# Docker compose for backend and dependencies\n",
    "frontend/package.json": "{\n  \"name\": \"frontend\",\n  \"version\": \"0.0.1\",\n  \"private\": true\n}\n",
    "frontend/tsconfig.json": "{\n  \"compilerOptions\": {}\n}\n",
    "frontend/vite.config.ts": "// Vite config placeholder\n",
    "frontend/Dockerfile": "# Frontend Dockerfile placeholder\n",
    "frontend/src/components/Map/PropertyMap.tsx": "// Property map component\n",
    "frontend/src/components/Map/RiskLayersControl.tsx": "// Risk layers control\n",
    "frontend/src/components/Search/AddressSearch.tsx": "// Address search component\n",
    "frontend/src/components/Dashboard/RiskScoreCard.tsx": "// Risk score card\n",
    "frontend/src/components/Dashboard/ClimateChart.tsx": "// Climate chart\n",
    "frontend/src/components/Dashboard/TrendGraph.tsx": "// Trend graph\n",
    "frontend/src/components/Reports/PDFViewer.tsx": "// PDF viewer component\n",
    "frontend/src/pages/Home.tsx": "// Home page\n",
    "frontend/src/pages/PropertyDetail.tsx": "// Property detail page\n",
    "frontend/src/pages/Dashboard.tsx": "// Dashboard page\n",
    "frontend/src/pages/Login.tsx": "// Login page\n",
    "frontend/src/hooks/usePropertySearch.ts": "// Property search hook\n",
    "frontend/src/hooks/useRiskAssessment.ts": "// Risk assessment hook\n",
    "frontend/src/services/api.ts": "// API client\n",
    "frontend/src/types/index.ts": "// TypeScript types\n",
    "ml/notebooks/data_exploration.ipynb": "{}",
    "ml/notebooks/model_training.ipynb": "{}",
    "ml/training/train_climate_model.py": "# Climate model training\n",
    "ml/training/train_crime_model.py": "# Crime model training\n",
    "ml/data/README.md": "# training datasets\n",
    "docs/API.md": "# API Documentation\n",
    "docs/DEPLOYMENT.md": "# Deployment Guide\n",
    "docs/CONTRIBUTING.md": "# Contributing Guide\n",
    ".github/workflows/ci.yml": "# CI pipeline\n",
    ".github/workflows/deploy.yml": "# Deploy workflow\n",
    "README.md": "# Real Estate Risk Scorer\n",
    ".gitignore": "venv/\n__pycache__/\n*.pyc\nnode_modules/\n",
    "LICENSE": "MIT License\n",
    "ROADMAP.md": "# Project Roadmap\n",
}

for path, content in placeholders.items():
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding='utf-8')

print('Project scaffold script created at:')
print(Path(__file__).resolve())

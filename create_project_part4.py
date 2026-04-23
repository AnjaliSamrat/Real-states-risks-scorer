"""
PART 4: Frontend Application Base
"""
import os

files = {
    # ==================== FRONTEND CONFIGURATION ====================
    'frontend/package.json': r'''{
  "name": "real-estate-risk-scorer",
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.2",
    "@tanstack/react-query": "^5.12.2",
    "lucide-react": "^0.294.0",
    "recharts": "^2.10.3",
    "clsx": "^2.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@typescript-eslint/eslint-plugin": "^6.14.0",
    "@typescript-eslint/parser": "^6.14.0",
    "@vitejs/plugin-react": "^4.2.1",
    "typescript": "^5.2.2",
    "vite": "^5.0.8",
    "eslint": "^8.55.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.3.6"
  }
}
''',

    'frontend/vite.config.ts': r'''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    host: true,
    port: 5173,
    watch: {
      usePolling: true,
    },
  },
})
''',

    'frontend/tailwind.config.js': r'''/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        risk: {
          'very-low': '#10b981',
          'low': '#84cc16',
          'moderate': '#eab308',
          'high': '#f97316',
          'very-high': '#ef4444',
        }
      }
    },
  },
  plugins: [],
}
''',

    'frontend/postcss.config.js': r'''export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
''',

    'frontend/src/index.css': r'''@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-white text-gray-900;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
      'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
      sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
}

.risk-gauge {
  transition: all 0.3s ease-in-out;
}
''',

    'frontend/src/main.tsx': r'''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
''',

    'frontend/src/App.tsx': r'''import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import Home from './pages/Home'
import PropertyDetail from './pages/PropertyDetail'
import Dashboard from './pages/Dashboard'
import Login from './pages/Login'
import Layout from './components/Layout'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="property/:id" element={<PropertyDetail />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="login" element={<Login />} />
          </Route>
        </Routes>
      </Router>
    </QueryClientProvider>
  )
}

export default App
''',

    # ==================== TYPES ====================
    'frontend/src/types/index.ts': r'''export interface Property {
  id: number
  address: string
  latitude: number
  longitude: number
  price?: number
  bedrooms?: number
  bathrooms?: number
  square_feet?: number
  year_built?: number
  property_type?: string
  created_at: string
}

export interface RiskAssessment {
  id: number
  property_id: number
  climate_score: number
  crime_score: number
  economic_score: number
  infrastructure_score: number
  overall_score: number
  risk_level?: string
  climate_data?: any
  crime_data?: any
  economic_data?: any
  infrastructure_data?: any
  assessment_date: string
}

export interface User {
  id: number
  email: string
  full_name?: string
  is_premium: boolean
}
''',

    # ==================== API SERVICE ====================
    'frontend/src/services/api.ts': r'''import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const propertyApi = {
  search: (params: any) => api.get('/properties/search', { params }),
  getById: (id: number) => api.get(`/properties/${id}`),
  create: (data: any) => api.post('/properties', data),
}

export const riskApi = {
  analyze: (data: any) => api.post('/risk-assessment/analyze', data),
  getLatest: (propertyId: number) => api.get(`/risk/${propertyId}/latest`),
}

export const authApi = {
  login: (username: string, password: string) => 
    api.post('/auth/login', new URLSearchParams({ username, password }), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }),
  register: (data: any) => api.post('/auth/register', data),
}
''',

    # ==================== COMPONENTS ====================
    'frontend/src/components/Layout.tsx': r'''import { Outlet, Link, useLocation } from 'react-router-dom'
import { Home, BarChart3, LogIn, Menu } from 'lucide-react'
import { useState } from 'react'

export default function Layout() {
  const location = useLocation()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const navigation = [
    { name: 'Home', href: '/', icon: Home },
    { name: 'Dashboard', href: '/dashboard', icon: BarChart3 },
    { name: 'Login', href: '/login', icon: LogIn },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <nav className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 justify-between items-center">
            <div className="flex items-center">
              <Link to="/" className="flex items-center space-x-2">
                <div className="h-8 w-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                  <Home className="h-5 w-5 text-white" />
                </div>
                <span className="text-xl font-bold text-gray-900">
                  RiskScorer
                </span>
              </Link>
            </div>

            <div className="hidden md:flex md:space-x-8">
              {navigation.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.href
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`inline-flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                      isActive
                        ? 'text-blue-600 bg-blue-50'
                        : 'text-gray-700 hover:text-blue-600 hover:bg-gray-50'
                    }`}
                  >
                    <Icon className="h-4 w-4 mr-2" />
                    {item.name}
                  </Link>
                )
              })}
            </div>

            <div className="md:hidden">
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="p-2 rounded-md text-gray-700 hover:bg-gray-100"
              >
                <Menu className="h-6 w-6" />
              </button>
            </div>
          </div>

          {mobileMenuOpen && (
            <div className="md:hidden py-4 space-y-2">
              {navigation.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.href
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    onClick={() => setMobileMenuOpen(false)}
                    className={`flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                      isActive
                        ? 'text-blue-600 bg-blue-50'
                        : 'text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    <Icon className="h-4 w-4 mr-2" />
                    {item.name}
                  </Link>
                )
              })}
            </div>
          )}
        </nav>
      </header>

      <main>
        <Outlet />
      </main>

      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
          <p className="text-center text-sm text-gray-500">
            © 2025 Real Estate Risk Scorer. Built with ❤️ for smarter investments.
          </p>
        </div>
      </footer>
    </div>
  )
}
''',

    'frontend/src/pages/Home.tsx': r'''import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, Shield, TrendingUp, MapPin } from 'lucide-react'

export default function Home() {
  const [address, setAddress] = useState('')
  const navigate = useNavigate()

  const features = [
    {
      icon: Shield,
      title: 'Climate Risk Analysis',
      description: 'Assess flood zones, wildfire risk, sea level rise, and earthquake hazards',
    },
    {
      icon: TrendingUp,
      title: 'Economic Indicators',
      description: 'Track employment, income trends, and local economic health',
    },
    {
      icon: MapPin,
      title: 'Crime & Safety',
      description: 'Understand crime patterns and neighborhood safety trends',
    },
  ]

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (address.trim()) {
      navigate('/property/1')
    }
  }

  return (
    <div className="bg-gradient-to-b from-blue-50 to-white">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
            Make Smarter Real Estate
            <span className="text-blue-600"> Investments</span>
          </h1>
          <p className="mt-6 text-lg leading-8 text-gray-600 max-w-2xl mx-auto">
            AI-powered risk analysis combining climate data, crime statistics, 
            and economic indicators to help you invest with confidence.
          </p>

          <form onSubmit={handleSearch} className="mt-10 max-w-xl mx-auto">
            <div className="relative">
              <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4">
                <Search className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                placeholder="Enter property address..."
                className="block w-full rounded-lg border border-gray-300 bg-white py-4 pl-12 pr-32 text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              />
              <div className="absolute inset-y-0 right-0 flex items-center pr-2">
                <button
                  type="submit"
                  className="inline-flex items-center px-6 py-2 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700 transition-colors"
                >
                  Analyze
                </button>
              </div>
            </div>
          </form>

          <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-3 max-w-3xl mx-auto">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="text-3xl font-bold text-blue-600">10+</div>
              <div className="text-sm text-gray-600 mt-2">Data Sources</div>
            </div>
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="text-3xl font-bold text-blue-600">4</div>
              <div className="text-sm text-gray-600 mt-2">Risk Categories</div>
            </div>
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="text-3xl font-bold text-blue-600">30yr</div>
              <div className="text-sm text-gray-600 mt-2">Projections</div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-gray-900">
              Comprehensive Risk Analysis
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              Everything you need to evaluate investment properties
            </p>
          </div>

          <div className="mt-16 grid grid-cols-1 gap-8 md:grid-cols-3">
            {features.map((feature) => {
              const Icon = feature.icon
              return (
                <div
                  key={feature.title}
                  className="bg-gray-50 rounded-xl p-8 hover:shadow-lg transition-shadow"
                >
                  <div className="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <Icon className="h-6 w-6 text-blue-600" />
                  </div>
                  <h3 className="mt-6 text-xl font-semibold text-gray-900">
                    {feature.title}
                  </h3>
                  <p className="mt-2 text-gray-600">
                    {feature.description}
                  </p>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      <div className="bg-blue-600 py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white">
            Ready to analyze your first property?
          </h2>
          <p className="mt-4 text-lg text-blue-100">
            Get started for free - no credit card required
          </p>
          <button
            onClick={() => document.querySelector('input')?.focus()}
            className="mt-8 px-8 py-3 bg-white text-blue-600 font-semibold rounded-lg hover:bg-blue-50 transition-colors"
          >
            Search Properties
          </button>
        </div>
      </div>
    </div>
  )
}
''',
}

for filepath, content in files.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Created: {filepath}")

print("\n" + "="*70)
print("🎉 PART 4 COMPLETE! Frontend base created!")
print("="*70)
print("\nNext: Install dependencies with 'npm install' in frontend/")

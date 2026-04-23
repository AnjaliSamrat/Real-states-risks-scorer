# 🗺️ Mapbox Interactive Maps - Quick Setup

## ✅ Already Installed
- ✅ Mapbox GL JS (v3.x)
- ✅ TypeScript types (@types/mapbox-gl)
- ✅ PropertyMap component created
- ✅ PropertyDetail page updated

## 🚀 Quick Setup (2 minutes)

### Option 1: Automated Setup
```powershell
.\setup_mapbox.ps1
```

### Option 2: Manual Setup

#### 1. Get Mapbox Token (FREE)
1. Go to: https://account.mapbox.com/auth/signup/
2. Sign up with email (free tier includes 50,000 map loads/month)
3. Verify email
4. Get token: https://account.mapbox.com/access-tokens/
5. Copy your **Default Public Token** (starts with `pk.`)

#### 2. Create .env File
```powershell
cd frontend
```

Create `frontend/.env`:
```env
VITE_MAPBOX_TOKEN=pk.YOUR_TOKEN_HERE
VITE_API_URL=http://localhost:8000
```

#### 3. Restart Frontend
```powershell
npm run dev
```

## 🎨 Map Features

### Risk-Based Colors
- 🟢 **Green** (0-20): Very Low Risk
- 🟡 **Lime** (21-40): Low Risk  
- 🟠 **Yellow** (41-60): Moderate Risk
- 🔴 **Orange** (61-80): High Risk
- ⚫ **Red** (81-100): Very High Risk

### Interactive Elements
- **Custom markers** with pulse animation
- **Popup** with property details & risk score
- **Risk radius circle** (size based on risk level)
- **Navigation controls** (zoom, rotate, pitch)
- **Fullscreen mode**
- **3D buildings** (pitch: 45°)

## 📍 Test the Map

### View a Property
1. Start both servers:
   ```powershell
   # Terminal 1: Backend
   cd backend
   .\venv\Scripts\activate
   uvicorn app.main:app --reload

   # Terminal 2: Frontend
   cd frontend
   npm run dev
   ```

2. Open: http://localhost:5173

3. Navigate to any property page (or use the search)

4. You should see:
   - Interactive Mapbox map
   - Colored marker based on risk score
   - Popup opens automatically
   - Risk radius circle
   - Navigation controls

### Test Different Locations
```powershell
# Create test properties
$cities = @(
    @{ address = "Empire State Building, New York"; price = 5000000; latitude = 40.7484; longitude = -73.9857 },
    @{ address = "Golden Gate Bridge, San Francisco"; price = 3500000; latitude = 37.8199; longitude = -122.4783 },
    @{ address = "Space Needle, Seattle"; price = 2500000; latitude = 47.6205; longitude = -122.3493 }
)

foreach ($city in $cities) {
    $body = $city | ConvertTo-Json
    Invoke-RestMethod -Uri "http://localhost:8000/api/properties" `
        -Method POST -Body $body -ContentType "application/json"
}
```

## 🔧 Troubleshooting

### Map Not Showing?
1. **Check .env file exists**: `frontend/.env`
2. **Verify token**: Should start with `pk.`
3. **Restart frontend**: Stop (Ctrl+C) and run `npm run dev` again
4. **Check browser console**: F12 → Console tab

### "Map requires Mapbox token" Message?
- Token not in `.env` file or incorrect format
- Create `frontend/.env` with `VITE_MAPBOX_TOKEN=pk.your_token`
- Restart frontend

### Map Shows Gray Box?
- Invalid or expired token
- Get a new token from https://account.mapbox.com/access-tokens/

### Network Error?
- Check your internet connection
- Mapbox requires internet to load map tiles

## 📚 Map Component Usage

```typescript
import PropertyMap from '@/components/Map/PropertyMap'

<PropertyMap
  latitude={40.7484}
  longitude={-73.9857}
  address="Empire State Building"
  riskScore={65}  // Optional: 0-100
/>
```

## 🎯 Success Checklist

- [ ] Mapbox account created (free)
- [ ] Token copied (starts with `pk.`)
- [ ] `.env` file created in `frontend/`
- [ ] Token added to `.env`
- [ ] Frontend restarted
- [ ] Map visible on property pages
- [ ] Markers showing with correct colors
- [ ] Popup opens automatically
- [ ] Navigation controls working
- [ ] Risk radius circle visible (when risk score present)

## 🆓 Free Tier Limits

Mapbox free tier includes:
- ✅ 50,000 map loads per month
- ✅ All map styles
- ✅ Navigation controls
- ✅ Custom markers & popups
- ✅ No credit card required for signup

Perfect for development and small projects!

## 🔗 Resources

- Mapbox Signup: https://account.mapbox.com/auth/signup/
- Get Token: https://account.mapbox.com/access-tokens/
- Mapbox Docs: https://docs.mapbox.com/mapbox-gl-js/
- Map Styles: https://docs.mapbox.com/api/maps/styles/

---

**Need Help?** Run `.\setup_mapbox.ps1` for guided setup!

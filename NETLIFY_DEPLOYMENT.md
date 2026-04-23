# Netlify Deployment Guide - Real Estate Risk Scorer

## ✅ Project Fixed and Ready for Netlify!

### What Was Fixed:
1. ✅ Frontend builds successfully without errors
2. ✅ Created `netlify.toml` configuration file
3. ✅ Added SPA fallback (`_redirects` file)
4. ✅ Created `.env.production` for production environment variables
5. ✅ Verified all dependencies install correctly
6. ✅ Build process completes successfully (dist folder generated)

---

## 🚀 Deploy Frontend to Netlify (2 Methods)

### Method 1: Deploy via Netlify CLI (Recommended for Testing)

1. **Install Netlify CLI:**
   ```bash
   npm install -g netlify-cli
   ```

2. **Login to Netlify:**
   ```bash
   netlify login
   ```

3. **Deploy from project root:**
   ```bash
   cd "C:\Users\anjal\OneDrive\Documents\real-estate risks scorer"
   netlify deploy --prod
   ```

4. **Follow prompts:**
   - Choose "Create & configure a new site"
   - Select your team
   - Site name: (choose a unique name)
   - Publish directory: `frontend/dist`

### Method 2: Deploy via Netlify Dashboard (Easier)

1. **Push code to GitHub:**
   ```bash
   cd "C:\Users\anjal\OneDrive\Documents\real-estate risks scorer"
   git init
   git add .
   git commit -m "Initial commit - ready for Netlify"
   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
   git push -u origin main
   ```

2. **Connect to Netlify:**
   - Go to https://app.netlify.com/
   - Click "Add new site" → "Import an existing project"
   - Choose GitHub and select your repository

3. **Configure Build Settings:**
   - **Base directory:** `frontend`
   - **Build command:** `npm run build`
   - **Publish directory:** `frontend/dist`
   - Click "Deploy site"

4. **Set Environment Variables (IMPORTANT!):**
   - After deployment, go to Site settings → Environment variables
   - Add: `VITE_API_URL` = `https://your-backend-url.onrender.com`
   - (Optional) Add: `VITE_OPENWEATHER_API_KEY` if you have one
   - Trigger redeploy after adding variables

---

## 🔧 Deploy Backend (Required for Full Functionality)

Your backend needs to be deployed separately. Options:

### Option 1: Deploy to Render.com (Free Tier Available)
1. Push code to GitHub
2. Go to https://render.com/
3. Create new "Web Service"
4. Connect your repository
5. Configure:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Python 3.11
6. Add environment variables (DATABASE_URL, REDIS_URL, SECRET_KEY, etc.)
7. After deployment, copy the backend URL and update Netlify environment variable

### Option 2: Deploy to Railway.app
1. Go to https://railway.app/
2. Connect GitHub repository
3. Railway will auto-detect `render.yaml` configuration
4. Deploy backend service
5. Copy URL and update Netlify

### Option 3: Use Vercel Serverless Functions
(More complex - requires refactoring backend to serverless)

---

## 📝 Post-Deployment Checklist

After deploying both frontend and backend:

- [ ] Update `VITE_API_URL` in Netlify environment variables with actual backend URL
- [ ] Trigger redeploy on Netlify after updating environment variables
- [ ] Test the deployed site: `https://your-site-name.netlify.app`
- [ ] Check browser console for any API connection errors
- [ ] Verify all features work (property search, risk analysis, etc.)
- [ ] Configure custom domain (optional)

---

## 🐛 Common Issues & Solutions

### Issue: "Cannot GET /dashboard" on page refresh
**Solution:** Already fixed! The `_redirects` file handles SPA routing.

### Issue: API calls fail with CORS error
**Solution:** Add CORS middleware to backend:
```python
# backend/app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-netlify-site.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: Build fails on Netlify
**Solution:** Check Node version in `netlify.toml` (set to 18)

### Issue: Environment variables not working
**Solution:** 
1. Make sure variables start with `VITE_` prefix
2. Rebuild after adding/changing environment variables
3. Clear cache and redeploy

---

## 🎯 Quick Test Locally

Test the production build locally before deploying:

```bash
cd frontend
npm run build
npx serve -s dist -p 3000
```

Visit http://localhost:3000 to test the production build.

---

## 📚 Additional Resources

- Netlify Documentation: https://docs.netlify.com/
- Vite Environment Variables: https://vitejs.dev/guide/env-and-mode.html
- Render.com Docs: https://render.com/docs
- FastAPI CORS: https://fastapi.tiangolo.com/tutorial/cors/

---

## 🎉 You're All Set!

Your project is now ready for Netlify deployment. The frontend will build successfully and all SPA routing will work correctly. Just remember to deploy your backend separately and update the API URL in Netlify's environment variables.

Good luck! 🚀

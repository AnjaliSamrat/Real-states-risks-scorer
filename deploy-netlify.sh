#!/bin/bash

# Netlify Deploy Script
# Run this script to deploy your site to Netlify

echo "🚀 Real Estate Risk Scorer - Netlify Deployment"
echo "================================================"
echo ""

# Check if netlify-cli is installed
if ! command -v netlify &> /dev/null; then
    echo "❌ Netlify CLI not found. Installing..."
    npm install -g netlify-cli
fi

# Navigate to project root
cd "$(dirname "$0")"

echo "📦 Building frontend..."
cd frontend

# Clean previous build
rm -rf dist

# Install dependencies
echo "📥 Installing dependencies..."
npm install

# Build
echo "🔨 Building production bundle..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Build failed! Please fix errors above."
    exit 1
fi

echo "✅ Build successful!"
echo ""

# Deploy
echo "🌐 Deploying to Netlify..."
cd ..
netlify deploy --prod --dir=frontend/dist

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📝 Next steps:"
echo "1. Copy the deployment URL"
echo "2. Deploy your backend to Render/Railway"
echo "3. Update VITE_API_URL in Netlify environment variables"
echo "4. Trigger a redeploy on Netlify"
echo ""
echo "For detailed instructions, see NETLIFY_DEPLOYMENT.md"

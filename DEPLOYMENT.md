# 🚀 Render Deployment Guide

## Manual Deployment Steps

### Step 1: Deploy Backend

1. **Go to Render Dashboard**
   - Visit [render.com](https://render.com)
   - Sign up/Login with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `channingwei/healthassist-rag`

3. **Configure Backend Service**
   - **Name**: `healthassist-backend`
   - **Environment**: `Python`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements-simple.txt`
   - **Start Command**: `cd backend && python api.py`

4. **Environment Variables**
   - `PYTHON_VERSION`: `3.13.4`
   - `PORT`: `5001`

5. **Click "Create Web Service"**

### Step 2: Deploy Frontend

1. **Create New Static Site**
   - Click "New +" → "Static Site"
   - Connect your GitHub repository: `channingwei/healthassist-rag`

2. **Configure Frontend Service**
   - **Name**: `healthassist-frontend`
   - **Environment**: `Static`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/build`

3. **Environment Variables**
   - `REACT_APP_API_URL`: `https://your-backend-service-name.onrender.com`
   - Replace `your-backend-service-name` with your actual backend service name

4. **Click "Create Static Site"**

### Step 3: Test Deployment

1. **Wait for Build**
   - Backend: ~5-10 minutes (includes model download)
   - Frontend: ~2-3 minutes

2. **Check Backend Health**
   - Visit: `https://your-backend-service-name.onrender.com/health`
   - Should return: `{"status": "healthy", "rag_engine_available": true}`

3. **Test Frontend**
   - Visit your frontend URL
   - Try asking a health question

## Troubleshooting

### Common Issues

1. **Build Fails on Backend**
   - Check logs for missing dependencies
   - Ensure `requirements-simple.txt` is in root directory
   - Verify Python version is 3.13.4
   - If setuptools error occurs, try using `requirements-simple.txt`

2. **Frontend Can't Connect to Backend**
   - Verify `REACT_APP_API_URL` environment variable
   - Check backend is running and healthy
   - Ensure CORS is enabled

3. **RAG Engine Not Loading**
   - Check if docs directory exists
   - Verify ChromaDB can create index
   - Look for model download errors

### Logs to Check

- **Backend Logs**: Look for RAG engine initialization
- **Frontend Logs**: Check for API connection errors
- **Build Logs**: Verify all dependencies installed

## Environment Variables Reference

### Backend
```bash
PYTHON_VERSION=3.13.4
PORT=5001
```

### Frontend
```bash
REACT_APP_API_URL=https://your-backend-service-name.onrender.com
```

## URLs After Deployment

- **Backend API**: `https://your-backend-service-name.onrender.com`
- **Frontend**: `https://your-frontend-service-name.onrender.com`
- **Health Check**: `https://your-backend-service-name.onrender.com/health`

## Support

If you encounter issues:
1. Check the Render documentation
2. Review the build logs
3. Verify all files are committed to GitHub
4. Ensure environment variables are set correctly 
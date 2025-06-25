# 🏥 HealthAssist

An AI-powered health information assistant built with React frontend and Flask backend with RAG (Retrieval-Augmented Generation) capabilities.

## Features

- 🤖 **Intelligent Health Q&A**: Powered by RAG technology with health document knowledge base
- 💬 **Real-time Chat Interface**: Modern, responsive chat UI
- 📚 **Health Tips**: Quick access to health advice and guidelines
- 🔍 **Source Attribution**: Shows which health documents were used for answers
- ⚠️ **Medical Disclaimers**: Proper health information warnings
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Architecture

- **Frontend**: React.js with modern CSS
- **Backend**: Flask API with RAG engine
- **RAG Engine**: Sentence transformers + ChromaDB for intelligent document retrieval
- **Knowledge Base**: Health guidelines and symptom information

## Local Development

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python api.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:5001

## Deployment on Render

### Option 1: Using render.yaml (Recommended)

1. **Fork/Clone this repository** to your GitHub account

2. **Connect to Render**:
   - Go to [render.com](https://render.com)
   - Sign up/Login with your GitHub account
   - Click "New +" and select "Blueprint"

3. **Deploy**:
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file
   - Click "Apply" to deploy both services

### Option 2: Manual Deployment

#### Deploy Backend
1. Create a new **Web Service** on Render
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && python api.py`
   - **Environment Variables**:
     - `PYTHON_VERSION`: `3.9.0`
     - `PORT`: `5001`

#### Deploy Frontend
1. Create a new **Static Site** on Render
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/build`
   - **Environment Variables**:
     - `REACT_APP_API_URL`: `https://your-backend-service.onrender.com`

### Environment Variables

#### Backend
- `PORT`: Port number (default: 5001)
- `HOST`: Host address (default: 0.0.0.0)

#### Frontend
- `REACT_APP_API_URL`: Backend API URL

## API Endpoints

- `POST /ask` - Main Q&A endpoint
- `GET /health-tips` - Get health tips by category
- `GET /health` - Health check endpoint

## Health Documents

The system includes comprehensive health information:
- General health guidelines
- Common symptoms and when to seek medical attention
- Nutrition and exercise advice
- Sleep hygiene tips
- Mental health guidance

## Medical Disclaimer

⚠️ **Important**: This application provides general health information for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical concerns.

## Technology Stack

- **Frontend**: React.js, CSS3
- **Backend**: Flask, Python
- **AI/ML**: Sentence Transformers, ChromaDB
- **Deployment**: Render
- **Version Control**: Git

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes. Please ensure compliance with medical information regulations in your jurisdiction.

## Support

For deployment issues or questions, please check the Render documentation or create an issue in this repository.
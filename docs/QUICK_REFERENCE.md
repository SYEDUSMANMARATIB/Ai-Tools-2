# Quick Reference Guide

## 🚀 Getting Started (Choose One)

### Option 1: Zero Dependencies Demo
```bash
python demo.py                    # Interactive demo
python demo.py examples           # See examples
```

### Option 2: Minimal Setup (Backend Only)
```bash
python quick-start.py             # Automated minimal setup
cd backend
python -m uvicorn app.main:app --reload
# Open: http://localhost:8000/api/docs
```

### Option 3: Full Setup (Backend + Beautiful UI)
```bash
# Backend
python quick-start.py
cd backend
python -m uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
# Open: http://localhost:3000
```

### Option 4: Docker
```bash
docker-compose up -d              # Start all services
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

## 📋 Essential Commands

### Development
```bash
# Backend
cd backend && python -m uvicorn app.main:app --reload

# Frontend
cd frontend && npm run dev

# Tests
pytest                            # Backend tests (when implemented)
npm test                          # Frontend tests (when implemented)
```

### API Testing
```bash
# Health check
curl http://localhost:8000/api/health

# Text redaction
curl -X POST "http://localhost:8000/api/redaction/redact-text" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "text=My email is john@example.com and phone is 555-123-4567"

# Document upload
curl -X POST "http://localhost:8000/api/redaction/process-document" \
     -F "file=@sample.pdf"
```

## 🔧 Configuration

### Environment Variables (.env)
```env
# Database
DATABASE_URL=sqlite:///./redaction.db

# File limits
MAX_FILE_SIZE=52428800            # 50MB

# AI Models
USE_LOCAL_MODELS=true
SPACY_MODEL=en_core_web_sm

# CORS (for frontend)
ALLOWED_HOSTS=["http://localhost:3000"]
```

## 🎯 Entity Types Detected

- **EMAIL**: `john@example.com`
- **PHONE**: `(555) 123-4567`, `555.123.4567`, `+1-555-123-4567`
- **SSN**: `123-45-6789`, `123 45 6789`
- **CREDIT_CARD**: `4532-1234-5678-9012`, `4532 1234 5678 9012`
- **DATE**: `12/25/1990`, `Jan 15, 2024`, `2024-01-15`
- **FINANCIAL**: `$1,234.56`, `Account #12345`, `Routing #987654321`
- **PERSON**: Names detected by AI models
- **ORGANIZATION**: Company names and institutions

## 🌐 URLs & Endpoints

### Frontend (React UI)
- **Main App**: http://localhost:3000
- **Upload Page**: http://localhost:3000/upload
- **Results**: http://localhost:3000/results
- **Processing Status**: http://localhost:3000/processing
- **Audit Dashboard**: http://localhost:3000/audit

### Backend API
- **API Root**: http://localhost:8000
- **Health Check**: http://localhost:8000/api/health
- **API Documentation**: http://localhost:8000/api/docs
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Key API Endpoints
- `POST /api/redaction/redact-text` - Redact text
- `POST /api/redaction/analyze-text` - Analyze without redaction
- `POST /api/redaction/process-document` - Extract text from document
- `POST /api/redaction/redact-document` - Process and redact document
- `GET /api/redaction/supported-formats` - Get supported file types
- `GET /api/redaction/entity-types` - Get available entity types

## 🔍 Troubleshooting

### Common Issues
```bash
# Port in use
lsof -i :8000 && kill -9 <PID>    # macOS/Linux
netstat -ano | findstr :8000      # Windows

# Dependencies
pip install -r backend/requirements-minimal.txt

# spaCy model
python -m spacy download en_core_web_sm

# Node.js dependencies
cd frontend && npm install

# Permissions (macOS/Linux)
chmod +x setup.py quick-start.py demo.py
```

### File Issues
```bash
# Check file permissions
ls -la demo.py setup.py quick-start.py

# Make executable
chmod +x *.py

# Python path issues
python -m pip install --upgrade pip
which python
```

## 📁 Project Structure
```
intelligent-document-redaction/
├── demo.py                       # Zero-dependency demo ✅
├── quick-start.py               # Minimal setup ✅
├── setup.py                     # Full setup ✅
├── backend/                     # Python API ✅
│   ├── app/main.py             # FastAPI application
│   ├── app/api/redaction.py    # Redaction endpoints
│   ├── app/services/           # Business logic
│   └── requirements*.txt       # Dependencies
├── frontend/                    # React UI ✅
│   ├── src/components/         # UI components
│   ├── src/pages/              # Page components
│   ├── src/App.tsx             # Main application
│   └── package.json            # Node dependencies
├── docs/                        # Documentation ✅
└── docker-compose.yml           # Docker setup ✅
```

## 🎮 Demo Examples

Try these in the demo or API:
```bash
# Email and phone
"My email is test@example.com and phone is 555-123-4567"

# Financial information
"SSN: 123-45-6789, Credit Card: 4532-1234-5678-9012"

# Banking details
"Account #12345678, routing #987654321, amount: $1,234.56"

# Personal information
"Contact John Doe at john.doe@company.com or call (555) 123-4567"

# Medical information
"Patient DOB: 01/15/1985, SSN: 123-45-6789, Policy #ABC123456"
```

## 🛠️ Development Tips

### Backend Development
```bash
# Auto-reload on changes
python -m uvicorn app.main:app --reload

# Debug mode
DEBUG=true python -m uvicorn app.main:app --reload

# Custom port
python -m uvicorn app.main:app --port 8001 --reload

# Custom host (for network access)
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Development
```bash
# Development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Install new dependencies
npm install <package-name>
npm install --save-dev <dev-package>
```

### Docker Development
```bash
# Rebuild specific service
docker-compose build backend
docker-compose build frontend

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Shell into container
docker-compose exec backend bash
docker-compose exec frontend sh

# Clean up
docker-compose down -v
docker system prune
```

### Testing Commands
```bash
# Test API endpoints
curl -X GET http://localhost:8000/api/health
curl -X GET http://localhost:8000/api/redaction/supported-formats
curl -X GET http://localhost:8000/api/redaction/entity-types

# Test text redaction
curl -X POST "http://localhost:8000/api/redaction/redact-text" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "text=Call me at 555-123-4567 or email test@example.com"

# Test text analysis (no redaction)
curl -X POST "http://localhost:8000/api/redaction/analyze-text" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "text=My SSN is 123-45-6789"
```

## 📝 Notes

- **Zero Dependencies Demo**: Works with just Python standard library
- **Minimal Setup**: Requires only basic Python packages (FastAPI, spaCy)
- **Full Setup**: Includes beautiful React UI with all features
- **Docker**: Complete containerized environment
- **Production Ready**: All components designed for enterprise use
- **Extensible**: Easy to add new entity types and detection methods
- **Compliant**: Built-in audit trails for regulatory compliance

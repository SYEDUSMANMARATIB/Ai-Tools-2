# Installation Guide

This guide will help you set up the Intelligent Document Redaction Tool on your local machine.

## Prerequisites

### Required Software
- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **PostgreSQL 13+** - [Download PostgreSQL](https://www.postgresql.org/download/)
- **Redis** - [Download Redis](https://redis.io/download)
- **Git** - [Download Git](https://git-scm.com/downloads)

### Optional (Recommended)
- **Docker & Docker Compose** - [Download Docker](https://www.docker.com/products/docker-desktop/)
- **Tesseract OCR** - [Installation Guide](https://tesseract-ocr.github.io/tessdoc/Installation.html)

### API Keys (Required)
You'll need at least one of these API keys:
- **OpenAI API Key** - [Get API Key](https://platform.openai.com/api-keys)
- **Anthropic API Key** - [Get API Key](https://console.anthropic.com/)

## Quick Start with Docker (Recommended)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd intelligent-document-redaction
```

### 2. Set Up Environment Variables
```bash
cp .env.example .env
```

Edit the `.env` file and add your API keys:
```env
OPENAI_API_KEY=your_actual_openai_api_key_here
ANTHROPIC_API_KEY=your_actual_anthropic_api_key_here
SECRET_KEY=your_super_secret_key_here
```

### 3. Start with Docker Compose
```bash
docker-compose up -d
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs

## Manual Installation

### Backend Setup

#### 1. Navigate to Backend Directory
```bash
cd backend
```

#### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Install spaCy Model
```bash
python -m spacy download en_core_web_sm
```

#### 5. Set Up Database
Make sure PostgreSQL is running, then create the database:
```sql
CREATE DATABASE redaction_db;
CREATE USER redaction_user WITH PASSWORD 'redaction_password';
GRANT ALL PRIVILEGES ON DATABASE redaction_db TO redaction_user;
```

#### 6. Run Database Migrations
```bash
alembic upgrade head
```

#### 7. Start the Backend Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

#### 1. Navigate to Frontend Directory
```bash
cd frontend
```

#### 2. Install Dependencies
```bash
npm install
```

#### 3. Start Development Server
```bash
npm run dev
```

### Background Tasks (Optional)

#### 1. Start Redis Server
```bash
redis-server
```

#### 2. Start Celery Worker
```bash
cd backend
celery -A app.core.celery worker --loglevel=info
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure the following:

#### Required Settings
```env
# API Keys (at least one required)
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Security
SECRET_KEY=your_secret_key_here
```

#### Database Settings
```env
DATABASE_URL=postgresql://redaction_user:redaction_password@localhost:5432/redaction_db
```

#### Redis Settings
```env
REDIS_URL=redis://localhost:6379
```

### OCR Setup (Optional)

For processing scanned documents, install Tesseract OCR:

#### Windows
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Add to PATH or set `TESSERACT_CMD` in `.env`

#### macOS
```bash
brew install tesseract
```

#### Ubuntu/Debian
```bash
sudo apt-get install tesseract-ocr
```

## Verification

### 1. Check Backend Health
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{"status": "healthy", "version": "1.0.0"}
```

### 2. Check Frontend
Open http://localhost:3000 in your browser

### 3. Test File Upload
1. Go to the upload page
2. Drag and drop a test document
3. Verify the file uploads successfully

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Kill process using port 3000
lsof -ti:3000 | xargs kill -9
```

#### Database Connection Issues
1. Verify PostgreSQL is running
2. Check database credentials in `.env`
3. Ensure database exists

#### Missing Dependencies
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

#### OCR Not Working
1. Install Tesseract OCR
2. Set correct path in `.env`:
   ```env
   TESSERACT_CMD=/usr/local/bin/tesseract
   ```

### Getting Help

If you encounter issues:
1. Check the logs in the terminal
2. Verify all prerequisites are installed
3. Ensure API keys are valid
4. Check firewall/antivirus settings

## Next Steps

Once installation is complete:
1. Upload a test document
2. Review the redaction results
3. Check the audit logs
4. Customize redaction patterns if needed

For production deployment, see the deployment guide.

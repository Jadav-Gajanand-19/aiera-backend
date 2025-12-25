# 🌿 Aira Backend API

FastAPI backend for the Aira emotional support companion, powered by Google Gemini.

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Add your GOOGLE_API_KEY to .env

# Run server
python main.py
```

Server runs at `http://localhost:8000`

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/chat` | POST | Chat with Aira |
| `/docs` | GET | Swagger docs |

### Chat Request

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I feel stressed today"}'
```

---

## 🔧 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google AI API key | ✅ |
| `DB_PATH` | SQLite database path | ❌ |
| `PORT` | Server port | ❌ |

---

## ☁️ Deploy to Railway

1. Push this folder to GitHub
2. Create project on [Railway.app](https://railway.app)
3. Add `GOOGLE_API_KEY` environment variable
4. Deploy ✨

---

## 📁 Files

| File | Purpose |
|------|---------|
| `main.py` | FastAPI server |
| `agent.py` | Aira agent logic |
| `requirements.txt` | Dependencies |
| `railway.json` | Railway config |

---

*Aira — A space to breathe, feel, and be.*

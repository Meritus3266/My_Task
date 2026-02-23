# Nigerian Law RAG System

Production-ready Agentic RAG system for querying Nigerian law documents using LangChain, LangGraph, and FastAPI.

## 🌟 Features

- **Agentic RAG** with LangGraph for intelligent document retrieval
- **FastAPI Backend** with REST API and WebSocket support
- **Session Management** for multi-turn conversations
- **Vector Search** using ChromaDB and OpenAI embeddings
- **Production Ready** with proper error handling and logging
- **CLI Interface** for local testing and development

## 📋 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure

Create `.env` file:
```bash
OPENAI_API_KEY=your_api_key_here
```

### 3. Add Documents

Place PDF files in `documents/` folder:
- LAW 243.pdf
- law 432 LAW OF BANKING AND INSURANCE II  post editorial.pdf
- LAW411 oil and gas I.pdf

### 4. Start Server

**Option A: Quick Start (Recommended)**
```bash
python start.py
```
This automatically checks prerequisites and starts the server.

**Option B: Manual Start**
```bash
python backend.py
```

**Option C: Using uvicorn**
```bash
uvicorn backend:app --reload
```

### 5. Access API

- **API Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Base URL:** http://localhost:8000

## 📁 Project Structure

```
nigerian-law-rag/
├── app.py                  # Core RAG agent
├── backend.py              # FastAPI server
├── start.py                # Quick start script
├── test_backend.py         # API test client
├── requirements.txt        # Dependencies
├── .env                    # Environment config
├── documents/              # PDF files
└── chroma_db/              # Vector database
```

## 🎯 Usage

### CLI Mode

```bash
# Interactive chat
python app.py --interactive

# Single query
python app.py --query "What is LAW 243 about?"

# Initialize database only
python app.py --init-db

# Rebuild database
python app.py --rebuild --init-db
```

### API Mode

```bash
# Start server
python backend.py

# Test API
python test_backend.py
```

### Python API Usage

```python
import requests

# Create session
response = requests.post("http://localhost:8000/sessions")
session_id = response.json()["session_id"]

# Query documents
response = requests.post(
    "http://localhost:8000/query",
    json={
        "query": "What is LAW 243 about?",
        "session_id": session_id
    }
)

print(response.json()["response"])
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/query` | POST | Query documents |
| `/chat` | POST | Chat endpoint |
| `/sessions` | POST | Create session |
| `/sessions` | GET | List sessions |
| `/sessions/{id}` | GET | Get session |
| `/sessions/{id}/history` | GET | Get history |
| `/sessions/{id}` | DELETE | Close session |
| `/stats` | GET | Statistics |
| `/ws/{id}` | WS | WebSocket |

## 🧪 Testing

```bash
# Run all tests
python test_backend.py

# Test specific endpoint
curl http://localhost:8000/health

# Query documents
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is LAW 243 about?"}'
```

## ⚙️ Configuration

Edit `.env` to customize:

```bash
# API Key (Required)
OPENAI_API_KEY=sk-...

# Model Settings
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small

# Document Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=150
RETRIEVER_K=4

# Server
HOST=0.0.0.0
PORT=8000
```

## 🐛 Troubleshooting

### "OPENAI_API_KEY not found"
- Create `.env` file
- Add your OpenAI API key

### "No PDF documents found"
- Place PDF files in `documents/` folder
- Restart the application

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Port already in use"
```bash
# Change port in .env
PORT=8001
```

### Vector Database Issues
```bash
# Rebuild database
python app.py --rebuild --init-db
```

## 📚 Documentation

- **Setup Guide:** See `SETUP_GUIDE.md`
- **API Docs:** http://localhost:8000/docs (when running)
- **Code Comments:** Detailed inline documentation

## 🚀 Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn backend:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker (Optional)

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables

For production, use environment variables instead of `.env` file:

```bash
export OPENAI_API_KEY=your_key_here
python backend.py
```

## 🔒 Security

- Never commit `.env` file
- Use secrets management in production
- Add authentication for production APIs
- Restrict CORS origins
- Implement rate limiting

## 📊 Performance

- Vector database stored on disk for persistence
- Async operations for better concurrency
- Session-based conversation memory
- Configurable retrieval parameters

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License

## 🆘 Support

For issues:
1. Check `SETUP_GUIDE.md`
2. Review troubleshooting section
3. Check server logs
4. Verify configuration

## ✅ Checklist

- [ ] Python 3.9+ installed
- [ ] Dependencies installed
- [ ] `.env` file configured
- [ ] PDFs in `documents/` folder
- [ ] Vector database initialized
- [ ] Server starts successfully
- [ ] Test returns valid response

---

**Made with ❤️ using LangChain, LangGraph, and FastAPI**
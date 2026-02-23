# Setup Guide - Nigerian Law RAG System

## 📁 Project Structure

Your project should look like this:

```
nigerian-law-rag/
├── app.py                  # Core RAG agent (CLI + API functions)
├── backend.py              # FastAPI server
├── test_backend.py         # API test client
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── documents/              # Place PDF files here (auto-created)
│   ├── LAW 243.pdf
│   ├── law 432 LAW OF BANKING AND INSURANCE II  post editorial.pdf
│   └── LAW411 oil and gas I.pdf
└── chroma_db/              # Vector database (auto-created)
```

## 🚀 Installation Steps

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment

Create a `.env` file:

```bash
# Copy the content
OPENAI_API_KEY=your_openai_api_key_here
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
CHUNK_SIZE=1000
CHUNK_OVERLAP=150
RETRIEVER_K=4
HOST=0.0.0.0
PORT=8000
```

**Important:** Replace `your_openai_api_key_here` with your actual OpenAI API key

### Step 3: Add PDF Documents

Create the `documents/` folder and add your PDF files:

```bash
mkdir -p documents
# Copy your PDF files into documents/
```

Expected files:
- `LAW 243.pdf`
- `law 432 LAW OF BANKING AND INSURANCE II  post editorial.pdf`
- `LAW411 oil and gas I.pdf`

### Step 4: Initialize Vector Database

**Option A: Via CLI**
```bash
python app.py --init-db
```

**Option B: It will auto-initialize on first run**

## 🎯 Usage

### Option 1: FastAPI Server (Recommended)

**Start the server:**
```bash
python backend.py
```

Or using uvicorn:
```bash
uvicorn backend:app --reload --host 0.0.0.0 --port 8000
```

**Access the API:**
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Base URL: http://localhost:8000

**Test the API:**
```bash
python test_backend.py
```

### Option 2: Command Line Interface

**Interactive mode:**
```bash
python app.py --interactive
```

**Single query:**
```bash
python app.py --query "What is LAW 243 about?"
```

**With specific thread:**
```bash
python app.py --query "What are the main topics?" --thread my_session
```

### Option 3: Using the API Programmatically

```python
import requests

# Create session
response = requests.post("http://localhost:8000/sessions")
session_id = response.json()["session_id"]

# Query
response = requests.post(
    "http://localhost:8000/query",
    json={
        "query": "What is LAW 243 about?",
        "session_id": session_id
    }
)

data = response.json()
print(data["response"])
print(data["sources"])
```

## 📝 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/query` | Query documents |
| POST | `/chat` | Chat endpoint (alias) |
| POST | `/sessions` | Create new session |
| GET | `/sessions` | List all sessions |
| GET | `/sessions/{id}` | Get session info |
| GET | `/sessions/{id}/history` | Get conversation history |
| DELETE | `/sessions/{id}` | Close session |
| GET | `/stats` | System statistics |
| WS | `/ws/{id}` | WebSocket connection |

### Example Requests

**Query Documents:**
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is LAW 243 about?"}'
```

**Get Session History:**
```bash
curl -X GET "http://localhost:8000/sessions/{session_id}/history"
```

**System Stats:**
```bash
curl -X GET "http://localhost:8000/stats"
```

## 🔧 Troubleshooting

### "OPENAI_API_KEY not found"
- Make sure `.env` file exists
- Check that your API key is correctly set
- No spaces or quotes around the key value

### "No pages were loaded from any PDF"
- Ensure PDF files are in `documents/` folder
- Check file names match those in `app.py` PDF_FILES list
- Verify PDFs are not corrupted

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Port 8000 already in use"
Change port in `.env` or run:
```bash
uvicorn backend:app --port 8001
```

### Vector Database Issues
Rebuild the database:
```bash
python app.py --rebuild --init-db
```

### API Connection Refused
Make sure the server is running:
```bash
python backend.py
```

## 🎨 Customization

### Change LLM Model

Edit `.env`:
```bash
LLM_MODEL=gpt-4  # More powerful but expensive
# or
LLM_MODEL=gpt-3.5-turbo  # Faster and cheaper
```

### Adjust Document Chunking

Edit `.env`:
```bash
CHUNK_SIZE=1500      # Larger chunks = more context
CHUNK_OVERLAP=200    # More overlap = better continuity
RETRIEVER_K=6        # Retrieve more documents
```

### Add More Documents

1. Place PDF files in `documents/` folder
2. Add filenames to `PDF_FILES` list in `app.py`
3. Rebuild database: `python app.py --rebuild --init-db`

## 📊 Testing

### Run Full Test Suite
```bash
python test_backend.py
```

### Test Individual Components

**Test CLI:**
```bash
python app.py --query "What is LAW 243 about?"
```

**Test Health:**
```bash
curl http://localhost:8000/health
```

**Test Query:**
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the main topics in banking law?"}'
```

## 🔒 Production Deployment

### Security Considerations

1. **Environment Variables:** Never commit `.env` to git
2. **API Keys:** Use secrets management in production
3. **CORS:** Restrict origins in production
4. **Rate Limiting:** Add rate limiting middleware
5. **Authentication:** Add API key authentication

### Production Configuration

```python
# In backend.py, update CORS:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Run with Multiple Workers

```bash
uvicorn backend:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Gunicorn (Production)

```bash
pip install gunicorn
gunicorn backend:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📈 Performance Tips

1. **Vector Store:** Keep vector database on SSD
2. **Caching:** Consider adding Redis for response caching
3. **Async:** Use async operations where possible
4. **Batch Processing:** Process multiple queries in batches
5. **Monitoring:** Add logging and monitoring

## 🆘 Support

If you encounter issues:

1. Check logs for error messages
2. Verify all dependencies are installed
3. Ensure OpenAI API key is valid
4. Check that documents are properly loaded
5. Review the troubleshooting section above

## ✅ Checklist

Before running the system:

- [ ] Python 3.9+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with OpenAI API key
- [ ] PDF documents in `documents/` folder
- [ ] Vector database initialized (auto or manual)
- [ ] Server starts without errors
- [ ] Test endpoint returns successful response

---

**Ready to go!** Start with: `python backend.py` 🚀
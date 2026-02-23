# Policy Assistant - Agentic RAG System

A complete AI-powered system for querying policy documents with intelligent retrieval, conversation context, and source citations.

##  Architecture

### Three Main Components:

#### 1. **AI Engine (Agentic RAG with LangGraph)** - `New_chunks.ipynb`
- Loads and processes policy documents (LAW 243, LAW 432, LAW 411)
- Creates semantic embeddings using OpenAI's text-embedding-3-small
- Builds vector database with Chroma for fast retrieval
- Implements ReAct agent that decides WHEN to retrieve documents
- Maintains conversation context for follow-up questions
- Automatically cites sources in responses

#### 2. **Backend API (FastAPI)** - `fastapi_backend.py`
- RESTful API endpoints for all chat operations
- Session management for multi-turn conversations
- Persistent conversation history
- WebSocket support for real-time chat
- System statistics and monitoring

#### 3. **Frontend (Optional)**
- Can be built with React/Vue/Angular
- Connects to backend via REST API or WebSocket

##  Setup Instructions

### Prerequisites
- Python 3.9+
- OpenAI API key
- pip package manager

### Installation

1. **Install Backend Dependencies**
```bash
pip install -r backend_requirements.txt
```

2. **Set up environment variables**
Create a `.env` file in the rag_project folder:
```
OPENAI_API_KEY=your_api_key_here
```

3. **Run the notebook** (One time setup)
- Open `New_chunks.ipynb` in Jupyter
- Run all cells to:
  - Load PDF documents
  - Create embeddings and vector database
  - Initialize the agentic RAG system
  - Test with sample queries

4. **Start the FastAPI Backend**
```bash
python fastapi_backend.py
```

The API will be available at: `http://localhost:8000`

##  API Usage

### Base URL
```
http://localhost:8000
```

### Key Endpoints

#### 1. Create a Session
```bash
POST /sessions
Response:
{
  "session_id": "uuid",
  "status": "created",
  "timestamp": "2024-01-23T..."
}
```

#### 2. Send a Query
```bash
POST /chat
Body:
{
  "query": "What is LAW 243 about?",
  "session_id": "uuid"  // optional, creates new if not provided
}

Response:
{
  "session_id": "uuid",
  "query": "What is LAW 243 about?",
  "response": "LAW 243 is about...",
  "sources": ["LAW 243.pdf (Page 1)", "LAW 243.pdf (Page 5)"],
  "timestamp": "2024-01-23T..."
}
```

#### 3. Send Follow-up Question (with context)
```bash
POST /chat/follow-up
Body:
{
  "query": "Tell me more about that",
  "session_id": "uuid"  // required
}
```

#### 4. Get Conversation History
```bash
GET /sessions/{session_id}/history
Response:
{
  "session_id": "uuid",
  "messages": [
    {
      "role": "user",
      "content": "What is LAW 243?",
      "timestamp": "...",
      "sources": null
    },
    {
      "role": "assistant",
      "content": "LAW 243 is...",
      "timestamp": "...",
      "sources": ["LAW 243.pdf (Page 1)"]
    }
  ],
  "created_at": "...",
  "total_messages": 2
}
```

#### 5. List All Sessions
```bash
GET /sessions
Response:
{
  "sessions": [
    {
      "session_id": "uuid",
      "created_at": "...",
      "last_message_at": "...",
      "message_count": 5,
      "status": "active"
    }
  ],
  "total": 1,
  "timestamp": "..."
}
```

#### 6. Get Document List
```bash
GET /documents
Response:
{
  "documents": [
    {
      "name": "LAW 243.pdf",
      "type": "pdf",
      "status": "indexed",
      "chunks": 15,
      "description": "Law document 243"
    },
    ...
  ],
  "total_documents": 3,
  "total_chunks": 55
}
```

#### 7. Get System Statistics
```bash
GET /system/stats
Response:
{
  "total_sessions": 5,
  "active_sessions": 3,
  "total_messages": 28,
  "documents_indexed": 3,
  "total_chunks": 55
}
```

#### 8. Close Session
```bash
DELETE /sessions/{session_id}
Response:
{
  "session_id": "uuid",
  "status": "closed",
  "timestamp": "..."
}
```

### WebSocket Real-time Chat
```javascript
// Connect
const ws = new WebSocket('ws://localhost:8000/ws/session_id');

// Send query
ws.send(JSON.stringify({
  query: "What is LAW 243 about?"
}));

// Receive response
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data.response);
  console.log(data.sources);
};
```

##  AI Engine Features

### Document Processing
- **Lads**: 3 PDF documents (LAW 243, LAW 432, LAW 411)
- **Chunks**: 55 total chunks with 1000 character size and 100 character overlap
- **Embeddings**: OpenAI text-embedding-3-small for semantic understanding

### Agent Capabilities
- **Semantic Search**: Retrieves top 3 relevant chunks per query
- **Context Awareness**: Maintains conversation history within sessions
- **Source Citations**: Every answer includes document sources and page numbers
- **Smart Retrieval**: Uses ReAct agent to decide when/how to retrieve information
- **Error Handling**: Graceful fallbacks for queries with no relevant results

### System Components
```
┌─────────────────────────────────────┐
│         Frontend (Optional)         │
│     React/Vue/Angular SPA          │
└────────────────┬────────────────────┘
                 │ REST API / WebSocket
┌────────────────▼────────────────────┐
│       FastAPI Backend               │
│  - Session Management              │
│  - API Endpoints                   │
│  - Request/Response Handling       │
└────────────────┬────────────────────┘
                 │ invoke
┌────────────────▼────────────────────┐
│    LangGraph Agentic RAG           │
│  - ReAct Agent                     │
│  - State Graph                     │
│  - Memory Management               │
└────────────────┬────────────────────┘
                 │ uses
┌────────────────▼────────────────────┐
│    Retrieval & LLM Pipeline        │
│  - Chroma Vector Store             │
│  - OpenAI Embeddings               │
│  - GPT-4o-mini LLM                 │
└─────────────────────────────────────┘
```

##  Conversation Flow

1. **User sends query** → FastAPI receives request
2. **Session created/retrieved** → Conversation context loaded
3. **Agent decides** → Should we search documents?
4. **Retrieval triggered** → Vector search finds relevant chunks
5. **LLM processes** → Uses retrieval results + context
6. **Response generated** → With automatic source citations
7. **History saved** → For follow-up questions
8. **Response sent** → Back to user via API/WebSocket

##  Configuration

### Vector Store Settings (in notebook)
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Characters per chunk
    chunk_overlap=100,    # Overlap for context
    separators=["\n\n", "\n", " ", ""]
)
```

### Retriever Settings (in notebook)
```python
retriever = vector_store.as_retriever(search_kwargs={"k": 3})
# Retrieves top 3 chunks per query
```

### LLM Settings (in notebook)
```python
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5,  # Balance between creative and factual
    api_key=openai_api_key
)
```

##  Example Usage

### Python Client Example
```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Create session
session_response = requests.post(f"{BASE_URL}/sessions")
session_id = session_response.json()["session_id"]

# Ask question
chat_response = requests.post(f"{BASE_URL}/chat", json={
    "query": "What is LAW 243 about?",
    "session_id": session_id
})

result = chat_response.json()
print(f"Response: {result['response']}")
print(f"Sources: {result['sources']}")

# Follow-up question
follow_up = requests.post(f"{BASE_URL}/chat/follow-up", json={
    "query": "Tell me more about section 3",
    "session_id": session_id
})

# Get history
history = requests.get(f"{BASE_URL}/sessions/{session_id}/history")
print(json.dumps(history.json(), indent=2))
```

##  Testing

### API Documentation
- **Interactive Docs**: `http://localhost:8000/docs` (Swagger UI)
- **ReDoc**: `http://localhost:8000/redoc` (Alternative docs)

### Test the Agent
1. Run the notebook cells to test locally
2. Use the FastAPI backend for remote access
3. Check `/health` endpoint to verify server is running

##  Security Considerations

1. **API Key Protection**: Keep OPENAI_API_KEY in .env file
2. **CORS Configuration**: Currently allows all origins (update for production)
3. **Session Validation**: Always validate session_id exists
4. **Error Handling**: Errors don't expose sensitive information
5. **Rate Limiting**: Add rate limiting middleware for production

##  Performance Tips

1. **Vector Store**: Persists to disk (`./chroma_db`) - reloads faster
2. **Chunk Size**: 1000 characters balances context and retrieval speed
3. **Embeddings Cache**: Chroma caches embeddings automatically
4. **Connection Pooling**: FastAPI handles connection pooling

##  Troubleshooting

### Issue: "OPENAI_API_KEY not found"
**Solution**: Create `.env` file with your API key

### Issue: "No pages loaded"
**Solution**: Ensure PDF files are in the same folder as notebook

### Issue: Backend won't start
**Solution**: Check port 8000 is available, try `python fastapi_backend.py --port 8001`

### Issue: Sessions not persisting
**Solution**: Sessions are in-memory. Use database for production persistence

##  Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Chroma Vector Store](https://docs.trychroma.com/)

##  Files Structure

```
rag_project/
├── New_chunks.ipynb              # AI Engine (LangGraph + RAG)
├── fastapi_backend.py            # Backend API
├── backend_requirements.txt       # Python dependencies
├── .env                          # Environment variables
├── chroma_db/                    # Vector store (persistent)
├── LAW 243.pdf
├── LAW 432 LAW OF BANKING...pdf
├── LAW411 oil and gas I.pdf
└── README.md                     # This file
```

##  Next Steps

1. **Run the notebook** to set up the AI engine
2. **Start the FastAPI backend** 
3. **Test endpoints** via Swagger UI at `/docs`
4. **Build a frontend** using the REST API
5. **Deploy** to production with proper security measures

---

**Version**: 1.0.0  
**Last Updated**: January 23, 2026  
**Status**: Ready for use 

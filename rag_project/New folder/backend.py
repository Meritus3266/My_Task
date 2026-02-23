# # fastapi_backend.py
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import Optional, List
# from datetime import datetime
# import uuid
# import os

# #  from rag_engine import engine

# app = FastAPI(
#     title="Nigerian Law RAG API",
#     description="Agentic RAG over Constitutional, Banking & Oil/Gas law documents",
#     version="1.0.0"
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# class ChatRequest(BaseModel):
#     query: str
#     session_id: Optional[str] = None
#     force_rebuild: bool = False


# class ChatResponse(BaseModel):
#     session_id: str
#     query: str
#     answer: str
#     timestamp: str


# @app.on_event("startup")
# async def startup():
#     # Warm-up / force initialization in production you might want lazy init
#     try:
#         engine.initialize()
#     except Exception as e:
#         print(f"Startup initialization failed: {e}")


# @app.post("/chat", response_model=ChatResponse)
# async def chat(request: ChatRequest):
#     """
#     Main chat endpoint  creates session if none provided
#     """
#     try:
#         session_id = request.session_id or str(uuid.uuid4())

#         if request.force_rebuild:
#             engine.initialize(force_rebuild=True)

#         answer = await engine.query(
#             question=request.query,
#             thread_id=session_id
#         )

#         return ChatResponse(
#             session_id=session_id,
#             query=request.query,
#             answer=answer,
#             timestamp=datetime.utcnow().isoformat() + "Z"
#         )

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/health")
# async def health():
#     return {
#         "status": "ok",
#         "vector_store_loaded": engine._initialized,
#         "timestamp": datetime.utcnow().isoformat() + "Z"
#     }


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         "fastapi_backend:app",
#         host="0.0.0.0",
#         port=int(os.getenv("PORT", 8000)),
#         reload=os.getenv("ENV", "development") == "development"
#     )









# from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import Optional, List, Dict
# from datetime import datetime
# import uuid
# import json
# import logging

# # Import the RAG agent from app.py
# from app import query_agent, init_components

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger("backend")

# #  FastAPI Application

# app = FastAPI(
#     title="Nigerian Law RAG API",
#     description="Agentic RAG system for querying Nigerian law documents",
#     version="1.0.0"
# )

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# #  Data Models

# class ChatMessage(BaseModel):
#     """Model for a single chat message"""
#     role: str
#     content: str
#     timestamp: str
#     sources: Optional[List[str]] = []

# class QueryRequest(BaseModel):
#     """Model for incoming query request"""
#     query: str
#     session_id: Optional[str] = None

# class QueryResponse(BaseModel):
#     """Model for query response"""
#     session_id: str
#     query: str
#     response: str
#     sources: List[str]
#     timestamp: str

# class SessionInfo(BaseModel):
#     """Model for session information"""
#     session_id: str
#     created_at: str
#     last_message_at: str
#     message_count: int
#     status: str

# class ConversationHistory(BaseModel):
#     """Model for conversation history"""
#     session_id: str
#     messages: List[ChatMessage]
#     created_at: str
#     total_messages: int

# #  Session Management

# class SessionManager:
#     """Manage conversation sessions and history"""
    
#     def __init__(self):
#         self.sessions: Dict[str, Dict] = {}
    
#     def create_session(self) -> str:
#         """Create a new conversation session"""
#         session_id = str(uuid.uuid4())
#         self.sessions[session_id] = {
#             "created_at": datetime.now().isoformat(),
#             "last_message_at": datetime.now().isoformat(),
#             "messages": [],
#             "status": "active"
#         }
#         logger.info(f"Created session: {session_id}")
#         return session_id
    
#     def get_session(self, session_id: str) -> Optional[Dict]:
#         """Retrieve session data"""
#         return self.sessions.get(session_id)
    
#     def session_exists(self, session_id: str) -> bool:
#         """Check if session exists"""
#         return session_id in self.sessions
    
#     def add_message(self, session_id: str, role: str, content: str, sources: Optional[List[str]] = None):
#         """Add a message to session history"""
#         if session_id not in self.sessions:
#             return False
        
#         message = {
#             "role": role,
#             "content": content,
#             "timestamp": datetime.now().isoformat(),
#             "sources": sources or []
#         }
        
#         self.sessions[session_id]["messages"].append(message)
#         self.sessions[session_id]["last_message_at"] = datetime.now().isoformat()
#         return True
    
#     def get_conversation_history(self, session_id: str) -> Optional[List[Dict]]:
#         """Get all messages for a session"""
#         if session_id not in self.sessions:
#             return None
#         return self.sessions[session_id]["messages"]
    
#     def close_session(self, session_id: str) -> bool:
#         """Close a session"""
#         if session_id in self.sessions:
#             self.sessions[session_id]["status"] = "closed"
#             logger.info(f"Closed session: {session_id}")
#             return True
#         return False
    
#     def get_all_sessions(self) -> List[Dict]:
#         """Get all sessions"""
#         return [
#             {
#                 "session_id": sid,
#                 "created_at": data["created_at"],
#                 "last_message_at": data["last_message_at"],
#                 "message_count": len(data["messages"]),
#                 "status": data["status"]
#             }
#             for sid, data in self.sessions.items()
#         ]

# # Initialize session manager
# session_manager = SessionManager()

# #  Application Lifecycle

# @app.on_event("startup")
# async def startup_event():
#     """Initialize the RAG system on startup"""
#     logger.info(" Starting Nigerian Law RAG API...")
#     try:
#         init_components()
#         logger.info(" RAG system initialized successfully")
#     except Exception as e:
#         logger.error(f" Failed to initialize RAG system: {e}")
#         raise

# @app.on_event("shutdown")
# async def shutdown_event():
#     """Cleanup on shutdown"""
#     logger.info("Shutting down Nigerian Law RAG API...")

# #  API Endpoints


# @app.get("/", tags=["Root"])
# async def root():
#     """API information and endpoints"""
#     return {
#         "service": "Nigerian Law RAG API",
#         "version": "1.0.0",
#         "description": "Agentic RAG for Constitutional, Banking/Insurance, and Oil & Gas Law",
#         "status": "running",
#         "endpoints": {
#             "health": "GET /health",
#             "query": "POST /query",
#             "chat": "POST /chat",
#             "sessions": "GET /sessions",
#             "create_session": "POST /sessions",
#             "get_session": "GET /sessions/{session_id}",
#             "history": "GET /sessions/{session_id}/history",
#             "close_session": "DELETE /sessions/{session_id}",
#             "websocket": "WS /ws/{session_id}"
#         },
#         "docs": "/docs",
#         "redoc": "/redoc"
#     }

# @app.get("/health", tags=["Health"])
# async def health_check():
#     """Health check endpoint"""
#     return {
#         "status": "healthy",
#         "service": "Nigerian Law RAG API",
#         "timestamp": datetime.now().isoformat()
#     }

# @app.post("/query", response_model=QueryResponse, tags=["Query"])
# async def query_documents(request: QueryRequest):
#     """
#     Query the Nigerian law documents
    
#     Args:
#         request: QueryRequest with query text and optional session_id
    
#     Returns:
#         QueryResponse with answer and sources
#     """
#     try:
#         # Create session if not provided
#         session_id = request.session_id or session_manager.create_session()
        
#         # Validate session
#         if not session_manager.session_exists(session_id):
#             raise HTTPException(status_code=404, detail="Session not found")
        
#         # Store user query
#         session_manager.add_message(session_id, "user", request.query)
        
#         # Query the agent
#         logger.info(f"Processing query in session {session_id}: {request.query[:50]}...")
#         response_text, sources = query_agent(request.query, session_id)
        
#         # Store assistant response
#         session_manager.add_message(session_id, "assistant", response_text, sources)
        
#         return QueryResponse(
#             session_id=session_id,
#             query=request.query,
#             response=response_text,
#             sources=sources,
#             timestamp=datetime.now().isoformat()
#         )
    
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Error processing query: {e}")
#         raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

# @app.post("/chat", response_model=QueryResponse, tags=["Chat"])
# async def chat(request: QueryRequest):
#     """
#     Chat endpoint (alias for /query for compatibility)
#     """
#     return await query_documents(request)

# @app.post("/sessions", tags=["Sessions"])
# async def create_session():
#     """Create a new conversation session"""
#     session_id = session_manager.create_session()
#     return {
#         "session_id": session_id,
#         "status": "created",
#         "timestamp": datetime.now().isoformat()
#     }

# @app.get("/sessions", tags=["Sessions"])
# async def list_sessions():
#     """Get all sessions"""
#     sessions = session_manager.get_all_sessions()
#     return {
#         "sessions": sessions,
#         "total": len(sessions),
#         "timestamp": datetime.now().isoformat()
#     }

# @app.get("/sessions/{session_id}", response_model=SessionInfo, tags=["Sessions"])
# async def get_session(session_id: str):
#     """Get session information"""
#     session = session_manager.get_session(session_id)
    
#     if not session:
#         raise HTTPException(status_code=404, detail="Session not found")
    
#     return SessionInfo(
#         session_id=session_id,
#         created_at=session["created_at"],
#         last_message_at=session["last_message_at"],
#         message_count=len(session["messages"]),
#         status=session["status"]
#     )

# @app.get("/sessions/{session_id}/history", response_model=ConversationHistory, tags=["Sessions"])
# async def get_conversation_history(session_id: str):
#     """Get conversation history for a session"""
#     session = session_manager.get_session(session_id)
    
#     if not session:
#         raise HTTPException(status_code=404, detail="Session not found")
    
#     messages = [ChatMessage(**msg) for msg in session["messages"]]
    
#     return ConversationHistory(
#         session_id=session_id,
#         messages=messages,
#         created_at=session["created_at"],
#         total_messages=len(messages)
#     )

# @app.delete("/sessions/{session_id}", tags=["Sessions"])
# async def delete_session(session_id: str):
#     """Close/delete a session"""
#     if not session_manager.session_exists(session_id):
#         raise HTTPException(status_code=404, detail="Session not found")
    
#     session_manager.close_session(session_id)
    
#     return {
#         "session_id": session_id,
#         "status": "closed",
#         "timestamp": datetime.now().isoformat()
#     }

# @app.get("/stats", tags=["System"])
# async def get_stats():
#     """Get system statistics"""
#     all_sessions = session_manager.sessions
#     total_messages = sum(len(s["messages"]) for s in all_sessions.values())
#     active_sessions = sum(1 for s in all_sessions.values() if s["status"] == "active")
    
#     return {
#         "total_sessions": len(all_sessions),
#         "active_sessions": active_sessions,
#         "total_messages": total_messages,
#         "documents": ["LAW 243", "Banking & Insurance Law", "Oil & Gas Law"],
#         "timestamp": datetime.now().isoformat()
#     }

# #  WebSocket Support

# @app.websocket("/ws/{session_id}")
# async def websocket_endpoint(websocket: WebSocket, session_id: str):
#     """
#     WebSocket endpoint for real-time chat
    
#     Usage:
#         Connect to ws://localhost:8000/ws/{session_id}
#         Send: {"query": "Your question"}
#         Receive: {"response": "...", "sources": [...]}
#     """
#     # Validate or create session
#     if not session_manager.session_exists(session_id):
#         session_manager.sessions[session_id] = {
#             "created_at": datetime.now().isoformat(),
#             "last_message_at": datetime.now().isoformat(),
#             "messages": [],
#             "status": "active"
#         }
    
#     await websocket.accept()
#     logger.info(f"WebSocket connection established: {session_id}")
    
#     try:
#         while True:
#             # Receive message
#             data = await websocket.receive_text()
#             message = json.loads(data)
#             query = message.get("query")
            
#             if not query:
#                 await websocket.send_json({"error": "Query is required"})
#                 continue
            
#             # Store user query
#             session_manager.add_message(session_id, "user", query)
            
#             # Process query
#             try:
#                 response_text, sources = query_agent(query, session_id)
                
#                 # Store assistant response
#                 session_manager.add_message(session_id, "assistant", response_text, sources)
                
#                 # Send response
#                 await websocket.send_json({
#                     "response": response_text,
#                     "sources": sources,
#                     "timestamp": datetime.now().isoformat()
#                 })
            
#             except Exception as e:
#                 logger.error(f"Error processing WebSocket query: {e}")
#                 await websocket.send_json({"error": f"Error: {str(e)}"})
    
#     except WebSocketDisconnect:
#         logger.info(f"WebSocket disconnected: {session_id}")
#     except Exception as e:
#         logger.error(f"WebSocket error: {e}")


# #  Run Application
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         "backend:app",
#         host="127.0.0.1", 
#         port=8000,
#         reload=True,
#         log_level="info"
#     )

    
































from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import uuid
import json
import logging
import hashlib
import secrets

# Import the RAG agent from app.py
from app import query_agent, init_components

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend")

#  FastAPI Application
app = FastAPI(
    title="The Legal Vault NG",
    description="Agentic RAG system for querying Nigerian law documents with user authentication",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

#  Data Models

class UserRegistration(BaseModel):
    """Model for user registration"""
    email: EmailStr
    name: Optional[str] = None

class UserLogin(BaseModel):
    """Model for user login"""
    email: EmailStr
    session_id: str

class AuthResponse(BaseModel):
    """Model for authentication response"""
    session_id: str
    email: str
    name: Optional[str]
    token: str
    created_at: str
    message: str

class ChatMessage(BaseModel):
    """Model for a single chat message"""
    role: str
    content: str
    timestamp: str
    sources: Optional[List[str]] = []

class QueryRequest(BaseModel):
    """Model for incoming query request"""
    query: str

class QueryResponse(BaseModel):
    """Model for query response"""
    query: str
    response: str
    sources: List[str]
    timestamp: str

class UserInfo(BaseModel):
    """Model for user information"""
    email: str
    name: Optional[str]
    session_id: str
    created_at: str
    last_active: str
    message_count: int

class ConversationHistory(BaseModel):
    """Model for conversation history"""
    messages: List[ChatMessage]
    total_messages: int

#  User Management

class UserManager:
    """Manage user accounts and authentication"""
    
    def __init__(self):
        self.users: Dict[str, Dict] = {}  # email -> user_data
        self.sessions: Dict[str, str] = {}  # session_id -> email
        self.tokens: Dict[str, str] = {}  # token -> email
    
    def create_user(self, email: str, name: Optional[str] = None) -> tuple[str, str]:
        """
        Create a new user account
        
        Returns:
            tuple: (session_id, token)
        """
        # Check if user already exists
        if email in self.users:
            raise ValueError("User with this email already exists")
        
        # Generate unique session_id and token
        session_id = str(uuid.uuid4())
        token = secrets.token_urlsafe(32)
        
        # Create user
        self.users[email] = {
            "email": email,
            "name": name,
            "session_id": session_id,
            "token": token,
            "created_at": datetime.now().isoformat(),
            "last_active": datetime.now().isoformat(),
            "messages": []
        }
        
        # Map session and token to email
        self.sessions[session_id] = email
        self.tokens[token] = email
        
        logger.info(f"Created user: {email} with session: {session_id}")
        return session_id, token
    
    def login_user(self, email: str, session_id: str) -> str:
        """
        Login user with email and session_id
        
        Returns:
            str: authentication token
        """
        # Check if user exists
        if email not in self.users:
            raise ValueError("User not found")
        
        # Verify session_id
        user = self.users[email]
        if user["session_id"] != session_id:
            raise ValueError("Invalid session ID")
        
        # Generate new token for this login
        token = secrets.token_urlsafe(32)
        user["token"] = token
        user["last_active"] = datetime.now().isoformat()
        self.tokens[token] = email
        
        logger.info(f"User logged in: {email}")
        return token
    
    def verify_token(self, token: str) -> Optional[str]:
        """
        Verify authentication token
        
        Returns:
            str: email if valid, None otherwise
        """
        return self.tokens.get(token)
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user data by email"""
        return self.users.get(email)
    
    def get_user_by_token(self, token: str) -> Optional[Dict]:
        """Get user data by token"""
        email = self.tokens.get(token)
        if email:
            return self.users.get(email)
        return None
    
    def add_message(self, email: str, role: str, content: str, sources: Optional[List[str]] = None):
        """Add a message to user's conversation history"""
        if email not in self.users:
            return False
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "sources": sources or []
        }
        
        self.users[email]["messages"].append(message)
        self.users[email]["last_active"] = datetime.now().isoformat()
        return True
    
    def get_conversation_history(self, email: str) -> Optional[List[Dict]]:
        """Get all messages for a user"""
        if email not in self.users:
            return None
        return self.users[email]["messages"]
    
    def update_last_active(self, email: str):
        """Update user's last active timestamp"""
        if email in self.users:
            self.users[email]["last_active"] = datetime.now().isoformat()

# Initialize user manager
user_manager = UserManager()

#  Authentication Dependency

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependency to get current authenticated user
    
    Returns:
        str: user email
    """
    token = credentials.credentials
    email = user_manager.verify_token(token)
    
    if not email:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_manager.update_last_active(email)
    return email

#  Application Lifecycle

@app.on_event("startup")
async def startup_event():
    """Initialize the RAG system on startup"""
    logger.info(" Starting Nigerian Law RAG API...")
    try:
        init_components()
        logger.info(" RAG system initialized successfully")
    except Exception as e:
        logger.error(f" Failed to initialize RAG system: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Nigerian Law RAG API...")

#  API Endpoints

@app.get("/", tags=["Root"])
async def root():
    """API information and endpoints"""
    return {
        "service": "Nigerian Law RAG API",
        "version": "2.0.0",
        "description": "Agentic RAG for Constitutional, Banking/Insurance, and Oil & Gas Law with User Authentication",
        "status": "running",
        "endpoints": {
            "health": "GET /health",
            "register": "POST /auth/register",
            "login": "POST /auth/login",
            "user_info": "GET /auth/me",
            "query": "POST /query",
            "chat": "POST /chat",
            "history": "GET /history",
            "stats": "GET /stats",
            "websocket": "WS /ws"
        },
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Nigerian Law RAG API",
        "timestamp": datetime.now().isoformat()
    }

#  Authentication Endpoints

@app.post("register", response_model=AuthResponse, tags=["Authentication"])
async def register_user(registration: UserRegistration):
    """
    Register a new user account
    
    Args:
        registration: UserRegistration with email and optional name
    
    Returns:
        AuthResponse with session_id and token
    """
    try:
        session_id, token = user_manager.create_user(
            email=registration.email,
            name=registration.name
        )
        
        return AuthResponse(
            session_id=session_id,
            email=registration.email,
            name=registration.name,
            token=token,
            created_at=datetime.now().isoformat(),
            message="Account created successfully"
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail="Error creating account")

@app.post("login", response_model=AuthResponse, tags=["Authentication"])
async def login_user(login: UserLogin):
    """
    Login with email and session_id
    
    Args:
        login: UserLogin with email and session_id
    
    Returns:
        AuthResponse with new authentication token
    """
    try:
        token = user_manager.login_user(login.email, login.session_id)
        user = user_manager.get_user_by_email(login.email)
        
        return AuthResponse(
            session_id=user["session_id"],
            email=user["email"],
            name=user.get("name"),
            token=token,
            created_at=user["created_at"],
            message="Login successful"
        )
    
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Error logging in user: {e}")
        raise HTTPException(status_code=500, detail="Error logging in")

# @app.get("me", response_model=UserInfo, tags=["Authentication"])
# async def get_current_user_info(email: str = Depends(get_current_user)):
#     """
#     Get current user information
    
#     Returns:
#         UserInfo with user details
#     """
#     user = user_manager.get_user_by_email(email)
    
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     return UserInfo(
#         email=user["email"],
#         name=user.get("name"),
#         session_id=user["session_id"],
#         created_at=user["created_at"],
#         last_active=user["last_active"],
#         message_count=len(user["messages"])
#     )

#  Query Endpoints

@app.post("", response_model=QueryResponse, tags=["Query"])
async def query_documents(
    request: QueryRequest,
    email: str = Depends(get_current_user)
):
    """
    Query the Nigerian law documents
    
    Args:
        request: QueryRequest with query text
        email: Current user email (from token)
    
    Returns:
        QueryResponse with answer and sources
    """
    try:
        user = user_manager.get_user_by_email(email)
        session_id = user["session_id"]
        
        # Store user query
        user_manager.add_message(email, "user", request.query)
        
        # Query the agent
        logger.info(f"Processing query for user {email}: {request.query[:50]}...")
        response_text, sources = query_agent(request.query, session_id)
        
        # Store assistant response
        user_manager.add_message(email, "assistant", response_text, sources)
        
        return QueryResponse(
            query=request.query,
            response=response_text,
            sources=sources,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

# @app.post("/chat", response_model=QueryResponse, tags=["Chat"])
# async def chat(
#     request: QueryRequest,
#     email: str = Depends(get_current_user)
# ):
#     """
#     Chat endpoint (alias for /query)
#     """
#     return await query_documents(request, email)

@app.get("", response_model=ConversationHistory, tags=["History"])
async def get_conversation_history(email: str = Depends(get_current_user)):
    """
    Get conversation history for current user
    
    Returns:
        ConversationHistory with all messages
    """
    messages_data = user_manager.get_conversation_history(email)
    
    if messages_data is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    messages = [ChatMessage(**msg) for msg in messages_data]
    
    return ConversationHistory(
        messages=messages,
        total_messages=len(messages)
    )

# @app.delete("", tags=["History"])
# async def clear_conversation_history(email: str = Depends(get_current_user)):
#     """Clear conversation history for current user"""
#     user = user_manager.get_user_by_email(email)
    
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     user["messages"] = []
    
#     return {
#         "message": "Conversation history cleared",
#         "timestamp": datetime.now().isoformat()
#     }

@app.get("", tags=["System"])
async def get_stats(email: str = Depends(get_current_user)):
    """Get user statistics"""
    user = user_manager.get_user_by_email(email)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "message_count": len(user["messages"]),
        "user_since": user["created_at"],
        "last_active": user["last_active"],
        "documents": ["LAW 243", "Banking & Insurance Law", "Oil & Gas Law"],
        "timestamp": datetime.now().isoformat()
    }

#  WebSocket Support

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str):
    """
    WebSocket endpoint for real-time chat
    
    Usage:
        Connect to ws://localhost:8000/ws?token=YOUR_TOKEN
        Send: {"query": "Your question"}
        Receive: {"response": "...", "sources": [...]}
    """
    # Verify token
    email = user_manager.verify_token(token)
    if not email:
        await websocket.close(code=1008, reason="Invalid token")
        return
    
    user = user_manager.get_user_by_email(email)
    session_id = user["session_id"]
    
    await websocket.accept()
    logger.info(f"WebSocket connection established for user: {email}")
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            message = json.loads(data)
            query = message.get("query")
            
            if not query:
                await websocket.send_json({"error": "Query is required"})
                continue
            
            # Store user query
            user_manager.add_message(email, "user", query)
            
            # Process query
            try:
                response_text, sources = query_agent(query, session_id)
                
                # Store assistant response
                user_manager.add_message(email, "assistant", response_text, sources)
                
                # Send response
                await websocket.send_json({
                    "response": response_text,
                    "sources": sources,
                    "timestamp": datetime.now().isoformat()
                })
            
            except Exception as e:
                logger.error(f"Error processing WebSocket query: {e}")
                await websocket.send_json({"error": f"Error: {str(e)}"})
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for user: {email}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

#  Admin Endpoints (Optional)

# @app.get("/admin/users", tags=["Admin"])
# async def list_all_users():
#     """
#     List all users (for admin purposes)
#     Note: In production, this should be protected with admin authentication
#     """
#     users = []
#     for email, user_data in user_manager.users.items():
#         users.append({
#             "email": email,
#             "name": user_data.get("name"),
#             "session_id": user_data["session_id"],
#             "created_at": user_data["created_at"],
#             "last_active": user_data["last_active"],
#             "message_count": len(user_data["messages"])
#         })
    
#     return {
#         "users": users,
#         "total": len(users),
#         "timestamp": datetime.now().isoformat()
#     }

#  Run Application

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend:app",
        host="127.0.0.1", 
        port=8000,
        reload=True,
        log_level="info"
    )

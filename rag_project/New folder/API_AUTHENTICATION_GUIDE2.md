# Nigerian Law RAG API - Authentication Guide

## Overview

This API now includes user authentication with automatic session management. Users register with their email, receive a unique session ID, and use both to login and receive an authentication token.

## Key Changes

1. ✅ **Email-based registration** - Create account with email (and optional name)
2. ✅ **Automatic session ID generation** - No manual session creation needed
3. ✅ **Token-based authentication** - Secure JWT-like tokens for API access
4. ✅ **Login with email + session ID** - Use credentials to get access token
5. ✅ **Protected endpoints** - All query endpoints require authentication

## Authentication Flow

### 1. Register New Account

**Endpoint:** `POST /auth/register`

**Request:**
```json
{
  "email": "user@example.com",
  "name": "John Doe"  // optional
}
```

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "created_at": "2026-01-28T10:30:00",
  "message": "Account created successfully"
}
```

**Important:** Save both `session_id` and `token`. You'll need the session_id to login later.

### 2. Login to Existing Account

**Endpoint:** `POST /auth/login`

**Request:**
```json
{
  "email": "user@example.com",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "token": "new_token_here...",
  "created_at": "2026-01-28T10:30:00",
  "message": "Login successful"
}
```

### 3. Use Token for API Requests

All protected endpoints require the token in the Authorization header:

```
Authorization: Bearer YOUR_TOKEN_HERE
```

## API Endpoints

### Authentication Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/auth/register` | POST | No | Register new account |
| `/auth/login` | POST | No | Login to existing account |
| `/auth/me` | GET | Yes | Get current user info |

### Query Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/query` | POST | Yes | Query Nigerian law documents |
| `/chat` | POST | Yes | Alias for /query |
| `/history` | GET | Yes | Get conversation history |
| `/history` | DELETE | Yes | Clear conversation history |
| `/stats` | GET | Yes | Get user statistics |

### System Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/` | GET | No | API information |
| `/health` | GET | No | Health check |
| `/admin/users` | GET | No* | List all users |

*Note: In production, admin endpoints should be protected

### WebSocket Endpoint

| Endpoint | Protocol | Auth Required | Description |
|----------|----------|---------------|-------------|
| `/ws?token=YOUR_TOKEN` | WebSocket | Yes | Real-time chat |

## Usage Examples

### Python Example

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# 1. Register
response = requests.post(
    f"{BASE_URL}/auth/register",
    json={"email": "user@example.com", "name": "John Doe"}
)
data = response.json()
session_id = data["session_id"]
token = data["token"]

print(f"Session ID: {session_id}")
print(f"Token: {token}")

# Save these for future use!

# 2. Query (with token)
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(
    f"{BASE_URL}/query",
    json={"query": "What are the key provisions of Nigerian banking law?"},
    headers=headers
)
result = response.json()
print(f"Response: {result['response']}")
print(f"Sources: {result['sources']}")

# 3. Get conversation history
response = requests.get(f"{BASE_URL}/history", headers=headers)
history = response.json()
print(f"Total messages: {history['total_messages']}")

# 4. Login later (with email + session_id)
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "user@example.com", "session_id": session_id}
)
new_token = response.json()["token"]
print(f"New token: {new_token}")
```

### cURL Examples

#### Register
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "name": "John Doe"}'
```

#### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "session_id": "YOUR_SESSION_ID"}'
```

#### Query
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"query": "What is the Constitution Act?"}'
```

#### Get User Info
```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Get History
```bash
curl -X GET "http://localhost:8000/history" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### JavaScript/Fetch Example

```javascript
// 1. Register
const registerResponse = await fetch('http://localhost:8000/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    name: 'John Doe'
  })
});
const { session_id, token } = await registerResponse.json();

// Save session_id and token
localStorage.setItem('session_id', session_id);
localStorage.setItem('token', token);

// 2. Query
const queryResponse = await fetch('http://localhost:8000/query', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    query: 'What are the key provisions of Nigerian banking law?'
  })
});
const result = await queryResponse.json();
console.log(result);

// 3. Login (later)
const loginResponse = await fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    session_id: localStorage.getItem('session_id')
  })
});
const { token: newToken } = await loginResponse.json();
localStorage.setItem('token', newToken);
```

### WebSocket Example

```python
import asyncio
import websockets
import json

async def chat():
    token = "YOUR_TOKEN_HERE"
    uri = f"ws://localhost:8000/ws?token={token}"
    
    async with websockets.connect(uri) as websocket:
        # Send query
        await websocket.send(json.dumps({
            "query": "What is the Oil and Gas Act?"
        }))
        
        # Receive response
        response = await websocket.recv()
        data = json.loads(response)
        print(f"Response: {data['response']}")
        print(f"Sources: {data['sources']}")

asyncio.run(chat())
```

## Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "detail": "User with this email already exists"
}
```

#### 401 Unauthorized
```json
{
  "detail": "Invalid or expired token"
}
```

#### 404 Not Found
```json
{
  "detail": "User not found"
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Error processing query: ..."
}
```

## Security Best Practices

1. **Store credentials securely**: Never hardcode tokens in your application
2. **Use HTTPS in production**: Always use encrypted connections
3. **Rotate tokens**: Re-login periodically to get fresh tokens
4. **Validate input**: Always validate email addresses on the client side
5. **Handle errors**: Implement proper error handling for auth failures

## Data Persistence

⚠️ **Important:** The current implementation stores user data in memory. This means:
- All data is lost when the server restarts
- Not suitable for production use

For production, you should:
1. Use a database (PostgreSQL, MongoDB, etc.)
2. Implement proper password hashing (currently not needed as we use email + session_id)
3. Add token expiration and refresh mechanisms
4. Implement rate limiting
5. Add email verification

## Testing the API

You can test the API using:
1. **Swagger UI**: Visit `http://localhost:8000/docs`
2. **ReDoc**: Visit `http://localhost:8000/redoc`
3. **Postman**: Import the endpoints and test interactively
4. **Python scripts**: Use the examples above

## Migration from Old API

If you're migrating from the previous version:

### Before (Old API)
```python
# Manual session creation
response = requests.post(f"{BASE_URL}/sessions")
session_id = response.json()["session_id"]

# Query with session_id in body
response = requests.post(
    f"{BASE_URL}/query",
    json={"query": "...", "session_id": session_id}
)
```

### After (New API)
```python
# Register once
response = requests.post(
    f"{BASE_URL}/auth/register",
    json={"email": "user@example.com"}
)
token = response.json()["token"]

# Query with token in header
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(
    f"{BASE_URL}/query",
    json={"query": "..."},
    headers=headers
)
```

## Troubleshooting

### "Invalid or expired token"
- Make sure you're using the latest token from login/register
- Check that the Authorization header is correctly formatted
- Verify the token hasn't been corrupted

### "User with this email already exists"
- Use the login endpoint instead of register
- Or use a different email address

### "Invalid session ID"
- Make sure you saved the session_id from registration
- Verify you're using the correct session_id for the email

## Support

For issues or questions:
1. Check the API docs at `/docs`
2. Review the error messages carefully
3. Enable logging to see detailed error information

## Running the Server

```bash
# Install dependencies
pip install fastapi uvicorn pydantic[email]

# Run the server
python backend.py

# Or with uvicorn directly
uvicorn backend:app --host 127.0.0.1 --port 8000 --reload
```

Server will be available at: `http://localhost:8000`

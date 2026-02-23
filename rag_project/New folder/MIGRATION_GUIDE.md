# Migration Guide: Old API → New Authentication API

## Summary of Changes

### What Changed?
1. ✅ **Email-based user accounts** - Users now register with email
2. ✅ **Automatic session ID** - Generated during registration (no manual creation)
3. ✅ **Token-based authentication** - Secure Bearer tokens for API access
4. ✅ **Login system** - Use email + session_id to get access token

### What Was Removed?
1. ❌ Manual session creation (`POST /sessions`)
2. ❌ Session ID in request body
3. ❌ Public endpoints for queries (now require authentication)
4. ❌ Session listing endpoints

## Migration Steps

### Step 1: Update Client Code

#### Old API (Before)
```python
import requests

BASE_URL = "http://localhost:8000"

# Create session manually
response = requests.post(f"{BASE_URL}/sessions")
session_id = response.json()["session_id"]

# Query with session_id in body
response = requests.post(
    f"{BASE_URL}/query",
    json={
        "query": "What is Nigerian banking law?",
        "session_id": session_id
    }
)
result = response.json()
```

#### New API (After)
```python
import requests

BASE_URL = "http://localhost:8000"

# Register user (one-time)
response = requests.post(
    f"{BASE_URL}/auth/register",
    json={
        "email": "user@example.com",
        "name": "John Doe"
    }
)
data = response.json()
session_id = data["session_id"]  # Save this!
token = data["token"]

# Query with token in header
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(
    f"{BASE_URL}/query",
    json={"query": "What is Nigerian banking law?"},
    headers=headers
)
result = response.json()

# For future sessions, login with saved credentials
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={
        "email": "user@example.com",
        "session_id": session_id
    }
)
token = response.json()["token"]
```

### Step 2: Update Frontend Code

#### Old Frontend (Before)
```javascript
// Create session on app load
const createSession = async () => {
  const response = await fetch('http://localhost:8000/sessions', {
    method: 'POST'
  });
  const { session_id } = await response.json();
  localStorage.setItem('session_id', session_id);
  return session_id;
};

// Query
const query = async (text) => {
  const session_id = localStorage.getItem('session_id');
  const response = await fetch('http://localhost:8000/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: text,
      session_id: session_id
    })
  });
  return await response.json();
};
```

#### New Frontend (After)
```javascript
// Register (one-time)
const register = async (email, name) => {
  const response = await fetch('http://localhost:8000/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, name })
  });
  const data = await response.json();
  
  // Save credentials
  localStorage.setItem('email', data.email);
  localStorage.setItem('session_id', data.session_id);
  localStorage.setItem('token', data.token);
  
  return data;
};

// Login (returning users)
const login = async (email, session_id) => {
  const response = await fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, session_id })
  });
  const data = await response.json();
  
  // Save new token
  localStorage.setItem('token', data.token);
  
  return data;
};

// Query (with authentication)
const query = async (text) => {
  const token = localStorage.getItem('token');
  const response = await fetch('http://localhost:8000/query', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ query: text })
  });
  return await response.json();
};

// Check if user is logged in
const isAuthenticated = () => {
  return localStorage.getItem('token') !== null;
};

// Auto-login on app load
const initializeAuth = async () => {
  const email = localStorage.getItem('email');
  const session_id = localStorage.getItem('session_id');
  
  if (email && session_id) {
    try {
      await login(email, session_id);
      return true;
    } catch (error) {
      // Token expired or invalid, need to register again
      localStorage.clear();
      return false;
    }
  }
  return false;
};
```

### Step 3: Update WebSocket Connections

#### Old WebSocket (Before)
```javascript
const sessionId = localStorage.getItem('session_id');
const ws = new WebSocket(`ws://localhost:8000/ws/${sessionId}`);
```

#### New WebSocket (After)
```javascript
const token = localStorage.getItem('token');
const ws = new WebSocket(`ws://localhost:8000/ws?token=${token}`);
```

## API Endpoint Mapping

| Old Endpoint | New Endpoint | Notes |
|--------------|--------------|-------|
| `POST /sessions` | `POST /auth/register` | Now creates user account |
| `GET /sessions` | `GET /auth/me` | Get current user info |
| `GET /sessions/{id}` | `GET /auth/me` | Only current user |
| `DELETE /sessions/{id}` | `DELETE /history` | Clear conversation |
| `POST /query` | `POST /query` | Now requires auth header |
| `GET /sessions/{id}/history` | `GET /history` | Now requires auth header |

## Response Format Changes

### Registration Response
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

### Query Response
```json
{
  "query": "What is Nigerian banking law?",
  "response": "Nigerian banking law is...",
  "sources": ["source1.pdf", "source2.pdf"],
  "timestamp": "2026-01-28T10:30:00"
}
```
Note: `session_id` is no longer in the response

## Common Migration Issues

### Issue 1: 401 Unauthorized
**Problem:** Getting "Invalid or expired token" error

**Solution:** 
```python
# Make sure you're including the Authorization header
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(url, headers=headers, json=data)
```

### Issue 2: Missing Session ID
**Problem:** Lost session_id and can't login

**Solution:**
```python
# You'll need to register again with the same email
# Old session_id won't work - this creates a new account
response = requests.post(
    f"{BASE_URL}/auth/register",
    json={"email": "user@example.com"}
)
# Save the new session_id!
```

### Issue 3: 400 User Already Exists
**Problem:** Trying to register with existing email

**Solution:**
```python
# Use login endpoint instead
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={
        "email": "existing@example.com",
        "session_id": "your-saved-session-id"
    }
)
```

## Testing Your Migration

Use this checklist to ensure everything works:

- [ ] Can register new users
- [ ] Can login with email + session_id
- [ ] Can query with authentication token
- [ ] Can retrieve conversation history
- [ ] Can clear conversation history
- [ ] WebSocket connections work with token
- [ ] Error handling works correctly
- [ ] Token is stored securely
- [ ] Auto-login works on app reload

## Rollback Plan

If you need to rollback to the old API:

1. Keep a backup of the old `backend.py`
2. Test the new API in a staging environment first
3. Have a rollback script ready:
   ```bash
   # Restore old backend
   cp backend.py.backup backend.py
   
   # Restart server
   pkill -f "python backend.py"
   python backend.py &
   ```

## Production Considerations

Before deploying to production:

1. **Add Database**: Replace in-memory storage with PostgreSQL/MongoDB
2. **Add Token Expiration**: Implement JWT with expiration times
3. **Add Rate Limiting**: Prevent abuse
4. **Add Email Verification**: Verify email addresses
5. **Use HTTPS**: Always encrypt in production
6. **Add Password**: Consider adding password authentication
7. **Add Refresh Tokens**: For long-lived sessions

## Example Complete Migration

Here's a complete example showing before and after:

### Before (Old App)
```python
# app.py (old)
import requests

BASE_URL = "http://localhost:8000"

class ChatApp:
    def __init__(self):
        # Create session
        response = requests.post(f"{BASE_URL}/sessions")
        self.session_id = response.json()["session_id"]
    
    def ask(self, query):
        response = requests.post(
            f"{BASE_URL}/query",
            json={"query": query, "session_id": self.session_id}
        )
        return response.json()["response"]

app = ChatApp()
print(app.ask("What is banking law?"))
```

### After (New App)
```python
# app.py (new)
import requests

BASE_URL = "http://localhost:8000"

class ChatApp:
    def __init__(self, email, name=None):
        self.email = email
        self.session_id = None
        self.token = None
        
        # Try to load saved credentials
        if not self.load_credentials():
            # Register new user
            self.register(email, name)
    
    def register(self, email, name):
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json={"email": email, "name": name}
        )
        data = response.json()
        self.session_id = data["session_id"]
        self.token = data["token"]
        self.save_credentials()
    
    def login(self):
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": self.email, "session_id": self.session_id}
        )
        self.token = response.json()["token"]
        self.save_credentials()
    
    def ask(self, query):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(
            f"{BASE_URL}/query",
            json={"query": query},
            headers=headers
        )
        return response.json()["response"]
    
    def save_credentials(self):
        # Save to file or database
        with open("credentials.json", "w") as f:
            json.dump({
                "email": self.email,
                "session_id": self.session_id,
                "token": self.token
            }, f)
    
    def load_credentials(self):
        try:
            with open("credentials.json", "r") as f:
                data = json.load(f)
                self.email = data["email"]
                self.session_id = data["session_id"]
                self.token = data["token"]
                return True
        except FileNotFoundError:
            return False

# Usage
app = ChatApp("user@example.com", "John Doe")
print(app.ask("What is banking law?"))
```

## Need Help?

- Check the API documentation: `http://localhost:8000/docs`
- Read the authentication guide: `API_AUTHENTICATION_GUIDE.md`
- Run the test suite: `python test_api.py`
- Open an issue if you encounter problems

## Timeline

Recommended migration timeline:
1. **Week 1**: Test new API in development
2. **Week 2**: Update client code and test thoroughly
3. **Week 3**: Deploy to staging environment
4. **Week 4**: Monitor and fix issues
5. **Week 5**: Deploy to production

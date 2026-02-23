"""
Test script for the Nigerian Law RAG API with Authentication
Demonstrates the complete authentication and query flow
"""

import requests
import json
from typing import Dict, Optional

# Configuration
BASE_URL = "http://localhost:8000"

class LawRagClient:
    """Client for Nigerian Law RAG API"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.session_id: Optional[str] = None
        self.email: Optional[str] = None
    
    def register(self, email: str, name: Optional[str] = None) -> Dict:
        """Register a new user"""
        response = requests.post(
            f"{self.base_url}/auth/register",
            json={"email": email, "name": name}
        )
        
        if response.status_code == 200:
            data = response.json()
            self.token = data["token"]
            self.session_id = data["session_id"]
            self.email = data["email"]
            print(f"✅ Registration successful!")
            print(f"📧 Email: {data['email']}")
            print(f"🆔 Session ID: {data['session_id']}")
            print(f"🔑 Token: {data['token'][:20]}...")
            return data
        else:
            print(f"❌ Registration failed: {response.json()}")
            return response.json()
    
    def login(self, email: str, session_id: str) -> Dict:
        """Login with email and session_id"""
        response = requests.post(
            f"{self.base_url}/auth/login",
            json={"email": email, "session_id": session_id}
        )
        
        if response.status_code == 200:
            data = response.json()
            self.token = data["token"]
            self.session_id = data["session_id"]
            self.email = data["email"]
            print(f"✅ Login successful!")
            print(f"🔑 New token: {data['token'][:20]}...")
            return data
        else:
            print(f"❌ Login failed: {response.json()}")
            return response.json()
    
    def get_user_info(self) -> Dict:
        """Get current user information"""
        if not self.token:
            print("❌ Not authenticated. Please login first.")
            return {}
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.base_url}/auth/me", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"👤 User Info:")
            print(f"   Email: {data['email']}")
            print(f"   Name: {data.get('name', 'N/A')}")
            print(f"   Session ID: {data['session_id']}")
            print(f"   Messages: {data['message_count']}")
            return data
        else:
            print(f"❌ Failed to get user info: {response.json()}")
            return response.json()
    
    def query(self, query_text: str) -> Dict:
        """Query the Nigerian law documents"""
        if not self.token:
            print("❌ Not authenticated. Please login first.")
            return {}
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(
            f"{self.base_url}/query",
            json={"query": query_text},
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n💬 Query: {data['query']}")
            print(f"\n📝 Response: {data['response'][:200]}...")
            print(f"\n📚 Sources: {', '.join(data['sources'][:3])}")
            return data
        else:
            print(f"❌ Query failed: {response.json()}")
            return response.json()
    
    def get_history(self) -> Dict:
        """Get conversation history"""
        if not self.token:
            print("❌ Not authenticated. Please login first.")
            return {}
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.base_url}/history", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📜 Conversation History ({data['total_messages']} messages):")
            for i, msg in enumerate(data['messages'][-5:], 1):  # Show last 5
                role_emoji = "👤" if msg['role'] == 'user' else "🤖"
                print(f"   {role_emoji} {msg['role']}: {msg['content'][:80]}...")
            return data
        else:
            print(f"❌ Failed to get history: {response.json()}")
            return response.json()
    
    def clear_history(self) -> Dict:
        """Clear conversation history"""
        if not self.token:
            print("❌ Not authenticated. Please login first.")
            return {}
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.delete(f"{self.base_url}/history", headers=headers)
        
        if response.status_code == 200:
            print("✅ Conversation history cleared")
            return response.json()
        else:
            print(f"❌ Failed to clear history: {response.json()}")
            return response.json()
    
    def get_stats(self) -> Dict:
        """Get user statistics"""
        if not self.token:
            print("❌ Not authenticated. Please login first.")
            return {}
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.base_url}/stats", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📊 Statistics:")
            print(f"   Messages: {data['message_count']}")
            print(f"   User since: {data['user_since']}")
            print(f"   Documents: {', '.join(data['documents'])}")
            return data
        else:
            print(f"❌ Failed to get stats: {response.json()}")
            return response.json()


def test_complete_flow():
    """Test the complete authentication and query flow"""
    print("=" * 60)
    print("🧪 Testing Nigerian Law RAG API - Authentication Flow")
    print("=" * 60)
    
    client = LawRagClient()
    
    # Test 1: Health check
    print("\n1️⃣ Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"✅ Health check: {response.json()['status']}")
    
    # Test 2: Register new user
    print("\n2️⃣ Registering new user...")
    email = f"test_user_{requests.utils.uuid4().hex[:8]}@example.com"
    client.register(email=email, name="Test User")
    
    # Save credentials for later
    saved_session_id = client.session_id
    
    # Test 3: Get user info
    print("\n3️⃣ Getting user info...")
    client.get_user_info()
    
    # Test 4: Query documents
    print("\n4️⃣ Querying Nigerian law documents...")
    client.query("What are the key provisions of Nigerian banking law?")
    
    # Test 5: Another query
    print("\n5️⃣ Another query...")
    client.query("Explain the regulatory framework for insurance companies in Nigeria")
    
    # Test 6: Get conversation history
    print("\n6️⃣ Getting conversation history...")
    client.get_history()
    
    # Test 7: Get statistics
    print("\n7️⃣ Getting statistics...")
    client.get_stats()
    
    # Test 8: Logout and login again
    print("\n8️⃣ Testing login with saved credentials...")
    client.token = None  # Simulate logout
    client.login(email=email, session_id=saved_session_id)
    
    # Test 9: Verify session persisted
    print("\n9️⃣ Verifying session persisted after login...")
    client.get_history()
    
    # Test 10: Clear history
    print("\n🔟 Clearing conversation history...")
    client.clear_history()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed successfully!")
    print("=" * 60)
    
    return client


def test_error_handling():
    """Test error handling"""
    print("\n" + "=" * 60)
    print("🧪 Testing Error Handling")
    print("=" * 60)
    
    client = LawRagClient()
    
    # Test 1: Query without authentication
    print("\n1️⃣ Testing query without authentication...")
    client.query("What is the Constitution Act?")
    
    # Test 2: Register duplicate email
    print("\n2️⃣ Testing duplicate registration...")
    email = "duplicate@example.com"
    client.register(email=email, name="First User")
    client2 = LawRagClient()
    client2.register(email=email, name="Second User")
    
    # Test 3: Login with wrong session_id
    print("\n3️⃣ Testing login with wrong session_id...")
    client3 = LawRagClient()
    client3.login(email=email, session_id="wrong-session-id")
    
    print("\n" + "=" * 60)
    print("✅ Error handling tests completed!")
    print("=" * 60)


def interactive_demo():
    """Interactive demo of the API"""
    print("\n" + "=" * 60)
    print("🎮 Interactive Nigerian Law RAG API Demo")
    print("=" * 60)
    
    client = LawRagClient()
    
    # Register or login
    print("\n📝 Choose an option:")
    print("1. Register new account")
    print("2. Login to existing account")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        email = input("Enter your email: ").strip()
        name = input("Enter your name (optional): ").strip() or None
        client.register(email=email, name=name)
        print(f"\n⚠️ IMPORTANT: Save your Session ID: {client.session_id}")
        print("You'll need this to login later!")
    
    elif choice == "2":
        email = input("Enter your email: ").strip()
        session_id = input("Enter your session ID: ").strip()
        client.login(email=email, session_id=session_id)
    
    else:
        print("Invalid choice!")
        return
    
    # Interactive query loop
    print("\n" + "=" * 60)
    print("💬 You can now ask questions about Nigerian law")
    print("Commands: 'history', 'stats', 'clear', 'quit'")
    print("=" * 60)
    
    while True:
        query = input("\n🤔 Your question: ").strip()
        
        if not query:
            continue
        
        if query.lower() == 'quit':
            print("👋 Goodbye!")
            break
        
        elif query.lower() == 'history':
            client.get_history()
        
        elif query.lower() == 'stats':
            client.get_stats()
        
        elif query.lower() == 'clear':
            client.clear_history()
        
        elif query.lower() == 'info':
            client.get_user_info()
        
        else:
            client.query(query)


if __name__ == "__main__":
    import sys
    
    print("\n🚀 Nigerian Law RAG API - Test Suite\n")
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        print(f"✅ Server is running at {BASE_URL}\n")
    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Server is not running at {BASE_URL}")
        print("Please start the server first: python backend.py")
        sys.exit(1)
    
    # Run tests based on command line argument
    if len(sys.argv) > 1:
        if sys.argv[1] == "demo":
            interactive_demo()
        elif sys.argv[1] == "errors":
            test_error_handling()
        else:
            print("Usage: python test_api.py [demo|errors]")
    else:
        # Run complete test flow
        test_complete_flow()
        
        print("\n💡 Tips:")
        print("   - Run 'python test_api.py demo' for interactive demo")
        print("   - Run 'python test_api.py errors' to test error handling")
        print("   - Check API docs at http://localhost:8000/docs")

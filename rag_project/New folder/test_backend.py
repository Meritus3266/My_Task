"""
Simple Test Client for Nigerian Law RAG API
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_create_session():
    """Test session creation"""
    print("\n" + "="*60)
    print("TEST 2: Create Session")
    print("="*60)
    
    response = requests.post(f"{BASE_URL}/sessions")
    data = response.json()
    session_id = data["session_id"]
    
    print(f"Status: {response.status_code}")
    print(f"Session ID: {session_id}")
    
    return session_id

def test_query(session_id):
    """Test document query"""
    print("\n" + "="*60)
    print("TEST 3: Query Documents")
    print("="*60)
    
    query = "What is LAW 243 about?"
    print(f"Query: {query}\n")
    
    payload = {
        "query": query,
        "session_id": session_id
    }
    
    response = requests.post(f"{BASE_URL}/query", json=payload)
    data = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"\nResponse:\n{data['response'][:500]}...")
    print(f"\nSources: {data['sources']}")

def test_follow_up(session_id):
    """Test follow-up query"""
    print("\n" + "="*60)
    print("TEST 4: Follow-up Query")
    print("="*60)
    
    query = "What are the main topics covered?"
    print(f"Query: {query}\n")
    
    payload = {
        "query": query,
        "session_id": session_id
    }
    
    response = requests.post(f"{BASE_URL}/query", json=payload)
    data = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"\nResponse:\n{data['response'][:500]}...")

def test_history(session_id):
    """Test conversation history"""
    print("\n" + "="*60)
    print("TEST 5: Conversation History")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/sessions/{session_id}/history")
    data = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Total Messages: {data['total_messages']}")
    print("\nMessages:")
    
    for i, msg in enumerate(data['messages'], 1):
        print(f"\n{i}. {msg['role'].upper()}:")
        print(f"   {msg['content'][:100]}...")

def test_stats():
    """Test system statistics"""
    print("\n" + "="*60)
    print("TEST 6: System Statistics")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/stats")
    data = response.json()
    
    print(f"Status: {response.status_code}")
    print(json.dumps(data, indent=2))

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("  Nigerian Law RAG API - Test Suite")
    print("="*60)
    
    try:
        # Test 1: Health
        test_health()
        
        # Test 2: Create session
        session_id = test_create_session()
        
        # Test 3: First query
        test_query(session_id)
        
        # Test 4: Follow-up
        test_follow_up(session_id)
        
        # Test 5: History
        test_history(session_id)
        
        # Test 6: Stats
        test_stats()
        
        print("\n" + "="*60)
        print("   All Tests Completed Successfully!")
        print("="*60 + "\n")
    
    except requests.exceptions.ConnectionError:
        print("\n Error: Cannot connect to the API")
        print("Make sure the server is running:")
        print("  python backend.py")
        print("  or")
        print("  uvicorn backend:app --reload")
    except Exception as e:
        print(f"\n Error: {e}")

if __name__ == "__main__":
    run_all_tests()
#!/usr/bin/env python3
"""
Quick Start Script for Nigerian Law RAG System
Handles initialization and server startup
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    print("\n" + "="*70)
    print("  Nigerian Law RAG System - Quick Start")
    print("="*70 + "\n")

def check_env_file():
    """Check if .env file exists"""
    if not Path(".env").exists():
        print(" .env file not found!")
        print("\n Creating .env file...")
        
        with open(".env", "w") as f:
            f.write("""# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# LLM Configuration
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small

# Document Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=150
RETRIEVER_K=4

# Server Configuration
HOST=0.0.0.0
PORT=8000
""")
        
        print(" .env file created")
        print("\n  IMPORTANT: Please edit .env and add your OpenAI API key!")
        print("   Then run this script again.\n")
        sys.exit(0)
    
    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print(" OpenAI API key not set!")
        print("\n  Please edit .env and add your OpenAI API key")
        print("   Then run this script again.\n")
        sys.exit(1)
    
    print(" Environment configured")

def check_documents():
    """Check if documents folder exists"""
    docs_path = Path("documents")
    
    if not docs_path.exists():
        print(" Creating documents folder...")
        docs_path.mkdir(parents=True, exist_ok=True)
        print(" Documents folder created")
    
    # Check for PDF files
    pdf_files = list(docs_path.glob("*.pdf"))
    
    if not pdf_files:
        print("\n  No PDF documents found in documents/ folder")
        print("   Please add your PDF files before continuing.")
        
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Exiting...")
            sys.exit(0)
    else:
        print(f" Found {len(pdf_files)} PDF document(s)")

def check_vector_db():
    """Check if vector database exists"""
    chroma_path = Path("chroma_db")
    
    if not chroma_path.exists() or not any(chroma_path.iterdir()):
        print("\n Vector database not found")
        print("   Initializing vector database...")
        
        try:
            # Initialize database
            subprocess.run([sys.executable, "app.py", "--init-db"], check=True)
            print(" Vector database initialized")
        except subprocess.CalledProcessError as e:
            print(f" Error initializing database: {e}")
            sys.exit(1)
    else:
        print(" Vector database found")

def start_server():
    """Start the FastAPI server"""
    print("\n" + "="*70)
    print("  Starting FastAPI Server")
    print("="*70)
    print("\n Server will be available at:")
    print("   • API Docs:  http://localhost:8000/docs")
    print("   • ReDoc:     http://localhost:8000/redoc")
    print("   • Base URL:  http://localhost:8000")
    print("\n  Press Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    try:
        # Start uvicorn server
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "backend:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n\n Server stopped. Goodbye!")
    except Exception as e:
        print(f"\n Error starting server: {e}")
        sys.exit(1)

def main():
    """Main function"""
    print_banner()
    
    print(" Checking prerequisites...\n")
    
    # Check environment
    check_env_file()
    
    # Check documents
    check_documents()
    
    # Check/initialize vector database
    check_vector_db()
    
    print("\n" + "="*70)
    print("   All checks passed!")
    print("="*70)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
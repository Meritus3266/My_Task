# #!/usr/bin/env python3
# """
# Agentic RAG System for Nigerian Law Documents
# --------------------------------------------
# Query constitutional law, banking & insurance law, oil & gas law documents.

# Usage:
#     python app.py --init-db                # Only build vector store (one-time)
#     python app.py --interactive             # Start chat interface
#     python app.py --query "What is LAW 243?" # One-shot query
#     python app.py --help
# """

# import argparse
# import os
# import sys
# import logging
# from pathlib import Path
# from typing import List, Optional

# from dotenv import load_dotenv

# # LangChain / LangGraph imports
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_chroma import Chroma
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_core.tools import tool
# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.graph import START, END, StateGraph
# from langgraph.prebuilt import create_react_agent, ToolNode

# # ──────────────────────────────────────────────────────────────────────────────
# #  Configuration & Constants
# # ──────────────────────────────────────────────────────────────────────────────

# load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# if not OPENAI_API_KEY:
#     print("Error: OPENAI_API_KEY not found in environment or .env file", file=sys.stderr)
#     sys.exit(1)

# # ─── Paths ───────────────────────────────────────────────────────────────────
# BASE_DIR = Path(__file__).resolve().parent
# CHROMA_DIR = BASE_DIR / "chroma_db"
# PDF_FOLDER = BASE_DIR

# PDF_FILES = [
#     "LAW 243.pdf",
#     "law 432 LAW OF BANKING AND INSURANCE II  post editorial.pdf",
#     "LAW411 oil and gas I.pdf",
# ]

# # ─── Model settings ──────────────────────────────────────────────────────────
# LLM_MODEL = "gpt-4o-mini"
# EMBEDDING_MODEL = "text-embedding-3-small"
# CHUNK_SIZE = 1000
# CHUNK_OVERLAP = 150
# RETRIEVER_K = 4

# # ─── Logging ─────────────────────────────────────────────────────────────────
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s | %(levelname)-7s | %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
# )
# logger = logging.getLogger("legal-rag")


# # ──────────────────────────────────────────────────────────────────────────────
# #  Tools
# # ──────────────────────────────────────────────────────────────────────────────

# @tool
# def search_documents(query: str) -> str:
#     """Search the Nigerian law documents (Constitutional, Banking/Insurance, Oil & Gas)."""
#     docs = retriever.invoke(query)

#     if not docs:
#         return "No relevant information found in the documents."

#     results = []
#     for i, doc in enumerate(docs, 1):
#         source = Path(doc.metadata.get("source", "unknown")).name
#         page = doc.metadata.get("page", "n/a")
#         content = doc.page_content.strip()
#         results.append(f"[Source {i}: {source} (page {page})]\n{content}\n")

#     return "\n" + "-" * 60 + "\n".join(results)


# # ──────────────────────────────────────────────────────────────────────────────
# #  Initialization Functions
# # ──────────────────────────────────────────────────────────────────────────────

# def load_and_split_documents() -> List:
#     """Load all PDFs and split them into chunks."""
#     if not PDF_FILES:
#         logger.error("No PDF files defined")
#         sys.exit(1)

#     all_pages = []

#     for filename in PDF_FILES:
#         path = PDF_FOLDER / filename
#         if not path.is_file():
#             logger.warning(f"File not found → {path}")
#             continue

#         try:
#             loader = PyPDFLoader(str(path))
#             pages = loader.load()
#             all_pages.extend(pages)
#             logger.info(f"Loaded {len(pages):3d} pages from {filename}")
#         except Exception as e:
#             logger.error(f"Failed to load {filename}: {e}")

#     if not all_pages:
#         logger.error("No pages were loaded from any PDF")
#         sys.exit(1)

#     logger.info(f"Total pages loaded: {len(all_pages)}")

#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=CHUNK_SIZE,
#         chunk_overlap=CHUNK_OVERLAP,
#         separators=["\n\n", "\n", ".", " ", ""],
#         length_function=len,
#     )

#     chunks = text_splitter.split_documents(all_pages)
#     logger.info(f"Created {len(chunks)} chunks (avg ~{CHUNK_SIZE} chars)")

#     return chunks


# def build_vector_store(chunks):
#     """Create or load Chroma vector database."""
#     if CHROMA_DIR.exists() and any(CHROMA_DIR.iterdir()):
#         logger.info("Loading existing Chroma database...")
#         vector_store = Chroma(
#             persist_directory=str(CHROMA_DIR),
#             embedding_function=OpenAIEmbeddings(model=EMBEDDING_MODEL),
#         )
#     else:
#         logger.info("Creating new vector database...")
#         embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
#         vector_store = Chroma.from_documents(
#             documents=chunks,
#             embedding=embeddings,
#             persist_directory=str(CHROMA_DIR),
#         )
#         logger.info("Vector store created and persisted")

#     return vector_store


# # ──────────────────────────────────────────────────────────────────────────────
# #  Global components (lazy init)
# # ──────────────────────────────────────────────────────────────────────────────

# llm = None
# vector_store = None
# retriever = None
# agent_executor = None
# compiled_agent = None


# def init_components(force_rebuild: bool = False):
#     global llm, vector_store, retriever, agent_executor, compiled_agent

#     llm = ChatOpenAI(model=LLM_MODEL, temperature=0.3)

#     if force_rebuild or not CHROMA_DIR.exists() or not any(CHROMA_DIR.iterdir()):
#         chunks = load_and_split_documents()
#         vector_store = build_vector_store(chunks)
#     else:
#         vector_store = build_vector_store([])  # load only

#     retriever = vector_store.as_retriever(search_kwargs={"k": RETRIEVER_K})

#     tools = [search_documents]

#     # Simple ReAct agent
#     agent_executor = create_react_agent(llm, tools)

#     # Graph with memory
#     class AgentState(dict):
#         messages: List

#     def agent_node(state: AgentState):
#         sys_msg = SystemMessage(content="""You are a precise legal assistant answering questions 
# about Nigerian law documents (Constitutional Law, Banking & Insurance, Oil & Gas).
# Always search documents before answering.
# Cite sources clearly using the format found in search_documents results.
# Be concise, accurate and professional.""")
#         msgs = [sys_msg] + state["messages"]
#         result = agent_executor.invoke({"messages": msgs})
#         return {"messages": state["messages"] + [result["messages"][-1]]}

#     workflow = StateGraph(AgentState)
#     workflow.add_node("agent", agent_node)
#     workflow.add_edge(START, "agent")
#     workflow.add_edge("agent", END)

#     memory = MemorySaver()
#     compiled_agent = workflow.compile(checkpointer=memory)


# # ──────────────────────────────────────────────────────────────────────────────
# #  Query & Chat Interface
# # ──────────────────────────────────────────────────────────────────────────────

# def run_query(query: str, thread_id: str = "default") -> str:
#     if compiled_agent is None:
#         init_components()

#     input_state = {"messages": [HumanMessage(content=query)]}

#     config = {"configurable": {"thread_id": thread_id}}

#     result = compiled_agent.invoke(input_state, config=config)

#     return result["messages"][-1].content.strip()


# def interactive_mode():
#     print("\n" + "═" * 70)
#     print("  Nigerian Law RAG Chat  (type 'quit' or 'exit' to leave)")
#     print("═" * 70 + "\n")

#     thread_id = "interactive_1"
#     counter = 1

#     while True:
#         try:
#             user_input = input("You: ").strip()
#             if user_input.lower() in ("quit", "exit", "q"):
#                 print("\nGoodbye.\n")
#                 break

#             if user_input.lower() == "new":
#                 counter += 1
#                 thread_id = f"interactive_{counter}"
#                 print(f"\nStarted new conversation: {thread_id}\n")
#                 continue

#             if not user_input:
#                 continue

#             print("\nThinking...\n")
#             answer = run_query(user_input, thread_id)
#             print("Assistant:")
#             print(answer)
#             print("\n" + "─" * 70 + "\n")

#         except KeyboardInterrupt:
#             print("\n\nInterrupted. Goodbye.")
#             break
#         except Exception as e:
#             print(f"\nError: {e}\n")


# def main():
#     parser = argparse.ArgumentParser(description="Agentic RAG over Nigerian Law PDFs")
#     parser.add_argument("--init-db", action="store_true", help="Build vector database only")
#     parser.add_argument("--interactive", action="store_true", help="Start interactive chat")
#     parser.add_argument("--query", type=str, help="Run single query and exit")
#     parser.add_argument("--thread", type=str, default="cli", help="Thread/conversation ID")
#     parser.add_argument("--rebuild", action="store_true", help="Force rebuild vector DB")

#     args = parser.parse_args()

#     # Initialize once
#     init_components(force_rebuild=args.rebuild)

#     if args.init_db:
#         logger.info("Vector database initialization complete. Exiting.")
#         return

#     if args.query:
#         answer = run_query(args.query, args.thread)
#         print(answer)
#         return

#     if args.interactive or len(sys.argv) == 1:
#         interactive_mode()
#         return

#     parser.print_help()


# if __name__ == "__main__":
#     main()







#!/usr/bin/env python3
"""
Agentic RAG System for Nigerian Law Documents
--------------------------------------------
Query constitutional law, banking & insurance law, oil & gas law documents.

Usage:
    python app.py --init-db                # Only build vector store (one-time)
    python app.py --interactive             # Start chat interface
    python app.py --query "What is LAW 243?" # One-shot query
    python app.py --help
"""

import argparse
import os
import sys
import logging
from pathlib import Path
from typing import List, Optional, Dict, TypedDict

from dotenv import load_dotenv

# LangChain / LangGraph imports
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import create_react_agent


#  Configuration & Constants


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY not found in environment or .env file", file=sys.stderr)
    sys.exit(1)

#  Paths 
BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = BASE_DIR / "chroma_db"
PDF_FOLDER = BASE_DIR / "documents"  # Fixed: Use documents folder

PDF_FILES = [
    "LAW 243.pdf",
    "law 432 LAW OF BANKING AND INSURANCE II  post editorial.pdf",
    "LAW411 oil and gas I.pdf",
]

#  Model settings 
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))
RETRIEVER_K = int(os.getenv("RETRIEVER_K", "4"))

#  Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("legal-rag")



#  State Definition


class AgentState(TypedDict):
    """State schema for the agent graph"""
    messages: List[BaseMessage]



#  Tools


# Global retriever (will be initialized)
retriever = None

@tool
def search_documents(query: str) -> str:
    """Search the Nigerian law documents (Constitutional, Banking/Insurance, Oil & Gas)."""
    if retriever is None:
        return "Error: Document retriever not initialized"
    
    try:
        docs = retriever.invoke(query)

        if not docs:
            return "No relevant information found in the documents."

        results = []
        for i, doc in enumerate(docs, 1):
            source = Path(doc.metadata.get("source", "unknown")).name
            page = doc.metadata.get("page", "n/a")
            content = doc.page_content.strip()
            results.append(f"[Source {i}: {source} (page {page})]\n{content}\n")

        return "\n" + "-" * 60 + "\n".join(results)
    except Exception as e:
        logger.error(f"Error in search_documents: {e}")
        return f"Error searching documents: {str(e)}"



#  Initialization Functions


def load_and_split_documents() -> List:
    """Load all PDFs and split them into chunks."""
    if not PDF_FILES:
        logger.error("No PDF files defined")
        sys.exit(1)

    # Create documents folder if it doesn't exist
    PDF_FOLDER.mkdir(parents=True, exist_ok=True)

    all_pages = []

    for filename in PDF_FILES:
        path = PDF_FOLDER / filename
        if not path.is_file():
            logger.warning(f"File not found → {path}")
            continue

        try:
            loader = PyPDFLoader(str(path))
            pages = loader.load()
            all_pages.extend(pages)
            logger.info(f"Loaded {len(pages):3d} pages from {filename}")
        except Exception as e:
            logger.error(f"Failed to load {filename}: {e}")

    if not all_pages:
        logger.error("No pages were loaded from any PDF")
        logger.error(f"Please place PDF files in: {PDF_FOLDER}")
        sys.exit(1)

    logger.info(f"Total pages loaded: {len(all_pages)}")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""],
        length_function=len,
    )

    chunks = text_splitter.split_documents(all_pages)
    logger.info(f"Created {len(chunks)} chunks (avg ~{CHUNK_SIZE} chars)")

    return chunks


def build_vector_store(chunks):
    """Create or load Chroma vector database."""
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    
    if CHROMA_DIR.exists() and any(CHROMA_DIR.iterdir()):
        logger.info("Loading existing Chroma database...")
        try:
            vector_store = Chroma(
                persist_directory=str(CHROMA_DIR),
                embedding_function=embeddings,
            )
            # Verify it has documents
            count = vector_store._collection.count()
            logger.info(f"Loaded vector store with {count} documents")
            return vector_store
        except Exception as e:
            logger.warning(f"Error loading existing database: {e}")
            logger.info("Creating new database...")
    
    # Create new database
    if not chunks:
        logger.error("No chunks provided for new database creation")
        sys.exit(1)
    
    logger.info("Creating new vector database...")
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
    )
    logger.info("Vector store created and persisted")

    return vector_store



#  Global components (lazy init)


llm = None
vector_store = None
agent_executor = None
compiled_agent = None


def init_components(force_rebuild: bool = False):
    """Initialize all system components"""
    global llm, vector_store, retriever, agent_executor, compiled_agent

    logger.info("Initializing components...")
    
    # Initialize LLM
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0.3)
    logger.info(f"LLM initialized: {LLM_MODEL}")

    # Initialize or load vector store
    if force_rebuild or not CHROMA_DIR.exists() or not any(CHROMA_DIR.iterdir()):
        chunks = load_and_split_documents()
        vector_store = build_vector_store(chunks)
    else:
        # Load existing with empty chunks list
        vector_store = build_vector_store([])

    # Create retriever
    retriever = vector_store.as_retriever(search_kwargs={"k": RETRIEVER_K})
    logger.info(f"Retriever configured (k={RETRIEVER_K})")

    # Create tools
    tools = [search_documents]

    # Create ReAct agent
    agent_executor = create_react_agent(llm, tools)
    logger.info("ReAct agent created")

    # Build graph with memory
    def agent_node(state: AgentState) -> AgentState:
        """Agent node that processes messages"""
        sys_msg = SystemMessage(content="""You are a precise legal assistant answering questions 
about Nigerian law documents (Constitutional Law, Banking & Insurance, Oil & Gas).
Always search documents before answering.
Cite sources clearly using the format found in search_documents results.
Be concise, accurate and professional.""")
        
        msgs = [sys_msg] + state["messages"]
        result = agent_executor.invoke({"messages": msgs})
        return {"messages": result["messages"]}

    # Create workflow
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent_node)
    workflow.add_edge(START, "agent")
    workflow.add_edge("agent", END)

    # Compile with memory
    memory = MemorySaver()
    compiled_agent = workflow.compile(checkpointer=memory)
    logger.info("Agent workflow compiled with memory")
    
    logger.info(" All components initialized successfully")



#  Query & Chat Interface


def run_query(query: str, thread_id: str = "default") -> str:
    """Run a single query through the agent"""
    if compiled_agent is None:
        init_components()

    input_state = {"messages": [HumanMessage(content=query)]}
    config = {"configurable": {"thread_id": thread_id}}

    try:
        result = compiled_agent.invoke(input_state, config=config)
        return result["messages"][-1].content.strip()
    except Exception as e:
        logger.error(f"Error running query: {e}")
        return f"Error: {str(e)}"


def interactive_mode():
    """Interactive chat mode"""
    print("\n" + "═" * 70)
    print("  Nigerian Law RAG Chat  (type 'quit' or 'exit' to leave)")
    print("═" * 70 + "\n")

    thread_id = "interactive_1"
    counter = 1

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ("quit", "exit", "q"):
                print("\nGoodbye.\n")
                break

            if user_input.lower() == "new":
                counter += 1
                thread_id = f"interactive_{counter}"
                print(f"\n✓ Started new conversation: {thread_id}\n")
                continue

            if not user_input:
                continue

            print("\n🔍 Thinking...\n")
            answer = run_query(user_input, thread_id)
            print("Assistant:")
            print(answer)
            print("\n" + "─" * 70 + "\n")

        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye.")
            break
        except Exception as e:
            logger.error(f"Error in interactive mode: {e}")
            print(f"\nError: {e}\n")



#  Public API (for FastAPI integration)


def get_agent():
    """Get or initialize the compiled agent"""
    global compiled_agent
    if compiled_agent is None:
        init_components()
    return compiled_agent


def query_agent(query: str, session_id: str) -> tuple:
    """
    Query the agent and return response with sources
    Returns: (response_text, sources_list)
    """
    if compiled_agent is None:
        init_components()
    
    try:
        response = run_query(query, thread_id=session_id)
        
        # Extract sources from response if present
        sources = []
        if "[Source" in response:
            # Parse sources from the response
            import re
            source_pattern = r'\[Source \d+: ([^\]]+)\]'
            matches = re.findall(source_pattern, response)
            sources = matches
        
        return response, sources
    except Exception as e:
        logger.error(f"Error in query_agent: {e}")
        return f"Error: {str(e)}", []



#  Main CLI


def main():
    parser = argparse.ArgumentParser(description="Agentic RAG over Nigerian Law PDFs")
    parser.add_argument("--init-db", action="store_true", help="Build vector database only")
    parser.add_argument("--interactive", action="store_true", help="Start interactive chat")
    parser.add_argument("--query", type=str, help="Run single query and exit")
    parser.add_argument("--thread", type=str, default="cli", help="Thread/conversation ID")
    parser.add_argument("--rebuild", action="store_true", help="Force rebuild vector DB")

    args = parser.parse_args()

    # Initialize once
    init_components(force_rebuild=args.rebuild)

    if args.init_db:
        logger.info("Vector database initialization complete. Exiting.")
        return

    if args.query:
        answer = run_query(args.query, args.thread)
        print("\nAnswer:")
        print(answer)
        print()
        return

    if args.interactive or len(sys.argv) == 1:
        interactive_mode()
        return

    parser.print_help()


if __name__ == "__main__":
    main()
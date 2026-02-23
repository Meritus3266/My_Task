"""
SIMPLE INFERENCE SCRIPT WITH RAG
Use your fine-tuned model with optional document retrieval
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import chromadb
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
# CONFIGURATION - EDIT THESE

# Path to your trained model
MODEL_PATH = "trained_model/final"

# Path to your documents (optional, for RAG)
DOCUMENTS_FOLDER = None  # Set to your docs folder path, e.g., "my_documents"

# Vector database path
VECTOR_DB_PATH = "vector_db"
# SIMPLE RAG SYSTEM

class SimpleRAG:
    """Ultra-simple RAG implementation"""
    
    def __init__(self, docs_folder=None):
        self.docs_folder = docs_folder
        self.embeddings = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
        self.collection = None
        
        if docs_folder and Path(docs_folder).exists():
            self.setup_documents()
    
    def setup_documents(self):
        """Load documents into vector database"""
        logger.info(f" Loading documents from {self.docs_folder}")
        
        # Create collection
        try:
            self.collection = self.client.get_collection("documents")
            logger.info("✓ Using existing collection")
        except:
            self.collection = self.client.create_collection("documents")
            
            # Read all text files
            docs = []
            ids = []
            doc_path = Path(self.docs_folder)
            
            for i, file_path in enumerate(doc_path.glob("**/*.txt")):
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    # Split into chunks
                    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
                    for j, chunk in enumerate(chunks):
                        docs.append(chunk)
                        ids.append(f"doc_{i}_{j}")
            
            if docs:
                self.collection.add(documents=docs, ids=ids)
                logger.info(f" Loaded {len(docs)} document chunks")
    
    def search(self, query, top_k=3):
        """Search for relevant documents"""
        if not self.collection:
            return []
        
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        return results['documents'][0] if results['documents'] else []

# INFERENCE CLASS

class SimpleInference:
    """Simple inference with optional RAG"""
    
    def __init__(self, model_path, use_rag=False, docs_folder=None):
        logger.info(" Loading model...")
        
        # Load model
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="auto",
            torch_dtype=torch.float16
        )
        self.model.eval()
        logger.info(" Model loaded")
        
        # Setup RAG if requested
        self.rag = None
        if use_rag:
            self.rag = SimpleRAG(docs_folder)
    
    def generate(self, prompt, max_tokens=200, temperature=0.7):
        """Generate text with optional RAG context"""
        
        # Get context from RAG if available
        context = ""
        if self.rag:
            docs = self.rag.search(prompt)
            if docs:
                context = "\n\n".join(docs)
                prompt = f"Context:\n{context}\n\nQuestion: {prompt}\n\nAnswer:"
        
        # Generate
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove the prompt from response
        if context:
            response = response.split("Answer:")[-1].strip()
        
        return response

# MAIN USAGE

def main():
    logger.info("=" * 80)
    logger.info("SIMPLE INFERENCE")
    logger.info("=" * 80)
    
    # Check if model exists
    if not Path(MODEL_PATH).exists():
        logger.error(f" Model not found at {MODEL_PATH}")
        logger.error("Please train the model first using simple_finetune.py")
        return
    
    # Initialize (with or without RAG)
    use_rag = DOCUMENTS_FOLDER is not None
    inference = SimpleInference(
        model_path=MODEL_PATH,
        use_rag=use_rag,
        docs_folder=DOCUMENTS_FOLDER
    )
    
    logger.info("\n" + "=" * 80)
    logger.info("Ready! Type your questions (or 'quit' to exit)")
    logger.info("=" * 80 + "\n")
    
    # Interactive loop
    while True:
        try:
            prompt = input("You: ").strip()
            
            if prompt.lower() in ['quit', 'exit', 'q']:
                logger.info("Goodbye!")
                break
            
            if not prompt:
                continue
            
            logger.info("Generating...")
            response = inference.generate(prompt)
            
            print(f"\nAssistant: {response}\n")
            print("-" * 80 + "\n")
            
        except KeyboardInterrupt:
            logger.info("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")


# Example batch inference
def batch_example():
    """Example of batch processing"""
    inference = SimpleInference(MODEL_PATH)
    
    questions = [
        "What is machine learning?",
        "Explain neural networks",
        "How does fine-tuning work?"
    ]
    
    for q in questions:
        logger.info(f"\nQ: {q}")
        response = inference.generate(q, max_tokens=150)
        logger.info(f"A: {response}\n")


if __name__ == "__main__":
    # Run interactive mode
    main()
    
    # Or uncomment for batch mode:
    # batch_example()

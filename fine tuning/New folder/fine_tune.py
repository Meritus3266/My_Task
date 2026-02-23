"""
 Production Fine-Tuning Backend (.env support)
OpenAI GPT-4o-mini + Weights & Biases + Flask API
"""

import os
from dotenv import load_dotenv  # pip install python-dotenv
import json
import wandb
from openai import OpenAI
from pathlib import Path
from typing import Dict
import argparse
from flask import Flask, request, jsonify

#  Load .env automatically
load_dotenv()

# Config (from .env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WANDB_API_KEY = os.getenv("WANDB_API_KEY")
DATASET_PATH = "fine_tune_dataset.jsonl"
MODEL_NAME = "gpt-4o-mini-2024-07-18"
EPOCHS = 4
SUFFIX = "pdf-knowledge-prod"

class FineTuneManager:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError(" OPENAI_API_KEY missing in .env")
        
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        if WANDB_API_KEY:
            wandb.login(key=WANDB_API_KEY)
    
    def validate_dataset(self, filepath: str) -> Dict:
        """Validate + stats"""
        docs = []
        total_tokens = 0
        
        with open(filepath, 'r') as f:
            for i, line in enumerate(f):
                doc = json.loads(line)
                if 'text' not in doc:
                    raise ValueError(f"Line {i+1}: Missing 'text'")
                total_tokens += len(doc['text'].split())
                docs.append(doc)
        
        return {
            "valid": True,
            "doc_count": len(docs),
            "total_tokens": total_tokens,
            "avg_tokens": total_tokens // len(docs),
            "cost_estimate": f"${(total_tokens * 4.4 / 1e6) * EPOCHS:.2f}"
        }
    
    def split_dataset(self):
        """90/10 train/val split"""
        docs = []
        with open(DATASET_PATH, 'r') as f:
            docs = [json.loads(line) for line in f]
        
        split = int(0.9 * len(docs))
        train_docs, val_docs = docs[:split], docs[split:]
        
        with open("train.jsonl", 'w') as f:
            for doc in train_docs: f.write(json.dumps(doc) + '\n')
        with open("val.jsonl", 'w') as f:
            for doc in val_docs: f.write(json.dumps(doc) + '\n')
        
        print(f" Split: {len(train_docs)} train / {len(val_docs)} val")
        return "train.jsonl", "val.jsonl"
    
    def create_fine_tune(self) -> str:
        """Start fine-tuning (upload files first via CLI/web)"""
        stats = self.validate_dataset(DATASET_PATH)
        print(f" {stats['doc_count']} docs, {stats['total_tokens']} tokens")
        print(f" Cost: {stats['cost_estimate']}")
        
        self.split_dataset()
        
        # NOTE: Upload train/val.jsonl to OpenAI first, get file IDs
        print("\n UPLOAD FILES TO OPENAI FIRST:")
        print("openai api files.create -f train.jsonl --purpose 'fine-tune'")
        print("openai api files.create -f val.jsonl --purpose 'fine-tune'")
        print("\nThen run:")
        print("python backend.py --mode train-complete <train_file_id> <val_file_id>")
        
        if WANDB_API_KEY:
            wandb.init(project="pdf-fine-tuning", config=stats)
        
        return "READY - Upload files & run train-complete"
    
    def start_training(self, train_file_id: str, val_file_id: str) -> str:
        """Start actual training with file IDs"""
        job = self.client.fine_tuning.jobs.create(
            training_file=train_file_id,
            validation_file=val_file_id,
            model=MODEL_NAME,
            hyperparameters={"n_epochs": EPOCHS},
            suffix=SUFFIX
        )
        
        print(f" Training started: https://platform.openai.com/fine-tuning/{job.id}")
        print(f" W&B: https://wandb.ai/runs/{wandb.run.id}")
        return job.id

# Global manager
manager = FineTuneManager()

# Flask API
app = Flask(__name__)
FINE_TUNE_ID = None

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "dataset": DATASET_PATH})

@app.route('/validate', methods=['GET'])
def validate():
    stats = manager.validate_dataset(DATASET_PATH)
    return jsonify(stats)

@app.route('/fine-tune', methods=['POST'])
def fine_tune():
    data = request.json
    train_id, val_id = data['train_file_id'], data['val_file_id']
    job_id = manager.start_training(train_id, val_id)
    return jsonify({"job_id": job_id, "status": "training"})

@app.route('/chat', methods=['POST'])
def chat():
    global FINE_TUNE_ID
    if not FINE_TUNE_ID:
        return jsonify({"error": "Set FINE_TUNE_ID env var"}), 400
    
    data = request.json
    response = manager.client.chat.completions.create(
        model=FINE_TUNE_ID,
        messages=[
            {"role": "system", "content": "PDF document expert."},
            {"role": "user", "content": data['message']}
        ]
    )
    return jsonify({"response": response.choices[0].message.content})

# CLI Commands
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF Fine-Tuning Backend")
    parser.add_argument('--mode', choices=['validate', 'split', 'train', 'chat', 'serve'])
    parser.add_argument('--train-file', help="OpenAI train file ID")
    parser.add_argument('--val-file', help="OpenAI val file ID")
    parser.add_argument('--model-id', help="Fine-tuned model ID")
    parser.add_argument('--message', help="Test message")
    args = parser.parse_args()
    
    if args.mode == 'validate':
        stats = manager.validate_dataset(DATASET_PATH)
        print(json.dumps(stats, indent=2))
    elif args.mode == 'split':
        manager.split_dataset()
    elif args.mode == 'train':
        manager.create_fine_tune()
    elif args.mode == 'chat':
        print(manager.client.chat.completions.create(
            model=args.model_id,
            messages=[{"role": "user", "content": args.message}]
        ).choices[0].message.content)
    elif args.mode == 'serve':
        print(" Server: http://localhost:5000")
        print("curl -X POST http://localhost:5000/chat -d '{\"message\":\"test\"}'")
        app.run(debug=False, host='0.0.0.0', port=5000)
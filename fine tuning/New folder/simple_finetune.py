"""
SIMPLE FINE-TUNING SCRIPT - All-in-One
Just update the paths below and run!
"""

import json
import logging
from pathlib import Path
import torch
from datasets import Dataset
from peft import LoraConfig, get_peft_model, TaskType
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    BitsAndBytesConfig,
)

# CONFIGURATION - EDIT THESE VALUES

# Your dataset path (update this!)
DATASET_PATH = r"C:\Users\ncc333\Desktop\My_Task\fine tuning\New folder\fine_tune_dataset.jsonl"

# Output directory for trained model
OUTPUT_DIR = "trained_model"

# Model to fine-tune - Choose any Hugging Face model!
# 
# POPULAR OPTIONS:
# ----------------
# Small Models (good for testing, fast training):
# "gpt2"                                # 117M params - Very fast
# "gpt2-medium"                         # 345M params - Good balance
# "microsoft/DialoGPT-medium"           # 774M params - Great for chat
# "TinyLlama/TinyLlama-1.1B-Chat-v1.0" # 1.1B params - Small but capable
# "Qwen/Qwen2-0.5B"                    # 0.5B params - Very efficient
#
# Medium Models (better quality, needs more GPU):
# "EleutherAI/gpt-neo-1.3B"            # 1.3B params - Good quality
# "EleutherAI/pythia-1.4b"             # 1.4B params - Well-trained
# "stabilityai/stablelm-2-1_6b"        # 1.6B params - Recent, good
#
# Large Models (best quality, needs powerful GPU + 4-bit quantization):
# "mistralai/Mistral-7B-v0.1"          # 7B params - Excellent quality
# "meta-llama/Llama-2-7b-hf"           # 7B params - Needs HF token
# "NousResearch/Llama-2-7b-hf"         # 7B params - Alternative
# "tiiuae/falcon-7b"                    # 7B params - Good performance
#
# For Llama models, you need to:
# 1. Request access on Hugging Face
# 2. Login: huggingface-cli login
# 3. Enter your token

MODEL_NAME = "gpt2"  # Small, fast model - perfect for testing!

# Training settings (optimized for gpt2)
EPOCHS = 3
BATCH_SIZE = 4          # gpt2 is small, so we can use larger batch size
LEARNING_RATE = 5e-5    # Lower learning rate for gpt2
MAX_LENGTH = 512        # Maximum sequence length

# SETUP LOGGING

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MAIN SCRIPT

def main():
    logger.info("=" * 80)
    logger.info("SIMPLE FINE-TUNING SCRIPT")
    logger.info("=" * 80)
    
    # Step 1: Check dataset
    logger.info(f" Checking dataset: {DATASET_PATH}")
    if not Path(DATASET_PATH).exists():
        logger.error(f" Dataset not found: {DATASET_PATH}")
        logger.error("Please update DATASET_PATH in the script!")
        return
    
    with open(DATASET_PATH, 'r', encoding='utf-8') as f:
        num_samples = len(f.readlines())
    logger.info(f"✓ Found {num_samples} samples")
    
    # Step 2: Load model and tokenizer
    logger.info(f" Loading model: {MODEL_NAME}")
    
    # Use 4-bit quantization to save memory
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_quant_type="nf4"
    )
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            quantization_config=bnb_config,
            device_map="auto",
            torch_dtype=torch.float16
        )
        logger.info("✓ Model loaded successfully")
        
    except Exception as e:
        logger.error(f" Failed to load model: {e}")
        return
    
    # Step 3: Setup LoRA
    logger.info(" Setting up LoRA adapters")
    
    # Auto-detect target modules based on model architecture
    # For gpt2, we target the attention layers
    target_modules = ["c_attn", "c_proj"]  # Optimized for gpt2
    
    logger.info(f"Target modules for gpt2: {target_modules}")
    
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=16,
        lora_alpha=32,
        lora_dropout=0.1,
        target_modules=target_modules,
        bias="none"
    )
    
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    # Step 4: Prepare dataset
    logger.info(" Preparing dataset")
    
    def format_and_tokenize(example):
        # Handle different JSON formats
        if "text" in example:
            text = example["text"]
        elif "instruction" in example and "output" in example:
            text = f"### Instruction:\n{example['instruction']}\n\n### Response:\n{example['output']}"
        elif "prompt" in example and "completion" in example:
            text = f"{example['prompt']}\n{example['completion']}"
        else:
            # Fallback: join all string values
            text = " ".join([str(v) for v in example.values() if isinstance(v, str)])
        
        # Tokenize
        tokenized = tokenizer(
            text,
            truncation=True,
            max_length=MAX_LENGTH,
            padding=False
        )
        tokenized["labels"] = tokenized["input_ids"].copy()
        return tokenized
    
    # Load and process dataset
    dataset = Dataset.from_json(DATASET_PATH)
    dataset = dataset.map(
        format_and_tokenize,
        remove_columns=dataset.column_names,
        desc="Tokenizing"
    )
    logger.info(f" Dataset prepared: {len(dataset)} samples")
    
    # Step 5: Setup training
    logger.info(" Starting training")
    
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=8,
        learning_rate=LEARNING_RATE,
        fp16=True,
        logging_steps=10,
        save_steps=500,
        save_total_limit=2,
        report_to="none",  # No external logging
    )
    
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=data_collator,
    )
    
    # Step 6: Train!
    logger.info("=" * 80)
    logger.info("TRAINING STARTED")
    logger.info("=" * 80)
    
    try:
        trainer.train()
    except RuntimeError as e:
        if "out of memory" in str(e):
            logger.error(" GPU ran out of memory!")
            logger.error("Try these solutions:")
            logger.error("1. Reduce BATCH_SIZE to 1")
            logger.error("2. Reduce MAX_LENGTH to 256")
            logger.error("3. Use a smaller model")
            return
        else:
            raise
    
    # Step 7: Save model
    logger.info(" Saving model")
    final_path = Path(OUTPUT_DIR) / "final"
    trainer.save_model(str(final_path))
    tokenizer.save_pretrained(str(final_path))
    
    logger.info("=" * 80)
    logger.info(" TRAINING COMPLETE!")
    logger.info("=" * 80)
    logger.info(f"Model saved to: {final_path}")
    logger.info("\nTo use your model:")
    logger.info("1. Load it with: AutoModelForCausalLM.from_pretrained('trained_model/final')")
    logger.info("2. Or use simple_inference.py")


def test_model():
    """Simple test function to try your trained model"""
    logger.info("\n" + "=" * 80)
    logger.info("TESTING TRAINED MODEL")
    logger.info("=" * 80)
    
    model_path = Path(OUTPUT_DIR) / "final"
    
    if not model_path.exists():
        logger.error(" Model not found. Train first!")
        return
    
    # Load model
    logger.info("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained(str(model_path))
    model = AutoModelForCausalLM.from_pretrained(
        str(model_path),
        device_map="auto",
        torch_dtype=torch.float16
    )
    model.eval()
    
    # Test prompt
    prompt = "Hello! How can I help you today?"
    logger.info(f"\nPrompt: {prompt}")
    
    # Generate
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    logger.info(f"Response: {response}\n")


if __name__ == "__main__":
    # Run training
    main()
    
    # Uncomment to test after training:
    # test_model()
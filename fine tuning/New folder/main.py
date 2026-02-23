import json
import logging
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

import torch
from datasets import Dataset, DatasetDict
from peft import LoraConfig, get_peft_model, TaskType
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    BitsAndBytesConfig,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('finetune.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# FIXED PATH - Your specific JSONL file
JSONL_PATH = r"C:\Users\ncc333\Desktop\My_Task\fine tuning\New folder\fine_tune_dataset.jsonl"


class LoRAFineTuner:
    """Production-ready LoRA fine-tuning for your dataset."""
    
    def __init__(
        self,
        model_name: str = "microsoft/DialoGPT-medium",
        output_dir: str = "lora-finetuned-model",
        jsonl_path: str = JSONL_PATH
    ):
        self.model_name = model_name
        self.output_dir = Path(output_dir)
        self.jsonl_path = Path(jsonl_path)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.output_dir.mkdir(exist_ok=True)
        
        logger.info(f"Using device: {self.device}")
        logger.info(f"JSONL dataset: {self.jsonl_path}")
        logger.info(f"Output directory: {self.output_dir}")
    
    def validate_dataset(self) -> bool:
        """Validate JSONL dataset exists and has data."""
        if not self.jsonl_path.exists():
            logger.error(f"JSONL file not found: {self.jsonl_path}")
            return False
        
        # Count lines and sample first few
        with open(self.jsonl_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        logger.info(f"Dataset contains {len(lines)} samples")
        
        if len(lines) == 0:
            logger.error("Dataset is empty!")
            return False
        
        # Log sample structure
        try:
            sample = json.loads(lines[0])
            logger.info(f"Sample structure: {list(sample.keys())}")
        except:
            logger.error("Invalid JSONL format!")
            return False
        
        return True
    
    def load_model_and_tokenizer(self, load_in_4bit: bool = True):
        """Load model and tokenizer with 4-bit quantization."""
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=load_in_4bit,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4"
        ) if load_in_4bit else None
        
        logger.info(f"Loading model: {self.model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            padding_side="right",
            trust_remote_code=True
        )
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            logger.info("Set pad_token to eos_token")
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=quantization_config,
            device_map="auto",
            trust_remote_code=True,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        )
        
        logger.info(" Model and tokenizer loaded successfully")
    
    def setup_lora(self, r: int = 16, lora_alpha: int = 32, target_modules: Optional[List[str]] = None):
        """Configure LoRA adapters."""
        if target_modules is None:
            # Auto-detect common target modules
            target_modules = ["q_proj", "v_proj", "k_proj", "o_proj"]
            if hasattr(self.model.config, "attention_layers"):
                target_modules.extend(["qkv_proj"])
        
        lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            inference_mode=False,
            r=r,
            lora_alpha=lora_alpha,
            lora_dropout=0.1,
            target_modules=target_modules,
            bias="none"
        )
        
        self.model = get_peft_model(self.model, lora_config)
        self.model.print_trainable_parameters()
        logger.info(" LoRA adapters configured")
    
    def create_dataset(self, max_length: int = 1024, max_samples: Optional[int] = None) -> Dataset:
        """Load and tokenize your JSONL dataset."""
        
        def format_text(example):
            """Format examples based on available fields."""
            # Handle different possible JSON structures
            if "text" in example:
                return {"text": example["text"]}
            elif all(k in example for k in ["instruction", "input", "output"]):
                text = f"### Instruction:\n{example['instruction']}\n\n### Input:\n{example['input']}\n\n### Response:\n{example['output']}"
                return {"text": text}
            elif "prompt" in example and "completion" in example:
                text = f"{example['prompt']}\n{example['completion']}"
                return {"text": text}
            else:
                # Fallback: concatenate all string values
                text = " ".join([v for k, v in example.items() if isinstance(v, str)])
                return {"text": text}
        
        def tokenize_function(examples):
            tokenized = self.tokenizer(
                examples["text"],
                truncation=True,
                padding=False,
                max_length=max_length,
                return_tensors="pt"
            )
            tokenized["labels"] = tokenized["input_ids"].clone()
            return tokenized
        
        logger.info("Loading and processing dataset...")
        
        # Load JSONL dataset
        dataset = Dataset.from_json(self.jsonl_path)
        
        # Limit samples if specified
        if max_samples:
            dataset = dataset.select(range(min(max_samples, len(dataset))))
        
        logger.info(f"Loaded {len(dataset)} samples")
        
        # Format text for training
        dataset = dataset.map(format_text)
        
        # Tokenize
        tokenized_dataset = dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=dataset.column_names,
            desc="Tokenizing"
        )
        
        logger.info(f" Dataset prepared: {len(tokenized_dataset)} samples")
        return tokenized_dataset
    
    def train(self, dataset: Dataset):
        """Execute production training."""
        training_args = TrainingArguments(
            output_dir=str(self.output_dir),
            overwrite_output_dir=True,
            num_train_epochs=3,
            per_device_train_batch_size=2,  # Conservative for stability
            gradient_accumulation_steps=8,
            warmup_steps=50,
            learning_rate=2e-4,
            weight_decay=0.01,
            fp16=True,
            logging_steps=10,
            save_steps=250,
            save_total_limit=2,
            report_to="tensorboard",
            run_name=f"lora-finetune-{self.jsonl_path.stem}",
            dataloader_pin_memory=False,
            remove_unused_columns=False,
            dataloader_num_workers=0,  # Stable for Windows
            gradient_checkpointing=True,
        )
        
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False,
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=dataset,
            data_collator=data_collator,
            tokenizer=self.tokenizer,
        )
        
        logger.info(" Starting LoRA fine-tuning...")
        trainer.train()
        
        # Save final model
        final_path = self.output_dir / "final"
        trainer.save_model(final_path)
        self.tokenizer.save_pretrained(final_path)
        
        logger.info(f" Training complete! Model saved to: {final_path}")
        logger.info(f" All checkpoints: {self.output_dir}")


def main():
    """Run the complete fine-tuning pipeline."""
    print(" LoRA Fine-tuning Pipeline")
    print(f" Dataset: {JSONL_PATH}")
    
    # Initialize trainer
    tuner = LoRAFineTuner(
        model_name="microsoft/DialoGPT-medium",  # Change as needed
        output_dir="lora-finetuned-model",
        jsonl_path=JSONL_PATH
    )
    
    # Step 1: Validate dataset
    if not tuner.validate_dataset():
        print(" Dataset validation failed!")
        sys.exit(1)
    
    # Step 2: Load model
    tuner.load_model_and_tokenizer(load_in_4bit=True)
    
    # Step 3: Setup LoRA
    tuner.setup_lora(r=16, lora_alpha=32)
    
    # Step 4: Prepare dataset
    dataset = tuner.create_dataset(max_length=1024, max_samples=None)
    
    # Step 5: Train
    tuner.train(dataset)
    
    print(" Fine-tuning completed successfully!")
    print("Run `tensorboard --logdir lora-finetuned-model` to view training logs")


if __name__ == "__main__":
    main()
# 🚀 SUPER SIMPLE FINE-TUNING

Just 3 files. No complexity. Works in VS Code.

## 📥 Files You Need

1. **simple_finetune.py** - Train your model
2. **simple_inference.py** - Use your model (with optional RAG)
3. **simple_requirements.txt** - Dependencies

## ⚡ Quick Start (5 Steps)

### Step 1: Install Dependencies
```bash
pip install -r simple_requirements.txt
```

### Step 2: Edit simple_finetune.py
Open `simple_finetune.py` and update line 24:
```python
DATASET_PATH = r"C:\Users\ncc333\Desktop\My_Task\fine tuning\New folder\fine_tune_dataset.jsonl"
```

### Step 3: Run Training
```bash
python simple_finetune.py
```

That's it! Your model will be saved to `trained_model/final/`

### Step 4: Test Your Model
Open `simple_inference.py` and run:
```bash
python simple_inference.py
```

Type questions and get answers!

### Step 5 (Optional): Add RAG

If you want to use documents:

1. Put your `.txt` files in a folder (e.g., `my_docs/`)
2. In `simple_inference.py`, update line 19:
```python
DOCUMENTS_FOLDER = "my_docs"
```
3. Run again - it will use your documents!

## 🎯 That's It!

**No configuration files.**  
**No complex setup.**  
**Just works.**

## 💡 Customization

Want to change settings? Just edit these in `simple_finetune.py`:

```python
EPOCHS = 3              # How many times to train
BATCH_SIZE = 2          # Reduce if GPU memory error
LEARNING_RATE = 2e-4    # How fast to learn
MODEL_NAME = "microsoft/DialoGPT-medium"  # Which model to use
```

## 🐛 Troubleshooting

**GPU Out of Memory?**
- Change `BATCH_SIZE = 1` in simple_finetune.py

**Import Errors?**
```bash
pip install -r simple_requirements.txt
```

**Model Not Found?**
- Run `simple_finetune.py` first to train

**RAG Not Working?**
- Make sure DOCUMENTS_FOLDER has .txt files
- First run will take time to index documents

## 📖 How It Works

1. **Training**: Loads your data → Fine-tunes model → Saves to `trained_model/final/`
2. **Inference**: Loads trained model → (Optional: searches documents) → Generates answer

## ✅ What Can You Do?

✓ Fine-tune on your dataset  
✓ Chat with your fine-tuned model  
✓ Add RAG for document-based answers  
✓ Batch process questions  
✓ All in VS Code!

Need the full production system? Use the `fine_tuning_rag_system.tar.gz` file instead.

This simple version is perfect for:
- Quick experiments
- Learning
- Small projects
- Local development

Enjoy! 🎉

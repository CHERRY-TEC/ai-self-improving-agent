# AI Self-Improving Agent - FREE Setup Guide

## Option 1: Ollama (RECOMMENDED - 100% FREE)

Ollama runs AI models **locally on your computer**. No API keys, no cost.

### Step 1: Install Ollama
1. Go to https://ollama.com/download
2. Download for Windows/Mac/Linux
3. Install it

### Step 2: Download a model
```bash
# For code improvement (recommended)
ollama pull codellama

# Or use a smaller/faster model
ollama pull llama3.2

# Or use the best free model
ollama pull llama3.1:8b
```

### Step 3: Run the agent
```bash
python main.py --iterations 5 --provider ollama --model codellama
```

### Step 4: Start Ollama (if not running)
```bash
ollama serve
```

---

## Option 2: HuggingFace (FREE with limits)

HuggingFace has a free inference API.

### Step 1: Get free API key (optional)
1. Go to https://huggingface.co
2. Sign up (free)
3. Get API token from Settings

### Step 2: Run the agent
```bash
# Set your token (optional - some models work without it)
set HF_TOKEN=your_token_here

python main.py --iterations 5 --provider huggingface --model meta-llama/Llama-3-8b-chat-hf
```

---

## Option 3: Local Rules (No AI, but FREE)

If you don't want to install anything:

```bash
python main.py --iterations 5 --provider local
```

This uses predefined rules (adds type hints, docstrings, etc.)

---

## Quick Start (Fastest)

```bash
# 1. Install Ollama from https://ollama.com/download
# 2. Open terminal and run:
ollama pull codellama

# 3. Run the agent:
python main.py
```

That's it! The agent will use Ollama (FREE) to improve its own code.

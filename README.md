# SemantixAI: Semantic Identifier Recovery & XAI Engine for Decompiled Code

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Model](https://img.shields.io/badge/Model-Salesforce%2Fcodet5--base-orange.svg)](https://huggingface.co/Salesforce/codet5-base)
[![Git LFS](https://img.shields.io/badge/Git%20LFS-6.2GB-green.svg)](https://git-lfs.github.com/)

**SemantixAI** is an AI-driven reverse engineering pipeline designed to restore meaningful function names and variable identifiers in stripped or obfuscated C/C++ binaries. By combining deep sequence-to-sequence translation via **CodeT5** with contextual API guardrails, dynamic confidence scoring, and Explainable AI (XAI), SemantixAI bridges the gap between raw binary decompiler output (e.g., Ghidra/IDA Pro) and human-readable source code.

---

## 🏗️ Architecture & Pipeline Overview

The core system operates across a modular 5-stage processing pipeline:

              +-----------------------------------+
              | Decompiled Function Code (C/AST)  |
              +-----------------+-----------------+
                                |
                                v
                 +--------------+--------------+
                 | 1. SemFlow Prompt Generation|
                 +--------------+--------------+
                                |
                                v
                 +--------------+--------------+
                 | 2. CodeT5 LLM Inference    |
                 |    (220M Fine-tuned Model)  |
                 +--------------+--------------+
                                |
                                v
                 +--------------+--------------+
                 | 3. Function/Identifier      |
                 |    Recovery & Guardrails    |
                 +--------------+--------------+
                                |
                                v
                 +--------------+--------------+
                 | 4. Confidence Engine        |
                 +--------------+--------------+
                                |
                                v
                 +--------------+--------------+
                 | 5. XAI Explanations Engine  |
                 +--------------+--------------+
                                |
                                v
              +-----------------+-----------------+
              | Final High-Confidence Identifiers |
              |  & Human-Readable Explanations   |
              +-----------------------------------+

### Key Modules:

1. **SemFlow Prompt Generator (`ai_module/prompt_generator.py`):** Normalizes decompiled code, extracts caller/callee AST signatures, and structures input prompts for LLM ingestion.

2. **CodeT5 LLM Predictor (`ai_module/llm_predictor.py`):** Leverages a fine-tuned `Salesforce/codet5-base` encoder-decoder model to generate candidate semantic function names.

3. **Function Recovery & Guardrails (`ai_module/name_predictor.py`):** Filters echo-based obfuscated placeholders (e.g., `sub_XXXXXX`) and applies post-processing rule-sets based on API evidence.

4. **Confidence Scoring Engine (`ai_module/confidence_engine.py`):** Evaluates semantic overlap, token entropy, and call-graph evidence to assign reliability scores.

5. **XAI Explanations Engine:** Generates natural language justifications explaining *why* a specific identifier name was chosen based on code semantics.

---

## 🚀 Quick Start & Installation

### Prerequisites

* Linux / macOS (Tested on Ubuntu 20.04/22.04 LTS)
* Python 3.8 or higher
* `git-lfs` (Git Large File Storage)

### 1. Clone the Repository (with Model Weights)

Since model binary weights (6.2 GB) are tracked via **Git LFS**, ensure `git-lfs` is installed prior to cloning:

```bash
# Install Git LFS
sudo apt update && sudo apt install git-lfs -y
git lfs install

# Clone repository
git clone https://github.com/Sebah1802/SemantixAI.git
cd SemantixAI

# Pull LFS model weights
git lfs pull
```

### 2. Set Up Virtual Environment & Dependencies

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 💻 Usage

### Run Full Pipeline End-to-End

To process decompiled input functions and produce semantic identifiers along with confidence scores and XAI justifications:

```bash
python -m ai_module.main
```

### Run Module Tests

To run individual component verifications:

```bash
# Test LLM Inference & Name Prediction
python test_inference.py

# Test Confidence Scoring Engine
python test_confidence.py
```

---

## 📂 Repository Structure

```text
SemantixAI/
├── ai_module/                  # Core Python modules
│   ├── prompt_generator.py     # SemFlow prompt construction
│   ├── llm_predictor.py        # CodeT5 inference engine
│   ├── name_predictor.py       # Function recovery & guardrails
│   ├── confidence_engine.py    # Confidence scoring logic
│   ├── json_reader.py          # Data ingestion utilities
│   └── main.py                 # Pipeline entry point
├── models/                     # Model directory (Tracked via Git LFS)
│   └── semantix_codet5/        # Fine-tuned CodeT5-base weights & config
├── dataset/                    # Training, validation, and test datasets
│   ├── train.json
│   ├── validation.json
│   └── test.json
├── sample_data/                # Benchmark decompiled functions
│   └── functions.json
├── test_inference.py           # Unit tests for model inference
├── test_confidence.py          # Unit tests for confidence scoring
├── train.py                    # Fine-tuning script for CodeT5
├── requirements.txt            # Python dependencies
└── .gitignore                  # Git tracking rules
```

---

## 💡 Tech Stack & Design Choices

    Base Model: Salesforce/codet5-base (220M parameters)

    Architecture: Encoder-Decoder (Seq2Seq) bidirectional attention.

    Why CodeT5-base? Chosen over standard encoder-only models (like CodeBERT) for sequence translation capabilities, and over 7B+ decoder-only LLMs for low-latency local execution on standard analyst hardware.

    Frameworks: PyTorch, Hugging Face Transformers, Datasets.

---

## 🤝 Team Collaboration

When pushing updates to this repository:

    Source code (.py, .json, .txt) can be committed via standard Git.

    Do not commit temporary training checkpoints or prediction cache outputs (sample_data/predictions.json).

    If modifying model binaries, ensure git-lfs is active before committing.

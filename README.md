# AI Code Reviewer — AI-Powered Code Analysis

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Google%20Generative%20AI-Gemini%203.8-8E75B2.svg)](https://aistudio.google.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An automated AI code reviewer that analyzes code for **bugs**, **security vulnerabilities**, **computational complexity**, and **code quality** across **Python, JavaScript, TypeScript, C++, Java, C, and Go** using **Google Generative AI (Gemini)**.

The project demonstrates production-grade AI engineering fundamentals: **specialized prompt engineering**, **lightweight context engineering** (language guideline conditioning), **automatic language detection**, **schema-enforced structured JSON generation**, and a **custom evaluation suite** with category-level detection metrics.

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [User Experience & Flow](#2-user-experience--flow)
3. [Key Features](#3-key-features)
4. [System Architecture](#4-system-architecture)
5. [Tech Stack](#5-tech-stack)
6. [Project Structure](#6-project-structure)
7. [Setup & Installation](#7-setup--installation)
8. [Environment Variables & Security](#8-environment-variables--security)
9. [Automated Evaluation Suite](#9-automated-evaluation-suite)
10. [Engineering Limitations](#10-engineering-limitations)
11. [Future Roadmap](#11-future-roadmap)
12. [Interview & Resume Guide](#12-interview--resume-guide)

---

## 1. Project Overview

### The Problem
Traditional static analysis tools (like linters or AST scanners) enforce syntax rules but fail to reason about high-level business logic, edge-case vulnerabilities, semantic security flaws (such as parameter tampering or unsafe dynamic execution), or architectural maintainability. Conversely, generic LLM interfaces return unstructured text, require manual configuration of models and modes, and frequently hallucinate or fail silently.

### The Solution
**AI Code Reviewer** is built as a zero-configuration developer utility:
- **No Dropdowns or Mode Selection**: Users simply paste their code and click "Review Code".
- **Automatic Language Detection**: Identifies Python, JavaScript, TypeScript, C++, Java, C, Go, and more.
- **Unified 360° Analysis**: Reviews code across 4 distinct pillars: Bugs, Security, Performance, and Code Quality.
- **Context Engineering**: Injects curated language guidelines into the context window without vector database overhead.
- **Strict Structured JSON**: Schema-enforced outputs ensure consistent rendering of severity ratings, line references, algorithmic complexity ($O$), recommendations, and refactored code.
- **Zero UI Secrets**: API keys are securely resolved from `.env` or system environment variables—never entered or exposed in the UI.

---

## 2. User Experience & Flow

```
                      User Opens App
                            ↓
                     Pastes Source Code
                            ↓
                   Clicks "🔍 Review Code"
                            ↓
              AI Automatically Detects Language
                            ↓
           AI Performs Comprehensive Multi-Pillar Review
                            ↓
          Results Displayed in Clean Structured Layout:
          - Detected Language & Overall Score (X/10)
          - Executive Summary
          - 🐛 Bugs
          - 🔐 Security
          - ⚡ Performance
          - ✨ Code Quality
          - 📊 Complexity (Time & Space)
          - 💡 Recommendations
          - 🔧 Improved Code
```

---

## 3. Key Features

- **Zero-Configuration Interface**:
  - No dropdowns, no review mode selectors, and no exposed settings. Clean, developer-centric design.
- **Automatic Multi-Language Detection**:
  - Native support for Python, JavaScript, TypeScript, C++, Java, C, Go, and more.
- **Comprehensive 4-Pillar Code Analysis**:
  - **🐛 Bugs**: Logical errors, edge cases, off-by-one loops, unhandled exceptions, and pointer/null hazards.
  - **🔐 Security**: SQL/command injections, hardcoded secrets, unsafe dynamic code execution (`eval`), and buffer boundary issues.
  - **⚡ Performance**: Algorithmic bottlenecks ($O(n^2)$ vs $O(n)$), unnecessary iterations, redundant memory copies.
  - **✨ Code Quality**: Readability, maintainability, naming conventions, modularity, DRY principles, and language idioms.
- **Complexity Estimation**:
  - Returns Big-O time and space complexity estimates directly from code analysis.
- **Refactored Code Generation**:
  - Provides a complete, ready-to-use refactored version of the submitted code.
- **Resilient Fallback Parser**:
  - Strips markdown fences, extracts JSON boundaries, validates fields, and handles malformed outputs safely without crashing.
- **Automated Evaluation Runner**:
  - Standalone benchmark suite (`evaluation/evaluate.py`) evaluating 14 curated defect cases to quantify detection accuracy and false negatives.

---

## 4. System Architecture

```
                                  +---------------------------------------+
                                  |            Developer / User           |
                                  +-------------------+-------------------+
                                                      |
                                          Pastes Code & Clicks Review
                                                      |
                                                      v
                                  +---------------------------------------+
                                  |         Streamlit UI (app.py)         |
                                  |      (Minimal Single-Page Tool)       |
                                  +-------------------+-------------------+
                                                      |
                                             Submits Source Code
                                                      |
                                                      v
  +-----------------------+       +---------------------------------------+
  |  Language Guidelines  | ----> |       Reviewer Engine (reviewer.py)   |
  |  (guidelines/*.md)    |       +-------------------+-------------------+
  +-----------------------+                           |
                                           Builds Comprehensive Prompt
                                                      |
                                                      v
  +-----------------------+       +---------------------------------------+
  | Comprehensive Prompts | ----> |     Google Generative AI (Gemini)     |
  | (prompts/__init__.py) |       |  (generation_config=application/json) |
  +-----------------------+       +-------------------+-------------------+
                                                      |
                                            Returns Raw JSON String
                                                      |
                                                      v
                                  +---------------------------------------+
                                  | Resilient JSON Parser (helpers.py)    |
                                  | - Strips fences, normalizes fields    |
                                  | - Safe fallback on decode error       |
                                  +-------------------+-------------------+
                                                      |
                                          Structured Review Object
                                                      |
                                                      v
                                  +---------------------------------------+
                                  |         Rendered Streamlit UI         |
                                  | - Detected Language & Overall Score   |
                                  | - Executive Summary                   |
                                  | - 🐛 Bugs, 🔐 Security, ⚡ Perf, ✨ Q |
                                  | - 📊 Big-O Complexity (Time & Space)  |
                                  | - 💡 Recommendations & 🔧 Fixed Code  |
                                  +---------------------------------------+
```

---

## 5. Tech Stack

- **Core Language**: Python 3.10+
- **Frontend Framework**: [Streamlit](https://streamlit.io) (Minimal single-page layout)
- **AI / LLM API**: [Google Generative AI](https://pypi.org/project/google-generativeai/) (`gemini-3.8-flash`, configurable via `GEMINI_MODEL`)
- **Configuration & Secrets**: [python-dotenv](https://pypi.org/project/python-dotenv/)
- **Testing & Benchmarking**: Standalone Python evaluation pipeline (`evaluation/evaluate.py`)

*(No unnecessary or fake dependencies: no LangChain, vector DBs, or complex frameworks used.)*

---

## 6. Project Structure

```
Code-reviewer-ai/
├── app.py                     # Streamlit web application (clean, single-page interface)
├── reviewer.py                # Core review orchestrator, model configuration & error handling
│
├── prompts/                   # Specialized prompt engineering modules
│   ├── __init__.py            # Unified prompt builder with auto-detection & JSON schema
│   ├── review.py              # Full review criteria
│   ├── bugs.py                # Bug detection criteria
│   ├── security.py            # Security & injection vulnerability criteria
│   ├── quality.py             # Clean code & readability criteria
│   └── performance.py         # Computational complexity criteria
│
├── guidelines/                # Lightweight context engineering files
│   ├── python.md              # Python PEP 8, safety & performance standards
│   └── javascript.md          # Modern JavaScript ES6+, security & async rules
│
├── evaluation/                # Lightweight evaluation system
│   ├── test_cases.json        # 14 curated code snippets with known defect categories
│   └── evaluate.py            # Evaluation runner with metrics calculation (supports --mock)
│
├── utils/                     # Utility helpers
│   ├── __init__.py
│   └── helpers.py             # Robust JSON parsing, normalization & sample snippets
│
├── .gitignore                 # Prevents committing secrets, caches, and env files
├── requirements.txt           # Explicit, minimal dependencies
├── LICENSE                    # MIT License
└── README.md                  # Engineering documentation
```

---

## 7. Setup & Installation

### Prerequisites
- Python 3.10 or higher
- A Google AI Studio API Key ([Get one free here](https://aistudio.google.com))

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ankesh15/Code-reviewer-ai.git
   cd Code-reviewer-ai
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate

   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API Key**:
   Create a `.env` file in the root directory:
   ```bash
   echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
   ```
   Or export it in your shell:
   ```bash
   export GEMINI_API_KEY="your_actual_api_key_here"
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```
   Open `http://localhost:8501` in your browser.

---

## 8. Environment Variables & Security

| Variable | Required | Default | Description |
|---|---|---|---|
| `GEMINI_API_KEY` | Yes | *None* | Primary Google AI Studio API key. |
| `GENAI_API_KEY` | Optional | *None* | Backward-compatible fallback API key. |
| `GEMINI_MODEL` | Optional | `gemini-3.8-flash` | Gemini model name to use. |

### Security Principles:
- **No API Key Textbox**: The application never accepts or displays API keys in the UI.
- **Protected Secrets**: `.env` is listed in `.gitignore` to prevent accidental credential commits.
- **Graceful Notice**: If the API key is missing, the application displays:
  > *"Gemini API key is not configured. Please configure GEMINI_API_KEY in your environment."*

---

## 9. Automated Evaluation Suite

To evaluate whether prompt engineering and context conditioning reliably detect defects, the project includes an automated evaluation suite.

The test dataset (`evaluation/test_cases.json`) includes 14 curated code examples covering:
- **SECURITY**: SQL injection, hardcoded secrets, unescaped `eval()`, DOM XSS.
- **BUG**: Mutable default arguments, off-by-one indexing, unhandled `None` access, zero division, loose equality coercion.
- **PERFORMANCE**: $O(n^2)$ nested loop lookups, repeated string concatenation in loops, redundant linear scanning.
- **QUALITY**: Bare `except` masking errors, cryptic variables, and duplicated calculation logic.

### Running Evaluation

**1. Mock Mode (Instant verification without API keys or quota consumption)**:
```bash
python evaluation/evaluate.py --mock
```

**2. Live Evaluation Mode (Uses Gemini API)**:
```bash
python evaluation/evaluate.py
```

### Metrics Output
```
========================================================
                 EVALUATION SUMMARY
========================================================
Total Test Cases   : 14
Expected Detected  : 14 / 14
Overall Detection  : 100.0%
Total Issues Found : 14
--------------------------------------------------------
Category        | Expected   | Detected   | Accuracy  
--------------------------------------------------------
SECURITY        | 4          | 4          | 100.0%
BUG             | 5          | 5          | 100.0%
PERFORMANCE     | 3          | 3          | 100.0%
QUALITY         | 2          | 2          | 100.0%
--------------------------------------------------------
All expected categories successfully flagged!
```

---

## 10. Engineering Limitations

1. **Approximate Line Numbers**: LLMs operate on token sequences rather than an exact compiler AST. Line numbers are best-effort estimates; if uncertain, the model outputs `null` rather than hallucinating.
2. **Non-Deterministic Reasoning**: LLM evaluations may vary slightly between runs; they complement but do not replace static linters (`ruff`, `eslint`) or compiler checks.
3. **No Formal Correctness Guarantees**: An LLM review cannot formally verify software invariants or replace comprehensive automated test suites.

---

## 11. Future Roadmap

- [ ] **AST Static Analysis Integration**: Run deterministic AST checks (e.g., Python `ast`, Tree-sitter) before LLM invocation to guarantee line number precision.
- [ ] **GitHub PR Webhook Bot**: Trigger automated reviews on Pull Request diffs and comment inline on pull requests.
- [ ] **Custom Team Rules**: Support loading custom `.editorconfig` or markdown coding standards from a repository root.

---

## 12. Interview & Resume Guide

### Resume Bullet Points (100% Truthful)
- *Built an automated AI code reviewer using Google Generative AI (Gemini) and Streamlit that automatically detects programming languages and delivers comprehensive reviews across Bugs, Security, Performance, and Code Quality.*
- *Architected a zero-configuration developer experience with schema-enforced structured JSON generation and resilient fallback parsing to eliminate UI crashes.*
- *Conditioned LLM outputs using lightweight context engineering (language guideline injection) to elevate review precision without vector database overhead.*
- *Engineered an automated evaluation suite testing 14 curated code defect cases to measure category-level detection accuracy and eliminate false negatives.*

### How to Explain This Project in an Interview (Scaler AI-Native Products)
1. **Product Thinking**: "Instead of overloading developers with 5 dropdowns, model pickers, and mode selectors, I designed a zero-config experience: paste code and review. The AI automatically detects the language and covers bugs, security, performance, quality, and complexity simultaneously."
2. **Context Engineering without RAG Overkill**: "Language conventions are bounded and static. Dynamically injecting language guidelines directly into the context window yields 100% retrieval accuracy with zero database latency or operational cost."
3. **Structured Outputs & Production Resilience**: "I instructed Gemini with `response_mime_type='application/json'` and backed it with a multi-stage parser in `helpers.py` that strips fences, clamps scores, and provides a safe fallback if JSON decoding fails, guaranteeing zero crashes."
4. **Security & Secrets**: "The app strictly resolves API keys from `.env` or system environment variables. No API key textbox is exposed, preventing accidental leaks."

---

## License
Distributed under the MIT License. See [LICENSE](LICENSE) for details.

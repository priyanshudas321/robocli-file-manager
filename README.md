# 🤖 RoboCLI: AI-Powered Autonomous File Agent

RoboCLI is a modular AI agent that bridges **Google Gemini 2.0 Flash** (via OpenRouter) with your local Windows file system. Built for the 2026 Robothon, it allows users to manage, search, and organize local data using natural language commands while strictly adhering to **Zero-Trust** security principles.

---


## 🌟 Key Features
* **Natural Language Processing:** Translates plain English instructions into precise system actions using Gemini 2.0.
* **Zero-Trust Security:** Hard-coded exclusions for system-critical directories (`C:\Windows`, `Program Files`) and hidden developer metadata.
* **Modular Architecture:** Distinct separation between AI Orchestration (`main.py`), Discovery (`search.py`), and Operations (`organize.py`).
* **Safe-by-Default:** Supports dry-run execution to preview file system changes before they are committed.

---

## 🛠️ Installation & Setup

### 1. Prerequisites
* Python 3.10+
* OpenRouter API Key

### 2. Environment Setup
```powershell
# Clone the repository
git clone [https://github.com/priyanshudas321/robocli-file-manager.git](https://github.com/priyanshudas321/robocli-file-manager.git)
cd robocli-file-manager

# Initialize and activate Virtual Environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

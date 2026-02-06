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
## 3️⃣ API Configuration

Create a `.env` file in the root directory and add your API key.

> ⚠️ Note:  
> This file is locally stored and protected by `.gitignore` to ensure professional security standards.

### Example `.env` file

```env
OPENROUTER_API_KEY=your_key_here

##make changes in the main.py
in the main.py file enter your API key from openrouter.AI
in the given below place

API_KEY = "ENTER_YOUR_API_KEYS"
```

---

# 🎮 Usage Guide

## 🤖 Agent Mode (Autonomous)

Launch the agent and talk to your computer in plain English:

```powershell
python main.py
```

**Example Command:**

```
Find all PDFs in my robot-test folder
```

---

## 🔍 Manual Search (Discovery Module)

Direct access to the secure search engine:

```powershell
python search.py --path "C:\Users\Name\Downloads" --ext .pdf
```

---

# 🛡️ Security Policy

This agent is built with **safety as a first principle**.  
It strictly refuses to traverse the following locations:

### 🚫 Operating System Folders
- `C:\Windows`
- `C:\Windows\System32`
- `System Volume Information`

### 🚫 Program Directories
- `C:\Program Files`
- `C:\Program Files (x86)`

### 🚫 Hidden / Metadata Folders
- `.git`
- `.env`
- `$Recycle.Bin`

# Initialize and activate Virtual Environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt



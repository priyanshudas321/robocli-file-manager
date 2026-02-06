# Local File Robot Usage Guide

This agent skill allows you to programmatically search and organize files using Zero-Trust security principles.

## Components

1.  **`search.py`**: Scans for files and outputs JSON.
2.  **`organize.py`**: Reads JSON input and moves files.

## How to Run

### 1. Basic Search

Search for specific file extensions. Use the `--path` to specify where to start.

```powershell
# Search for PDFs in your Downloads folder
python LocalFileRobot/search.py --path "C:\Users\YourName\Downloads" --ext .pdf
```

### 2. Dry-Run Organization (Planning)

See what _would_ happen without actually moving files. You can pipe the search output directly to the organizer.

```powershell
# Plan to move all PDFs from Downloads to a "PDFs" folder on Desktop
python LocalFileRobot/search.py --path "C:\Users\YourName\Downloads" --ext .pdf | python LocalFileRobot/organize.py --dest "C:\Users\YourName\Desktop\PDFs"
```

### 3. Execution (Dangerous)

Actually move the files. Add the `--execute` flag.

```powershell
# MOVE files
python LocalFileRobot/search.py --path "C:\Users\YourName\Downloads" --ext .pdf | python LocalFileRobot/organize.py --dest "C:\Users\YourName\Desktop\PDFs" --execute
```

## Security

- **Zero-Trust**: The robot will strictly refuse to search `C:\Windows`, `C:\Program Files`, or hidden folders (like `.git`).
- **Safe Mode**: By default, `organize.py` only prints a plan. You must explicitly add `--execute` to make changes.

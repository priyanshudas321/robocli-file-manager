import os
import json
import argparse
import sys
from pathlib import Path

# Try to import colorama for colored output, fallback if not present
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    comp_available = True
except ImportError:
    comp_available = False
    
class Colors:
    GREEN = Fore.GREEN if comp_available else ""
    RED = Fore.RED if comp_available else ""
    YELLOW = Fore.YELLOW if comp_available else ""
    CYAN = Fore.CYAN if comp_available else ""
    RESET = Style.RESET_ALL if comp_available else ""

# Zero-Trust Exclusions
EXCLUDED_DIRS = {
    'C:\\Windows',
    'C:\\Program Files',
    'C:\\Program Files (x86)',
    '$Recycle.Bin',
    'System Volume Information'
}

def is_safe_path(path_obj):
    """
    Checks if the path is safe to traverse.
    Excludes system directories and hidden folders (starting with .).
    """
    path_str = str(path_obj)
    
    # Check absolute system paths
    for excluded in EXCLUDED_DIRS:
        if path_str.lower().startswith(excluded.lower()):
            return False
            
    # Check for hidden directories in the current part
    parts = path_obj.parts
    for part in parts:
        if part.startswith('.') and len(part) > 1: # Ignore current dir '.' but catch .git, .config
            # Allow '.agent' folder as it's our working directory
            if part.lower() == '.agent':
                continue
            return False
            
    return True

def search_files(root_dir, extension=None):
    results = []
    root_path = Path(root_dir).resolve()
    
    log(f"{Colors.CYAN}Starting search in: {root_path}{Colors.RESET}")
    
    if not is_safe_path(root_path):
        log(f"{Colors.RED}Security/Safety Alert: Skipping unsafe root directory {root_path}{Colors.RESET}")
        return []

    try:
        for root, dirs, files in os.walk(root_path):
            current_path = Path(root)
            
            # Modify dirs in-place to skip unsafe/hidden directories during traversal
            # This prevents os.walk from entering them
            dirs[:] = [d for d in dirs if not d.startswith('.') and is_safe_path(current_path / d)]
            
            if not is_safe_path(current_path):
                continue
                
            for file in files:
                if extension and not file.lower().endswith(extension.lower()):
                    continue
                    
                full_path = current_path / file
                
                try:
                    file_stat = full_path.stat()
                    results.append({
                        "name": file,
                        "path": str(full_path),
                        "size": file_stat.st_size,
                        "extension": full_path.suffix.lower()
                    })
                except (PermissionError, OSError) as e:
                    log(f"{Colors.YELLOW}Skipping file (access denied): {full_path} - {e}{Colors.RESET}")
                    
    except (PermissionError, OSError) as e:
        log(f"{Colors.RED}Directory access denied: {root_path} - {e}{Colors.RESET}")

    return results

def log(message):
    """Log to stderr so stdout remains clean for JSON"""
    print(message, file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Local File Robot - Search Module")
    parser.add_argument("--path", required=True, help="Root directory to start search")
    parser.add_argument("--ext", help="Filter by file extension (e.g., .pdf)")
    
    args = parser.parse_args()
    
    found_files = search_files(args.path, args.ext)
    
    log(f"{Colors.GREEN}Search complete. Found {len(found_files)} files.{Colors.RESET}")
    
    # Output ONLY valid JSON to stdout
    print(json.dumps(found_files, indent=2))

import os
import shutil
import json
import argparse
import sys
from pathlib import Path

# Try to import colorama for colored output
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

def log(message):
    print(message, file=sys.stderr)

def generate_plan(files, dest_dir):
    plan = []
    dest_path = Path(dest_dir).resolve()
    
    for file_info in files:
        src_path = Path(file_info['path'])
        # Simple organization strategy: Move all to dest_dir
        # Can be enhanced to group by extension in subfolders if needed
        # For now, following user request "target actions (Search, Move, Group)" logic
        # Let's support a flat move to start, or group by extension if implied.
        # User said: "Group by extension" in the prompt example ("Group"). 
        # Let's implement grouping by extension.
        
        ext = file_info['extension'].lstrip('.').lower() or 'no_extension'
        target_folder = dest_path / ext
        target_path = target_folder / src_path.name
        
        plan.append({
            "source": str(src_path),
            "destination": str(target_path),
            "target_folder": str(target_folder)
        })
        
    return plan

def execute_plan(plan):
    results = {
        "success": [],
        "errors": []
    }
    
    for item in plan:
        src = Path(item['source'])
        dest = Path(item['destination'])
        target_folder = Path(item['target_folder'])
        
        try:
            # Create target folder if it doesn't exist
            if not target_folder.exists():
                os.makedirs(target_folder, exist_ok=True)
                
            # Check if destination file already exists
            if dest.exists():
                # Simple conflict resolution: rename
                base = dest.stem
                suffix = dest.suffix
                counter = 1
                while dest.exists():
                    dest = target_folder / f"{base}_{counter}{suffix}"
                    counter += 1
            
            log(f"{Colors.YELLOW}Moving: {src} -> {dest}{Colors.RESET}")
            shutil.move(str(src), str(dest))
            
            # Verification
            if dest.exists() and not src.exists():
                results["success"].append({
                    "file": src.name,
                    "from": str(src),
                    "to": str(dest)
                })
            else:
                 # In case move turned into copy (e.g. across drives), src might still exist
                 # But shutil.move usually deletes src. 
                 # If verified existence of new file:
                 if dest.exists():
                     results["success"].append({"file": src.name, "note": "Moved (src check skipped)"})
                 else:
                     raise OSError("Destination file not found after move")

        except Exception as e:
            log(f"{Colors.RED}Error moving {src.name}: {e}{Colors.RESET}")
            results["errors"].append({
                "file": src.name,
                "error": str(e)
            })
            
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Local File Robot - Organize Module")
    parser.add_argument("--files", help="JSON string of files to organize (reads from stdin if not provided)")
    parser.add_argument("--dest", required=True, help="Destination root directory")
    parser.add_argument("--execute", action="store_true", help="Execute the moves (default is dry-run/plan)")
    
    args = parser.parse_args()
    
    files_input = args.files
    if not files_input:
        # Read from stdin if available
        if not sys.stdin.isatty():
            files_input = sys.stdin.read()
            
    if not files_input:
        log(f"{Colors.RED}Error: No files provided via --files or stdin{Colors.RESET}")
        parser.print_help()
        sys.exit(1)
        
    try:
        files = json.loads(files_input)
    except json.JSONDecodeError:
        log(f"{Colors.RED}Invalid JSON input for --files{Colors.RESET}")
        sys.exit(1)
        
    dest_dir = args.dest
    
    if not args.execute:
        log(f"{Colors.CYAN}Generating Plan (Dry Run)...{Colors.RESET}")
        plan = generate_plan(files, dest_dir)
        print(json.dumps(plan, indent=2))
        sys.exit(0)
    else:
        log(f"{Colors.CYAN}Executing Plan...{Colors.RESET}")
        plan = generate_plan(files, dest_dir)
        results = execute_plan(plan)
        
        log(f"{Colors.GREEN}Execution Complete.{Colors.RESET}")
        log(f"Moved: {len(results['success'])}, Errors: {len(results['errors'])}")
        print(json.dumps(results, indent=2))

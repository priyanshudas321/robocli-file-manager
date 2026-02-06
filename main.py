Timport os
import json
import subprocess
import sys
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Using the direct key to bypass .env loading issues for the deadline
API_KEY = "ENTER_YOUR_API_KEYS"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)

def run_robot():
    print("🤖 Robot Initializing...")
    user_prompt = input("🤖 Robot Online. What is my task? ")
    
    system_instr = "You are a file robot. Return ONLY a valid JSON object. Example: {\"action\": \"find\", \"path\": \"C:\\\\Users\", \"ext\": \".pdf\"}"
    
    try:
        completion = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[
                {"role": "system", "content": system_instr},
                {"role": "user", "content": user_prompt}
            ]
        )

        content = completion.choices[0].message.content.strip()
        
        # Strip any markdown backticks if Gemini includes them
        if "```" in content:
            content = content.split("```")[1].replace("json", "").strip()
            
        command = json.loads(content)
        
        if command['action'] == 'find':
            path = command.get('path', os.getcwd())
            ext = command.get('ext', '.pdf')
            print(f"🔍 Searching for {ext} in {path}...")
            
            result = subprocess.run(
                [sys.executable, 'search.py', '--path', path, '--ext', ext], 
                capture_output=True, 
                text=True
            )
            print(result.stdout)
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_robot()

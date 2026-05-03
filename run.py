import subprocess
import sys
import time
import threading
import webbrowser

def run_backend():
    subprocess.run([sys.executable, "-m", "uvicorn", "backend:app", "--reload", "--port", "8000"])

def run_frontend():
    time.sleep(3)
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

if __name__ == "__main__":
    print("=" * 50)
    print("👮 Police Rulebook Assistant - Starting...")
    print("=" * 50)
    
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    time.sleep(2)
    webbrowser.open("http://localhost:8501")
    
    run_frontend()
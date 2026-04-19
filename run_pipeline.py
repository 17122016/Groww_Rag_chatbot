import subprocess
import os
import sys
from datetime import datetime

def run_step(name, command):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = "ingest_pipeline.log"
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"STEP: {name}\n")
        f.write(f"TIME: {timestamp}\n")
        f.write(f"{'='*50}\n\n")
        
        print(f"Running {name}...")
        try:
            # Change directory to the root of the project for command execution
            process = subprocess.Popen(
                command, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8"
            )
            
            for line in process.stdout:
                sys.stdout.write(line)
                f.write(line)
                
            process.wait()
            if process.returncode == 0:
                f.write(f"\nSUCCESS: {name} completed.\n")
                print(f"SUCCESS: {name} completed.")
            else:
                f.write(f"\nERROR: {name} failed with exit code {process.returncode}\n")
                print(f"FAILED: {name} failed.")
                return False
        except Exception as e:
            f.write(f"\nCRITICAL ERROR in {name}: {str(e)}\n")
            print(f"CRITICAL ERROR in {name}: {e}")
            return False
            
    return True

def main():
    # Root directory setup
    log_file = "ingest_pipeline.log"
    if os.path.exists(log_file):
        os.remove(log_file)
        
    print("Starting Automated Ingest Pipeline Run...")
    
    steps = [
        ("Phase A: Scraping Service", "python Implementation_Phases/Phase_A_Data_Ingestion/scraper.py"),
        ("Phase B: Preprocessing Service", "python Implementation_Phases/Phase_B_Preprocessing/preprocessor.py"),
        ("Phase C: Embedding & Cloud Sync", "python Implementation_Phases/Phase_C_Embedding/embedder.py")
    ]
    
    for name, cmd in steps:
        if not run_step(name, cmd):
            print("\nPipeline stopped due to errors.")
            break
    else:
        print("\nFull Pipeline Ingestion Sync Complete!")

if __name__ == "__main__":
    main()

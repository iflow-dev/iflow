#!/usr/bin/env python3
"""
Test monitoring script that runs tests and monitors for completion
"""
import subprocess
import time
import signal
import sys
import os

def run_and_monitor_test():
    """Run the test and monitor for completion"""
    print("Starting test run...")
    
    # Build the test command
    cmd = [sys.executable, "tests/run_radish.py", "local", "tests/features/test_artifact_creation.feature"]
    
    print(f"Running: {' '.join(cmd)}")
    
    # Start the test process
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    start_time = time.time()
    max_duration = 180  # 3 minutes in seconds
    check_interval = 10  # 10 seconds
    
    print(f"Test started at {time.strftime('%H:%M:%S')}")
    print(f"Will monitor for up to {max_duration} seconds, checking every {check_interval} seconds")
    
    try:
        while True:
            elapsed = time.time() - start_time
            
            # Check if process has completed
            return_code = process.poll()
            
            if return_code is not None:
                # Process has completed
                stdout, stderr = process.communicate()
                print(f"\n✅ Test completed at {time.strftime('%H:%M:%S')}")
                print(f"Duration: {elapsed:.1f} seconds")
                print(f"Return code: {return_code}")
                
                if stdout:
                    print("STDOUT:")
                    print(stdout[-1000:] if len(stdout) > 1000 else stdout)  # Last 1000 chars
                
                if stderr:
                    print("STDERR:")
                    print(stderr[-1000:] if len(stderr) > 1000 else stderr)  # Last 1000 chars
                
                return return_code
            
            # Check if we've exceeded max duration
            if elapsed >= max_duration:
                print(f"\n⏰ Test timeout reached ({max_duration} seconds)")
                print("Terminating test process...")
                process.terminate()
                
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    print("Force killing process...")
                    process.kill()
                    process.wait()
                
                return -1
            
            # Print progress
            print(f"⏳ Test still running... {elapsed:.1f}s elapsed")
            
            # Wait for next check
            time.sleep(check_interval)
    
    except KeyboardInterrupt:
        print("\n🛑 Test monitoring interrupted by user")
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        return -2

if __name__ == "__main__":
    exit_code = run_and_monitor_test()
    sys.exit(exit_code)

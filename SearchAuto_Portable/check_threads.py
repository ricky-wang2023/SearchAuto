#!/usr/bin/env python3
"""
Simple script to check what threads are currently running
"""

import threading
import time

def check_running_threads():
    """Check and display all currently running threads"""
    print("=== Currently Running Threads ===")
    
    # Get all active threads
    active_threads = threading.enumerate()
    
    if not active_threads:
        print("No threads are currently running.")
        return
    
    print(f"Total active threads: {len(active_threads)}")
    print()
    
    for i, thread in enumerate(active_threads, 1):
        print(f"{i}. Thread Name: {thread.name}")
        print(f"   Thread ID: {thread.ident}")
        print(f"   Is Daemon: {thread.daemon}")
        print(f"   Is Alive: {thread.is_alive()}")
        print(f"   Function: {thread._target.__name__ if hasattr(thread, '_target') and thread._target else 'Unknown'}")
        print()

if __name__ == "__main__":
    check_running_threads()
    
    # Keep checking every 5 seconds
    print("Monitoring threads... (Press Ctrl+C to stop)")
    try:
        while True:
            time.sleep(5)
            print("\n" + "="*50)
            check_running_threads()
    except KeyboardInterrupt:
        print("\nThread monitoring stopped.") 
#!/usr/bin/env python3
"""
Debug script to run the benefit orchestrator creation with proper error handling
"""

import traceback
import sys
import os

# Add the current directory to path so we can import the main script
sys.path.insert(0, os.getcwd())

try:
    print("Starting debug script...")
    
    # Import the main function
    from create_benefit_orchestrator import main
    
    print("Running main function...")
    main()
    
    print("Script completed successfully!")
    
except Exception as e:
    print(f"❌ Error occurred: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    
    # Also save error to file for analysis
    with open("error_log.txt", "w") as f:
        f.write(f"Error: {e}\n")
        f.write("\nTraceback:\n")
        f.write(traceback.format_exc())
    
    print("\nError details saved to error_log.txt") 
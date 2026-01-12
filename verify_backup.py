import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from app.services.summary_service import SummaryService

def test_backup():
    print("Testing backup models...")
    service = SummaryService()
    chunks = [{"text": "This is a short test transcript to verify the summarization service is working and using backup models correctly."}]
    
    try:
        summary = service.generate_summary(chunks)
        print("\nFinal Result: Success")
        print(f"Summary: {summary}")
    except Exception as e:
        print(f"\nFinal Result: Failed with error: {e}")

if __name__ == "__main__":
    test_backup()

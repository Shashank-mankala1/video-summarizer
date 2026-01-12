
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.workers.ingest_worker import run_ingestion

print(run_ingestion)

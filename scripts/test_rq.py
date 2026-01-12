
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.rq_queue import ingestion_queue
from app.workers.test_worker import say_hello

job = ingestion_queue.enqueue(say_hello)

print("Job ID:", job.id)
print("Job status:", job.get_status())

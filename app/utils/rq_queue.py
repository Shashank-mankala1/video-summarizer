import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rq import Queue
from app.utils.redis_conn import redis_conn

ingestion_queue = Queue(
    name="ingestion",
    connection=redis_conn
)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.redis_conn import redis_conn

redis_conn.set("test_key", "hello")
value = redis_conn.get("test_key")

print(value)

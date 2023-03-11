from pymilvus import connections
import os

class MilvusConnection:
    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self._conn = None

    def connect(self):
        if not self._conn:
            self._conn = connections.connect(**self._kwargs)
        return self._conn
    
pool = MilvusConnection(
    uri=f"{os.environ.get('MILVUS_HOST')}:{os.environ.get('MILVUS_PORT')}",
    user=os.environ.get('DB_NAME'),
    password=os.environ.get('DB_PASSWORD'),
    secure=True,
)

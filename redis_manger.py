import redis
import platform

# 拿到一个redis的连接池
pool = redis.ConnectionPool(host='192.168.0.11', port=6379, max_connections=2, password="abc123")
# 从池子中拿一个链接
conn = redis.Redis(connection_pool=pool, decode_responses=True)

if platform.system() == 'Windows':
    conn.select(0)
else:
    conn.select(8)
def set_version():
    version=conn.get('version')
    if version==None:
        conn.set('version',0)
    else:
        version=int(version.decode('utf-8'))
        conn.set('version', version+1)

def get_version():
    version = conn.get('version')
    if version==None:
        return 0
    else:
        version=int(version.decode('utf-8'))
        return version
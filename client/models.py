from rediscluster import StrictRedisCluster
from redis import StrictRedis
import json
import sys

# Create your models here.

redis_conns = {}
datatypes = {
    'none': 'get',
    'string': 'get',
    'list': 'lrange',
    'set': 'smembers',
    'zset': 'zrange',
    'hash': 'hgetall',
}


def get(ip, port, password, key):
    try:
        redis_nodes = [{'host': ip, 'port': int(port)}]
        conn = redis_conns.get(json.dumps(redis_nodes), False)
        if not conn:
            conn = redis_conn(redis_nodes, password or None)
        if key == '*':
            result = conn.keys()
            result.sort()
            result = json.dumps(result, ensure_ascii=False)
        else:
            datatype = conn.type(key)
            result = datatype in ('list', 'zset') and getattr(conn, datatypes[datatype])(key, 0, -1) or getattr(conn, datatypes[datatype])(key)
            size = str(sys.getsizeof(result)) + 'bytes'
            value = json.dumps(isinstance(result, set) and list(result) or result, ensure_ascii=False)
            result = json.dumps({'key': key, 'value': value, 'type': datatype, 'size': size})
    except Exception as e:
        result = str(e)
    return result


def redis_conn(redis_nodes, password=None):
    try:
        conn = StrictRedisCluster(startup_nodes=redis_nodes, decode_responses=True, password=password)
        redis_conns[json.dumps(redis_nodes)] = conn
    except Exception as e:
        print(e)
        conn = StrictRedis(host=redis_nodes[0]['host'], port=redis_nodes[0]['port'], decode_responses=True, password=password)
        redis_conns[json.dumps(redis_nodes)] = conn
    return conn

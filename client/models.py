from rediscluster import StrictRedisCluster
from redis import StrictRedis
import json
import sys

redistypes = ['standalone', 'cluster']
conntypes = {
    # '127.0.0.1:6379': 'standalone',
    # '127.0.0.1:7000': 'cluster'
}
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
        conn = _redis_conn(ip, port, password=password or None)
        if key == '*':
            result = conn.scan(count=conn.dbsize())[1]
            result.sort()
            result = json.dumps(result, ensure_ascii=False)
        else:
            datatype = conn.type(key)
            value = datatype in ('list', 'zset') and getattr(conn, datatypes[datatype])(key, 0, -1) or getattr(conn, datatypes[datatype])(key)
            value = json.dumps(isinstance(value, set) and list(value) or value, ensure_ascii=False)
            size = str(sys.getsizeof(value)) + 'bytes'
            result = json.dumps({'key': key, 'value': value, 'type': datatype, 'size': size})
    except Exception as e:
        print(e)
        conntypes.pop('{}:{}'.format(ip, port))
        result = str(e)
    return result


def _redis_conn(ip, port, password=None):
    _key = '{}:{}'.format(ip, port)
    print('"{}": "{}"'.format(_key, conntypes.get(_key, "First log on")))
    if conntypes.get(_key, None) == 'standalone':
        conn = _conn_standalone(ip, port, password)
    elif conntypes.get(_key, None) == 'cluster':
        conn = _conn_cluster(ip, port, password)
    else:
        conn = _conn_cluster(ip, port, password)
        conn = conn or _conn_standalone(ip, port, password)
    return conn


def _conn_standalone(ip, port, password):
    try:
        conn = StrictRedis(host=ip, port=port, decode_responses=True, password=password, socket_connect_timeout=2)
        conntypes['{}:{}'.format(ip, port)] = 'standalone'
    except Exception as e:
        print(e)
        conn = None
    return conn


def _conn_cluster(ip, port, password):
    try:
        conn = StrictRedisCluster(startup_nodes=[{'host': ip, 'port': int(port)}], decode_responses=True, password=password, socket_connect_timeout=2)
        conntypes['{}:{}'.format(ip, port)] = 'cluster'
    except Exception as e:
        print(e)
        conn = None
    return conn

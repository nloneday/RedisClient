from rediscluster import StrictRedisCluster
from redis import StrictRedis
import json
import sys

REDIS_TYPE = ['standalone', 'cluster']
CONNS_TYPE = {
    # '127.0.0.1:6379': 'standalone',
    # '127.0.0.1:7000': 'cluster'
}
DATA_TYPES = {
    'string': 'get',
    'list': 'lrange',
    'set': 'smembers',
    'zset': 'zrange',
    'hash': 'hgetall',
}

CONN = None


def get(ip, port, password, key):
    try:
        _conns_type_key = '{}:{}'.format(ip, port)
        result = []
        conn = _redis_conn(ip, port, password=password or None)
        if key == '*':
            if CONNS_TYPE[_conns_type_key] == 'cluster':
                masters = ['{}:{}'.format(node['host'], node['port']) for node in conn.cluster_nodes() if
                           node['master'] is None]
                keys = sum([conn.dbsize()[node] for node in masters])
                values = conn.scan(count=keys).values()
                for item in values:
                    result.extend(item[1])
            else:
                result = conn.scan(count=conn.dbsize())[1]
            result.sort()
            result = json.dumps(result, ensure_ascii=False)
        else:
            data_type = conn.type(key)
            if data_type in ('list', 'zset'):
                value = getattr(conn, DATA_TYPES[data_type])(key, 0, -1)
            else:
                value = getattr(conn, DATA_TYPES[data_type])(key)
            value = json.dumps(isinstance(value, set) and list(value) or value, ensure_ascii=False)
            size = str(sys.getsizeof(value)) + 'bytes'
            result = json.dumps({'key': key, 'value': value, 'type': data_type, 'size': size})
    except Exception as e:
        print(e)
        CONNS_TYPE.pop('{}:{}'.format(ip, port))
        result = str(e)
    return result


def _redis_conn(ip, port, password=None):
    global CONN
    if CONN is None:
        _conns_type_key = '{}:{}'.format(ip, port)
        print('"{}": "{}"'.format(_conns_type_key, CONNS_TYPE.get(_conns_type_key, "First log on")))
        if CONNS_TYPE.get(_conns_type_key, None) == 'standalone':
            CONN = _conn_standalone(ip, port, password)
        elif CONNS_TYPE.get(_conns_type_key, None) == 'cluster':
            CONN = _conn_cluster(ip, port, password)
        else:
            CONN = _conn_cluster(ip, port, password)
            CONN = CONN or _conn_standalone(ip, port, password)
    return CONN


def _conn_standalone(ip, port, password):
    try:
        conn = StrictRedis(host=ip, port=port, decode_responses=True, password=password, socket_connect_timeout=5,
                           socket_timeout=10, retry_on_timeout=True)
        CONNS_TYPE['{}:{}'.format(ip, port)] = 'standalone'
    except Exception as e:
        print(e)
        conn = None
    return conn


def _conn_cluster(ip, port, password):
    try:
        conn = StrictRedisCluster(startup_nodes=[{'host': ip, 'port': int(port)}], decode_responses=True,
                                  password=password, socket_connect_timeout=5, socket_timeout=10, retry_on_timeout=True)
        CONNS_TYPE['{}:{}'.format(ip, port)] = 'cluster'
    except Exception as e:
        print(e)
        conn = None
    return conn

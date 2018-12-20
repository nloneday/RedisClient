from rediscluster import StrictRedisCluster
from redis import StrictRedis
import json
import sys

REDIS_TYPE = ['standalone', 'cluster']

CONN = {
    # '127.0.0.1:6379:db?:standalone': 'conn',
    # '127.0.0.1:7000:db0:cluster': 'conn'
}
DATA_TYPES = {
    'string': 'get',
    'list': 'lrange',
    'set': 'smembers',
    'zset': 'zrange',
    'hash': 'hkeys',
}


class Redis:
    def __init__(self, redis, host, port, db, password, key, hash_key):
        self._redis = redis
        self._host = host
        self._port = port
        self._db = self._redis == 'standalone' and db or '0'
        self._password = password
        self._key = key
        self._hash_key = hash_key
        self._conn_key = '{}:{}:{}:{}'.format(self._host, self._port, self._db, self._redis)

    def get(self):
        try:
            result = []
            conn = self._redis_conn()
            if self._key == '*':
                if self._redis == 'cluster':
                    masters = ['{}:{}'.format(node['host'], node['port']) for node in conn.cluster_nodes() if
                               node['master'] is None]
                    keys = sum([conn.dbsize()[node] for node in masters])
                    values = conn.scan(count=keys).values()
                    for item in values:
                        result.extend(item[1])
                else:
                    keys = conn.dbsize()
                    result = keys and conn.scan(count=conn.dbsize())[1] or []
                result = json.dumps(result, ensure_ascii=False)
            else:
                data_type = conn.type(self._key)
                if data_type in ('list', 'zset'):
                    value = getattr(conn, DATA_TYPES[data_type])(self._key, 0, -1)
                elif data_type == 'hash' and self._hash_key:
                    value = conn.hget(self._key, self._hash_key)
                else:
                    value = getattr(conn, DATA_TYPES[data_type])(self._key)
                value = json.dumps(isinstance(value, set) and list(value) or value, ensure_ascii=False)
                result = {'key': self._key, 'type': data_type, 'value': value}
                if self._hash_key:
                    result['hash_key'] = self._hash_key
                result = json.dumps(result)
        except Exception as e:
            print(e)
            result = 'Timeout connecting to server, please check!'
            CONN.pop(self._conn_key)
        return result

    def _redis_conn(self):
        conn = None
        global CONN
        try:
            if CONN.get(self._conn_key, None) is None:
                if self._redis == 'standalone':
                    conn = StrictRedis(host=self._host, port=self._port, db=self._db, password=self._password,
                                       decode_responses=True, socket_connect_timeout=5, socket_timeout=5)
                else:
                    conn = StrictRedisCluster(startup_nodes=[{'host': self._host, 'port': int(self._port)}],
                                              password=self._password, decode_responses=True, socket_connect_timeout=5,
                                              socket_timeout=5)
                print('"{}": "{}"'.format(self._conn_key, "First log on"))
                CONN[self._conn_key] = conn
            else:
                conn = CONN[self._conn_key]
        except Exception as e:
            print(e)
        return conn

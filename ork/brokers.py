import redis


class Redis:
    def __init__(self, host='localhost', port=6379):
        self.host = host
        self.port = port

    @staticmethod
    def connect(host, port):
        return redis.StrictRedis(host=host, port=port)

    @property
    def connection(self):
        if getattr(self, '_conn', None):
            return self._conn
        self._conn = self.connect(self.host, self.port)
        return self._conn

    def get(self, key, block=True):
        # XXX: Consider using BRPOPLPUSH for improved reliability.
        command = self.connection.blpop if block else self.connection.lpop
        res = command(key)
        if res:
            return res[1].decode()

    def set(self, key, value):
        return self.connection.rpush(key, value)


BROKERS = {
    'redis': Redis
}


def get_broker(config):
    config = config.get('broker', {})
    try:
        bname = list(config.keys())[0]
    except IndexError:
        bname = 'redis'
    return BROKERS[bname](**config.get(bname, {}))

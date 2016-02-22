import redis

__boardSetKey = '_all_boards'
__passphraseKeyFormat = '{}::passphrase'
__layersKeyFormat = '{}::layers'

@contextmanager
def connect():
    try:
        yield redis.StrictRedis(host='localhost', port=6379)
    finally:
        pass


class Board():
    def exists(id):
        with connect() as r:
            return r.sismember(__boardSetKey, id)

    def __init__(self, id):
        self.id = id

        with connect() as r:
            r.sadd(__boardSetKey, id)

    def __passphraseKey(self):
        return __passphraseKeyFormat.format(self.id)

    def __layersKey(self):
        return __layersKeyFormat.format(self.id)

    def has_passphrase(self):
        with connect() as r:
            return r.exists(self.__passphraseKey())

    def get_passphrase(self):
        with connect() as r:
            return r.get(self.__passphraseKey())

    def set_passphrase(self, passphrase):
        with connect() as r:
            r.set(self.__passphraseKey(), passphrase)

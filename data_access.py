from contextlib import contextmanager
import redis

_boardSetKey = '_all_boards'
_passphraseKeyFormat = '{}::passphrase'
_layersKeyFormat = '{}::layers'

@contextmanager
def connect():
    try:
        yield redis.StrictRedis(host='localhost', port=6379)
    finally:
        pass


class Board():
    def exists(id):
        with connect() as r:
            return r.sismember(_boardSetKey, id)

    def create(id):
        with connect() as r:
            r.sadd(__boardSetKey, id)

        return Board(id)

    def __init__(self, id):
        self.id = id

    def __passphraseKey(self):
        return _passphraseKeyFormat.format(self.id)

    def __layersKey(self):
        return _layersKeyFormat.format(self.id)

    def has_passphrase(self):
        with connect() as r:
            return r.exists(self.__passphraseKey())

    def get_passphrase(self):
        with connect() as r:
            return r.get(self.__passphraseKey())

    def set_passphrase(self, passphrase):
        with connect() as r:
            r.set(self.__passphraseKey(), passphrase)

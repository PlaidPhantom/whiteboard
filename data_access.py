from contextlib import contextmanager
from uuid import uuid4

import json
import redis

_boardSetKey = '_all_boards' # set of all board ids
_passphraseKeyFormat = '{}::passphrase' # board passphrase as string. format board id
_channelNameFormat = '{}::channel' # name of board pubsub channel. format board id
_layerListKeyFormat = '{}::layers' # board's layer ids as list. format board id
_layerKeyFormat = '{}::{}' # layer's string value format board id & layer id

def connectRedis():
    return redis.StrictRedis(host='localhost', port=6379)

@contextmanager
def connect():
    try:
        yield connectRedis()
    finally:
        pass


class Board():
    def exists(id):
        with connect() as r:
            return r.sismember(_boardSetKey, id)

    def create(id):
        with connect() as r:
            r.sadd(_boardSetKey, id)

        return Board(id)

    def __init__(self, id):
        self.id = id

    def __passphraseKey(self):
        return _passphraseKeyFormat.format(self.id)

    def __channelKey(self):
        return _channelNameFormat.format(self.id)

    def __layerListKey(self):
        return _layerListKeyFormat.format(self.id)

    def __layerKey(self, layerId):
        return _layerKeyFormat.format(self.id, layerId)

    def has_passphrase(self):
        with connect() as r:
            return r.exists(self.__passphraseKey())

    def get_passphrase(self):
        with connect() as r:
            return r.get(self.__passphraseKey())

    def set_passphrase(self, passphrase):
        with connect() as r:
            r.set(self.__passphraseKey(), passphrase)

    def getChannelKey(self):
        return self.__channelKey()

    def handleMessage(self, message):
        if message["type"] == "add-path":
            self.appendToPath(message)
            return None
        elif message["type"] == "fin-path":
            return self.startNewPath()

    def startNewPath(self):
        id = str(uuid4())

        with connect() as r:
            r.rpush(self.__layerListKey(), id)
            r.set(self.__layerKey(id), "")

        return { "type": "path-id", "id": id }

    def appendToPath(self, msg):
        with connect() as r:
            r.append(self.__layerKey(msg["id"]), msg["data"])

            r.publish(self.__channelKey(), json.dumps(msg).encode('utf8'))

    def getCurState(self):
        paths = []

        with connect() as r:
            pathIds = [ id.decode('utf8') for id in r.lrange(self.__layerListKey(), 0, -1) ]

            for id in pathIds:
                paths.append({ "id": id, "data": r.get(self.__layerKey(id)).decode('utf8') })

        return { "type": "cur-state", "paths": paths }

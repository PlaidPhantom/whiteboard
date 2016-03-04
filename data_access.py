from contextlib import contextmanager
from uuid import uuid4

import redis

_boardSetKey = '_all_boards'
_passphraseKeyFormat = '{}::passphrase'
_layersKeyFormat = '{}::layers'
_channelNameFormat = '{}::channel'

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

    def __layersKey(self):
        return _layersKeyFormat.format(self.id)

    def __channelKey(self):
        return _channelNameFormat.format(self.id)

    def has_passphrase(self):
        with connect() as r:
            return r.exists(self.__passphraseKey())

    def get_passphrase(self):
        with connect() as r:
            return r.get(self.__passphraseKey())

    def set_passphrase(self, passphrase):
        with connect() as r:
            r.set(self.__passphraseKey(), passphrase)

    def getChannelReceiver(self):
        with connect() as r:
            receiver = r.pubsub(ignore_subscribe_messages=True)
            receiver.subscribe(self.__channelKey())
            return receiver;

    def handleMessage(self, message):
        if msg.type == "add-path":
            self.broadcastToChannel(msg)
            # TODO add to redis path DB
            return None
        elif msg.type == "fin-path":
            return newPathMessage()

    def startNewPath(self):
        return { "type": "path-id", "id": self.newPathId() }

    def broadcastToChannel(self, message):
        with connect() as r:
            r.publish(self.__channelKey(), message)


    def newPathId(self):
        self.pathId = str(uuid4())
        return self.pathId

    def getAllPaths():
        pass

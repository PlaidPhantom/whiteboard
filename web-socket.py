from asyncio import get_event_loop, gather, sleep
import json
from re import match
from sys import argv

from websockets import serve, ConnectionClosed

from data_access import Board, connect

debug = '--debug' in argv

class SocketServer():
    def __init__(self, connection, boardId):
        self.connection = connection
        self.board = Board(boardId)

    async def run(self):
        try:
            # TODO passphrase convo
            msg = json.dumps(self.board.getCurState())
            if debug:
                print('SOCKET: sent state', msg)
            await self.connection.send(msg)
            msg = json.dumps(self.board.startNewPath())
            if debug:
                print('SOCKET: sent path id', msg)
            await self.connection.send(msg)

            await gather(self.listen(), self.watch())

        except ConnectionClosed:
            pass

    async def startNewPath(self):
        await self.connection.send(json.dumps(self.board.startNewPath()))

    async def listen(self):
        while True:
            s = await self.connection.recv()
            if debug:
                print('SOCKET: client sent', s)
            msg = json.loads(s)
            response = self.board.handleMessage(msg)

            if response is not None:
                r = json.dumps(response)
                if debug:
                    print('SOCKET: sent response', r)
                await self.connection.send(r);


    async def watch(self):
        with connect() as r:
            receiver = r.pubsub(ignore_subscribe_messages=True)
            receiver.subscribe(self.board.getChannelKey())

            try:
                while True:
                    msg = receiver.get_message()
                    if msg is None:
                        await sleep(1)
                    elif msg["type"] != "message":
                        if debug:
                            print('SOCKET: ignoring message', json.dumps(msg))
                    else:
                        data = msg['data'].decode('utf8')
                        if debug:
                            print('SOCKET: relaying message', data)

                        await self.connection.send(data)
            finally:
                receiver.close()


async def openConnection(connection, path):
    boardId = path[len('/socket/'):]

    if match('^[A-Za-z0-9_-]+$', boardId) is None:
        return
    else:
        connection = SocketServer(connection, boardId)
        await connection.run()

server = serve(openConnection, port=8082)

get_event_loop().run_until_complete(server)
get_event_loop().run_forever()

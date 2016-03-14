from asyncio import get_event_loop, wait, sleep
import json
from re import match

from websockets import serve

from data_access import Board

class SocketServer():
    def __init__(self, connection, boardId):
        self.connection = connection
        self.board = Board(boardId)

        self.receiver = self.board.getChannelReceiver()

    async def run(self):
        # TODO passphrase convo
        await self.connection.send(json.dumps(self.board.getCurState()))
        await self.connection.send(json.dumps(self.board.startNewPath()))
        await wait([self.listen, self.watch])

    async def startNewPath(self):
        await self.connection.send(json.dumps(self.board.startNewPath()))

    async def listen(self):
        while True:
            msg = json.loads(await self.connection.recv())

            response = self.board.handleMessage(msg)

            if response is not None:
                await self.connection.send(json.dumps(response));


    async def watch(self):
        while True:
            msg = self.receiver.get_message()

            if msg is None:
                await sleep(1)
            if msg.id != self.board.pathId:
                await self.connection.send(msg)


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

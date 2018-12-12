#!/usr/bin/env python

# WS client example

#!/usr/bin/env python3.6

import asyncio
import websockets
from random import *
import datetime

timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
id = randint(1, 100)

message = {'type': 'message', 'channel': 'general', 'sender_id': id, 'content': "Tere, maailm!", 'timestamp': timestamp}


async def msg():
    async with websockets.connect('ws://chat.randohinn.com:8080') as websocket:
        await websocket.send(str(message))
        msg = await websocket.recv()
        print(msg)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(msg())
    asyncio.get_event_loop().run_forever()

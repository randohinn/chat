import asyncio
import websockets
import ast
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.messages
auth = client.users

users = set()

async def join(websocket):
    users.add(websocket)
    message_history = db.entries.find().sort({$natural: -1}).limit(20);
    for message in message_history:
        await asyncio.wait([user.send(message) for user in users])

async def disconnect(websocket):
    users.remove(websocket)

async def send_message(message):
    if users:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([user.send(message) for user in users])

async def message_handler(websocket, path):
    await join(websocket)
    try:
        async for message in websocket:
            msg_dict = ast.literal_eval(message)
            if msg_dict['type'] == "message":
                db.entries.insert_one(msg_dict)
                await send_message(message)
            elif msg_dict['type'] == "auth":
                # Vajab uuid kontrolli veel
                response = {}
                response["status"] = "OK"
                await websocket.send(response)
    except websockets.exceptions.ConnectionClosed:
        await disconnect(websocket)

async def handler(websocket, path):
    consumer_task = asyncio.ensure_future(
        message_handler(websocket, path))
    #producer_task = asyncio.ensure_future(
    #    producer_handler(websocket, path))
    done, pending = await asyncio.wait(
        [consumer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()

if __name__ == '__main__':
    print("Starting chat server")
    start_server = websockets.serve(handler, '0.0.0.0', 8080)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

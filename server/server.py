import asyncio
import websockets

async def connect(websocket):
    print(websocket)

async def message_handler(websocket, path):
    try:
        async for message in websocket:
            print(message)
            print(path)
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")

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
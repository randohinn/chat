#!/usr/bin/env python

# WS client example

#!/usr/bin/env python3.6

import asyncio
import websockets
from random import *
import datetime
import tkinter as tk
import threading
import os

class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        #self.root.quit()
        os._exit(0)

    def run(self):
        self.root = tk.Tk()
        self.root.title("Chat - Programmmeerimise projekt")
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.minsize(800,600)
        self.root.maxsize(800,600)
        label = tk.Label(self.root, text="Hello World")
        label.pack()
        message_text = tk.Entry(self.root, font=("Arial", 12))
        message_text.pack(fill='x')

        self.root.mainloop()



timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
id = randint(1, 100)

message = {'type': 'message', 'channel': 'general', 'sender_id': id, 'content': "Tere, maailm!", 'timestamp': timestamp}


async def msg():
    async with websockets.connect('ws://chat.randohinn.com:8080') as websocket:
        while True:
            #await websocket.send(str(message))
            msg = await websocket.recv()
            print(msg)

if __name__ == '__main__':
    window = App()
    asyncio.get_event_loop().run_until_complete(msg())
    asyncio.get_event_loop().run_forever()

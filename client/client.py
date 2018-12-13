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
import uuid, ast

all_messages = []
message_out = ""
window = ""
socket = 0
id = hex(uuid.getnode())
print(id)

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
        #label.pack()
        self.canvas = tk.Canvas(self.root, scrollregion=(0,0,800,4200))
        self.vbar=tk.Scrollbar(self.root,orient=tk.VERTICAL)
        self.vbar.grid(row=0, column=2, sticky="ns")
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.vbar.set)

        self.root.columnconfigure(0, weight=3)
        self.root.rowconfigure(0, weight=3)

        send_button = tk.Button(self.root, text="Saada", command=self.send_click)
        send_button.grid(row=1, column=1)

        self.message_text = tk.Entry(self.root, font=("Arial", 12))
        self.message_text.grid(row=1, column=0, sticky="we")

        self.canvas.grid(row=0, column=0, sticky="wesn")
        self.root.mainloop()


    def send_click(self):
        global message_out
        timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        message = {'type': 'message', 'channel': 'general', 'sender_id': id, 'content': self.message_text.get(), 'timestamp': timestamp}
        self.message_text.delete(0, 'end')
        message_out = message

async def run():
    websocket = await websockets.connect('ws://chat.randohinn.com:8080')
    while True:
        await msg(websocket)

async def actually_send(websocket):
    global message_out
    print(type(message_out))
    if isinstance(message_out,dict):
        await websocket.send(str(message_out))
        message_out = ""
        print("snet")

async def recieve(websocket):
    global all_messages
    try:
        msg = await websocket.recv()
        print(msg)
        message = ast.literal_eval(msg)
        all_messages.append(message)
        sender_id = window.canvas.create_text(10, 10+(64*(len(all_messages)-1)), anchor="nw", font=('Arial Bold', 10))
        message_text = window.canvas.create_text(10, 30+(64*(len(all_messages)-1)), anchor="nw")

        window.canvas.itemconfig(sender_id, text=str(message['sender_id'])+"    @     "+str(message['timestamp']))
        window.canvas.itemconfig(message_text, text=str(message['content']))
        window.canvas.config(scrollregion=window.canvas.bbox(tk.ALL))
        window.canvas.yview_moveto(1)
    except:
        pass


async def msg(websocket):
    asyncio.ensure_future(actually_send(websocket))
    asyncio.ensure_future(recieve(websocket))
    await asyncio.sleep(.1)

if __name__ == '__main__':
    window = App()
    asyncio.get_event_loop().run_until_complete(run())

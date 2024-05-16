import asyncio
import websockets
import tkinter as tk
from multiprocessing import Process, Pipe
from threading import Thread

window = tk.Tk()

canvas = tk.Canvas(window, width=1080, height=1080, bg='white')

def start_tkinter(command_queue):
    def process_commands():
        while True:
            command = command_queue.recv()
            if command == "clear":
                canvas.delete("all")
            else:
                x, y = map(int, command.split())
                canvas.create_oval(x-3, y-3, x+3, y+3, fill='black')

    pct = Thread(target=process_commands)
    pct.start()

    canvas.pack()
    window.mainloop()
    pct.join()



def start_server(command_queue):
    async def connect_to_server():
        async with websockets.connect("ws://localhost:8765") as websocket:
            while True:
                response = await websocket.recv()
                command_queue.send(response)
                print(f"Received: {response}")

    asyncio.get_event_loop().run_until_complete(connect_to_server())


if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    pt = Process(target=start_tkinter, args=(parent_conn,))
    pt.start()

    ps = Process(target=start_server, args=(child_conn,))
    ps.start()

    pt.join()
    ps.join()
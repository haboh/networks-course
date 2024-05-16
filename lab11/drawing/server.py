import asyncio
import websockets
import tkinter as tk
import queue
from multiprocessing import Process, Pipe

window = tk.Tk()

canvas = tk.Canvas(window, width=1080, height=1080, bg='white')

def start_tkinter(command_queue):
    def draw(event):
        x, y = event.x, event.y
        canvas.create_oval(x-3, y-3, x+3, y+3, fill='black')
        command_queue.send(f"{x} {y}")

    def clear(event):
        canvas.delete("all")
        command_queue.send("clear")

    canvas.bind('<B1-Motion>', draw)
    canvas.bind('<Button-3>', clear)

    canvas.pack()
    window.mainloop()


def start_server(command_queue):
    async def echo(websocket, path):
        while True:
            await websocket.send(command_queue.recv())

    start_server = websockets.serve(echo, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    pt = Process(target=start_tkinter, args=(parent_conn,))
    pt.start()

    ps = Process(target=start_server, args=(child_conn,))
    ps.start()

    pt.join()
    ps.join()
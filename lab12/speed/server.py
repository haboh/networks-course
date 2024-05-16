import socket
import random
import struct
import time
from tkinter import *

PACKET_SIZE = 4096

def receive(host, port):
    if variable.get() == "TCP":
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, int(port)))
            s.listen()
            conn, _ = s.accept()
            with conn:
                data = conn.recv(16)

                start_time, N = struct.unpack_from("dl", data)

                cnt = 0

                for i in range(N):
                    data = conn.recv(PACKET_SIZE)
                    if len(data) == PACKET_SIZE:
                        cnt += 1

                end = time.time()

                speed.delete(0, END)
                speed.insert(0, f"{N * PACKET_SIZE / (end - start_time) / 1024}Mb/s")

                packets.delete(0, END)
                packets.insert(0, f"{cnt} / {N}")
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((host, int(port)))

            data = sock.recv(16)

            start_time, N = struct.unpack_from("dl", data)

            cnt = 0

            for i in range(N):
                data = sock.recv(PACKET_SIZE)
                if len(data) == PACKET_SIZE:
                    cnt += 1

            end = time.time()

            speed.delete(0, END)
            speed.insert(0, f"{N * PACKET_SIZE / (end - start_time) / 1024}Mb/s")

            packets.delete(0, END)
            packets.insert(0, f"{cnt} / {N}")


def clicked():
    receive(src.get(), port.get())

window = Tk()
window.geometry('1080x1080')

variable = StringVar(window)
variable.set("UDP")

proto = OptionMenu(window, variable, "UDP", "TCP")
proto.grid(column=0, row=0)

lbl = Label(window, text="Введите IP")
lbl.grid(column=0, row=1)
src = Entry(window,width=30)
src.grid(column=1, row=1, padx=(20, 0), pady=(20, 20))

lbl2 = Label(window, text="Выберите порт для получения")
lbl2.grid(column=0, row=2)
port = Entry(window,width=30)
port.grid(column=1, row=2, padx=(20, 0), pady=(20, 20))

lbl3 = Label(window, text="Скорость передачи")
lbl3.grid(column=0, row=3)
speed = Entry(window,width=30)
speed.grid(column=1, row=3, padx=(20, 0), pady=(20, 20))
# speed.config(state='readonly')

lbl4 = Label(window, text="Число полученных пакетов")
lbl4.grid(column=0, row=4)
packets = Entry(window,width=30)
packets.grid(column=1, row=4, padx=(20, 0), pady=(20, 20))
# packets.config(state='readonly')

submit = Button(window, text="Получить", command=clicked)
submit.grid(column=0, row=5, padx=(0, 0), pady=(20, 20))

window.mainloop()
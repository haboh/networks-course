import socket
import random
import struct
import time
from tkinter import *

PACKET_SIZE = 4096

def get_random_data():
    return random.randbytes(PACKET_SIZE)

def get_start_time(num):
    return struct.pack("dl", time.time(), num)

def send(src, port, num):
    if variable.get() == "UDP":
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(get_start_time(num), (src, int(port)))
            for i in range(num):
                sock.sendto(get_random_data(), (src, int(port)))
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.connect((src, int(port)))
            soc.sendall(get_start_time(num))
            for i in range(num):
                soc.sendall(get_random_data())

def clicked():
    send(src.get(), port.get(), int(packets_number.get()))

window = Tk()

variable = StringVar(window)
variable.set("UDP")

proto = OptionMenu(window, variable, "UDP", "TCP")
proto.grid(column=0, row=0)

window.geometry('1080x1080')
lbl = Label(window, text="Введите IP адрес получателя")
lbl.grid(column=0, row=1)
src = Entry(window,width=20)
src.grid(column=1, row=1, padx=(20, 0), pady=(20, 20))

lbl2 = Label(window, text="Выберите порт отправки")
lbl2.grid(column=0, row=2)
port = Entry(window,width=20)
port.grid(column=1, row=2, padx=(20, 0), pady=(20, 20))

lbl3 = Label(window, text="Введите количество пакетов для отправки")
lbl3.grid(column=0, row=3)
packets_number = Entry(window,width=20)
packets_number.grid(column=1, row=3, padx=(20, 0), pady=(20, 20))

submit = Button(window, text="Отправить", command=clicked)
submit.grid(column=0, row=4, padx=(0, 0), pady=(20, 20))

window.mainloop()
import datetime
import socket
import time
import pytz

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

tz_Moscow = pytz.timezone('Europe/Moscow') 

while True:
  message = datetime.datetime.now(tz_Moscow).strftime("%H:%M:%S").encode()
  server_socket.sendto(message, ('<broadcast>', 8080))
  time.sleep(1)
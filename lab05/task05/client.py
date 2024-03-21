import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client_socket.bind(('', 8080))

while True:
  time, _ = client_socket.recvfrom(4096)
  print("Time in Saint-Petersburg now:", time.decode())
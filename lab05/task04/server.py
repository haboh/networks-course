import socket
import os

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5050))
server_socket.listen()

while True:
  client, addr = server_socket.accept()
  comm = client.recv(4096).decode()
  print("Command started.")
  print("----------------")
  result = os.system(comm)
  client.send('0'.encode())
  print("----------------")
  print("Command finished.")
  client.close()
import socket 
import sys

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5050))

command = sys.argv[1]
client_socket.send(command.encode())

response = client_socket.recv(4096).decode()
print(response)
  
client_socket.close()
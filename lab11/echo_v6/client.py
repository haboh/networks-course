import socket

client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
client.connect(('::1', 8787)) # ::1 -- localhost ipv6 adress

while True:
    message = input("Enter message: ")
    client.send(message.encode('utf-8'))

    response = client.recv(4096).decode('utf-8')
    print(f"Server responsed: {response}")


client.close()
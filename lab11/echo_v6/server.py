import socket

server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
server.bind(('::1', 8787)) # ::1 -- localhost ipv6 adress
server.listen(1)

print("Server start. Wait for client")

conn, addr = server.accept()

while True:
    print(f"Connection with {addr}")

    data = conn.recv(4096).decode('utf-8')
    print(f"Message got: {data}")

    response = data.upper()
    conn.send(response.encode('utf-8'))

conn.close()

from socket import socket, AF_INET, SOCK_STREAM
import sys
import os

def main():
    server_port = int(sys.argv[1])
    server_address = '127.0.0.1'
    
    web_socket = socket(AF_INET, SOCK_STREAM)
    web_socket.bind((server_address, server_port))

    web_socket.listen()
    while True:
        client, address = web_socket.accept()
        data = client.recv(4096).decode()
        filename = data[5:].split()[0]
        if not os.path.exists(filename):
            client.send(f'''HTTP/1.1 404 Not found'''.encode())
        else:
            with open(filename, 'r') as output_file:
                client.send(f'''HTTP/1.1 200 Ok\n{output_file.read()}'''.encode())
        client.close()


if __name__ == "__main__":
    main()
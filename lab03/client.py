import sys
from socket import socket, AF_INET, SOCK_STREAM


def main():
    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]

    with socket(AF_INET, SOCK_STREAM) as server_socket:
        server_socket.connect((server_host, server_port))
        server_socket.send(
            f'''GET /{filename} HTTP/1.1
                Host: {server_host}'''.encode()
        )

        response = server_socket.recv(4096)
        print(response.decode())


if __name__ == "__main__":
    main()


from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
import sys
import os
from queue import Queue

def process_client(client):
    data = client.recv(4096).decode()
    filename = data[5:].split()[0]
    if not os.path.exists(filename):
        client.send(f'''HTTP/1.1 404 Not found'''.encode())
    else:
        with open(filename, 'r') as output_file:
            client.send(f'''HTTP/1.1 200 Ok\n{output_file.read()}'''.encode())
    

def process_queue(queue, concurrency_level):
    processing_queue = Queue()

    while len(processing_queue) < concurrency_level:
        client = queue.get()
        processing_queue.put(client)

        def process(client):
            process_client(client)
            processing_queue.get()
            client.close()

        thread = Thread(target=process, args=[client])
        thread.run()

def main():
    server_port = int(sys.argv[1])
    concurrency_level = int(sys.argv[2])
    server_address = '127.0.0.1'
    
    web_socket = socket(AF_INET, SOCK_STREAM)
    web_socket.bind((server_address, server_port))

    web_socket.listen()

    client_queue = Queue()

    Thread(target=process_queue, args=[client_queue, concurrency_level]).run()

    while True:
        client, address = web_socket.accept()
        client_queue.put(client)

if __name__ == "__main__":
    main()
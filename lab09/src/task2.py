import socket
import sys

def check_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((ip, port))
    s.close()
    return result

def find_free_ports(ip, start_port, end_port):
    free_ports = []
    for port in range(start_port, end_port + 1):
        if check_port(ip, port) != 0:
            free_ports.append(port)
    return free_ports

def main():
    ip_address = sys.argv[1]
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])
    
    free_ports = find_free_ports(ip_address, start_port, end_port)
    
    print(f'Free port for IP-address {ip_address} in range [{start_port} ... {end_port}]:')
    for port in free_ports:
        print(port)

if __name__ == '__main__':
    main()
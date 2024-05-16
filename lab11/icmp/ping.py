import socket
import struct
import time
import sys
from dns import resolver,reversename

def trace_route(url, num_packets=3):
    destination_ip = socket.gethostbyname(url)
    port = 0

    for ttl in range(1, 30 + 1):
        ttl_exceeded = False
        hop_ip = None
        rtt_times = []

        icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        icmp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        icmp_socket.settimeout(2)

        for i in range(num_packets):
            send_time = time.time()
            packet = b'\x08\x00\xf7\xff\x00\x00\x00\x00'
            icmp_socket.sendto(packet, (destination_ip, port))

            try:
                recv_packet, addr = icmp_socket.recvfrom(1024)
                recv_time = time.time()
                hop_ip = addr[0]
                rtt = (recv_time - send_time) * 1000
                rtt_times.append(rtt)
            except socket.timeout:
                ttl_exceeded = True
                break

        icmp_socket.close()

        if not ttl_exceeded:
            try:
                hop_name = socket.gethostbyaddr(hop_ip)[0]
            except socket.herror:
                hop_name = hop_ip

            print(f"{ttl}: {hop_name} ({hop_ip}) - RTT: {rtt_times} ms")
        else:
            print(f"{ttl}: *")

        if hop_ip == destination_ip:
            break

if len(sys.argv) < 2:
    print("usage: sudo python3 ping.py [url] [message_count]")
else:
    trace_route(sys.argv[1], int(sys.argv[2] if len(sys.argv) == 3 else 3))

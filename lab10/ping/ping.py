import socket
import struct
import time

def checksum(data):
    checksum = 0
    for i in range(0, len(data), 2):
        checksum += (data[i] << 8) + data[i+1]
    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum = ~checksum & 0xFFFF
    return checksum

def ping_url(url):
    try:
        icmp = socket.getprotobyname("icmp")
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        packet_id = 1
        sequence = 1
        payload = b'CHAO'
        
        header = struct.pack('!BBHHH', 8, 0, 0, packet_id, sequence)
        data = header + payload
        
        checksum_value = checksum(data)
        header = struct.pack('!BBHHH', 8, 0, checksum_value, packet_id, sequence)
        packet = header + payload
        
        start_time = time.time()
        
        sock.sendto(packet, (url, 0))
        sock.settimeout(1)
        
        reply, _ = sock.recvfrom(4096)
        
        end_time = time.time()
        
        time_diff = end_time - start_time
    
        icmp_header = reply[20:28]
        icmp_type, icmp_code, _, _, _ = struct.unpack('!BBHHH', icmp_header)
                
        if icmp_type == 0 and icmp_code == 0:
            return f'Ping to {url} successful. Time: {time_diff} seconds', time_diff
        else:
            return f'Ping to {url} failed. ICMP error code: {icmp_type}:{icmp_code}', float('inf')

    except socket.error as e:
        return f'Ping to {url} failed. Error: {e}', float('inf')

def main():
    url = input('Enter ip: ')
    count = input('Enter number of pings (default=infinity): ')
    count = int(count) if count != '' else -1
    
    lost = 0
    total_tries = 0
    total_rtt = 0
    max_rtt = 0
    min_rtt = float('inf')
    
    while count != 0:
        result, diff = ping_url(url)
        if diff != float('inf'):
            total_rtt += diff
            min_rtt = min(min_rtt, diff)
            max_rtt = max(max_rtt, diff)
        else:
            lost += 1
        total_tries += 1

        print(result)
        print(f"min rtt: {min_rtt}, max_rtt: {max_rtt}, avg_rtt: {0 if total_tries == lost else total_rtt / (total_tries - lost)}, lost: {lost / total_tries}")
        
        count -= 1


if __name__ == '__main__':
    main()

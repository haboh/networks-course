import subprocess

def get_ip_address():
    ip = subprocess.check_output(['hostname', '-I']).decode('utf-8').split()[0]
    return ip

def get_netmask():
    netmask = subprocess.check_output(['ip', 'a', 'show', 'eth0']).decode('utf-8').split('\n')[1].split()[1]
    return netmask

if __name__ == '__main__':
    ip_address = get_ip_address()
    netmask = get_netmask()
    
    print(f'IP-adress: {ip_address}')
    print(f'Net mask: {netmask}')
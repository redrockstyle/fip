import socket
import struct
from ipaddress import ip_address
import random
import sys


def ip_obfuscator(ip_str, rand=0):
    ip = {}
    if ip_str == 'localhost':
        ip_str = '127.0.0.1'
    else:
        try:
            ip_address(ip_str)
        except ValueError:
            print(f"ip address is not valid")
            return None
    ip_dec = struct.unpack("!L", socket.inet_aton(ip_str))[0]
    ip['dec8'] = ip_str
    ip['short'] = '.'.join(x for x in ip_str.split('.') if x.strip('0'))  # incorrect convert !!!
    ip['dec32'] = str(ip_dec)
    ip['hex8'] = '.'.join(hex(int(x)) for x in ip_str.split('.'))
    ip['hex32'] = str(hex(ip_dec))
    ip['oct8'] = '.'.join(format(int(x), '04o') for x in ip_str.split('.'))
    ip['oct32'] = oct(ip_dec).replace('o', '')

    if rand:
        rand_str = ['hex8', 'oct8', 'dec8']
        for i in range(rand):
            ip[f'rand{1 + i}'] = '.'.join(
                ip[rand_str[random.randint(0, len(rand_str) - 1)]].split('.')[x] for x in range(4))
    return ip


def print_obf(header, dicty):
    if dicty:
        print(header)
        for k in dicty:
            print(f"{k}:\t{dicty[k]}")


def main():
    if len(sys.argv) == 2:
        print_obf("IP OBFUSCATION", ip_obfuscator(sys.argv[1]))
    elif len(sys.argv) == 3:
        print_obf(f"IP WITH RANDOM {int(sys.argv[2])}", ip_obfuscator(sys.argv[1], int(sys.argv[2])))
    else:
        print(f"Usage: {sys.argv[0]} <ip> [<number_rand>]")


if __name__ == '__main__':
    main()

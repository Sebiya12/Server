import socket
import struct

MULTICAST_GROUP = "233.0.0.1"
PORT = 1502

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    print("UDP Server started. Enter messages to send:")

    while True:
        msg = input("Введите строку для передачи клиентам: ")
        sock.sendto(msg.encode('utf-8'), (MULTICAST_GROUP, PORT))
        print("Отправлено.")

if __name__ == "__main__":
    main()

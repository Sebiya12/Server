import socket
import struct

MULTICAST_GROUP = "233.0.0.1"
PORT = 1502

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(("", PORT))

    mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print("Ожидание сообщения от сервера...")

    while True:
        data, addr = sock.recvfrom(1024)
        print("Получено сообщение:", data.decode('utf-8').strip())

if __name__ == "__main__":
    main()

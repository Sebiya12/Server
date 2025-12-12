import socket
from date_message import DateMessage

HOST = "localhost"
PORT = 1500

def main():
    s = socket.socket()
    s.connect((HOST, PORT))

    data = s.recv(4096)
    msg = DateMessage.deserialize(data)

    print("Сообщение:", msg.message)
    print("Дата:", msg.date)

if __name__ == "__main__":
    main()

import socket
from date_message import DateMessage

HOST = "0.0.0.0"
PORT = 1500

def main():
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen(5)

    print("Starting the server")

    while True:
        conn, addr = s.accept()
        print("Connection accepted from", addr)

        msg = DateMessage("Текущая дата/время на сервере")
        conn.sendall(msg.serialize())
        conn.close()

if __name__ == "__main__":
    main()

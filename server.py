import socket

class Server:

    def __init__(self, SERVER_IP, PORT, CONCURENT_CONNECTIONS=1):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((SERVER_IP, PORT))
        print("S-a facut bind la " + str((SERVER_IP, PORT)))

        self.server_socket.listen(CONCURENT_CONNECTIONS)

    def accept_connection(self):
        conn, addr = self.server_socket.accept()
        return (conn, addr)

    def receive_message(self, conn) -> str:
        return conn.recv(1024).decode()

    def close_socket(self):
        if self.server_socket is not None:
            self.server_socket.close()


import socket

class Server:

    def __init__(self, SERVER_IP, PORT, CONCURENT_CONNECTIONS=1):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((SERVER_IP, PORT))
        print("S-a facut bind la " + str((SERVER_IP, PORT)))

        server_socket.listen(CONCURENT_CONNECTIONS)

    def accept_connection():
        conn, addr = server_socket.accept()
        return (conn, addr)

    def receive_message() -> str:
        return conn.recv(1024).decode()

    def close_socket(sock):
        if sock is not None:
            sock.close()


import socket
import threading

HOST = '127.0.0.1'
PORT = 9999
clients = []


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        try:
            message = conn.recv(1024)
            if not message:
                break
            print(f"[{addr[1]}] {message.decode('utf-8')}")
            broadcast(message, conn)
        except OSError:
            break

    if conn in clients:
        clients.remove(conn)
    conn.close()
    print(f"[DISCONNECTED] {addr} disconnected.")


def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(message)
            except OSError:
                client.close()
                if client in clients:
                    clients.remove(client)


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[STARTING] Server is listening on {HOST}:{PORT}...")

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    start_server()
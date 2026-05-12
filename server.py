import socket
import threading

# List to keep track of all connected clients (so we can broadcast)
clients = []


def handle_client(client_socket, address):
    """
    This function runs inside a SEPARATE thread for every user.
    It handles receiving messages from one user and sending them to everyone else.
    """
    print(f"[NEW CONNECTION] {address} connected.")

    connected = True
    while connected:
        try:
            # Receive message from this specific client
            message = client_socket.recv(1024).decode('utf-8')

            if message:
                print(f"[{address}] {message}")
                # BROADCAST: Send this message to every other connected client
                broadcast(message, client_socket)
            else:
                # If message is empty, the client likely disconnected
                connected = False
        except:
            # Handle errors (like the client force-closing the app)
            connected = False

    # Cleanup when the client leaves
    clients.remove(client_socket)
    client_socket.close()
    print(f"[DISCONNECTED] {address} disconnected.")


def broadcast(message, sender_socket):
    """Sends a message to everyone except the person who sent it."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5050))
    server.listen()
    print("[STARTING] Server is listening...")

    while True:
        # This line BLOCKS and waits for a new user
        conn, addr = server.accept()

        # Add the new connection to our list
        clients.append(conn)

        # CREATE A NEW THREAD:
        # target=handle_client is the function to run
        # args=(conn, addr) are the variables to pass to that function
        thread = threading.Thread(target=handle_client, args=(conn, addr))

        # Start the thread (This is an OS-level call to the CPU scheduler)
        thread.start()

        # Show how many active threads (users) we have
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    start_server()
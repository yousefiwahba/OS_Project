import socket
import threading

# 1. Connect to the Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5050))


def receive_messages():
    """
    This function runs continuously on a BACKGROUND thread.
    Its only job is to wait for the server to send data and print it.
    """
    while True:
        try:
            # This is a BLOCKING call, but because it's on a background thread,
            # it doesn't freeze the rest of the program!
            message = client.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                print("Disconnected from server.")
                client.close()
                break
        except:
            print("An error occurred or connection was closed.")
            client.close()
            break


def write_messages():
    """
    This function runs on the MAIN thread.
    Its only job is to wait for you to type something and send it.
    """
    while True:
        # Wait for user input
        message = input("")

        if message.lower() == 'quit':
            client.close()
            break

        # Send the message to the server
        client.send(message.encode('utf-8'))


# 2. Start the listening thread
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# 3. Start the writing loop (runs on the main thread)
write_messages()
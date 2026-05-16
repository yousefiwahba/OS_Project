import socket
import threading


class NetworkClient:
    def __init__(self, host='127.0.0.1', port=9999, on_receive_callback=None):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.on_receive_callback = on_receive_callback
        self.username = "Unknown"

    def connect(self, username):
        """Saves the username, connects to the server, and starts listening."""
        self.username = username
        try:
            self.client_socket.connect((self.host, self.port))
            listener = threading.Thread(target=self._receive_messages, daemon=True)
            listener.start()
            return True
        except ConnectionRefusedError:
            return False

    def _receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode("utf-8")
                if not data:
                    break

                # PROTOCOL PARSING: Split the string at the FIRST '|' symbol
                if "|" in data:
                    sender_name, actual_message = data.split("|", 1)
                    if self.on_receive_callback:
                        self.on_receive_callback(sender_name, actual_message)
                else:
                    # Fallback if a message doesn't have a | symbol
                    if self.on_receive_callback:
                        self.on_receive_callback("System", data)
            except OSError:
                break

    def send_message(self, text):
        try:
            # PROTOCOL FORMATTING: Glue the username and message together
            formatted_message = f"{self.username}|{text}"
            self.client_socket.send(formatted_message.encode("utf-8"))
        except OSError:
            pass

    def disconnect(self):
        try:
            self.client_socket.shutdown(socket.SHUT_RDWR)
            self.client_socket.close()
        except OSError:
            pass
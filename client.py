import socket
import threading


class NetworkClient:
    def __init__(self, host='127.0.0.1', port=9999, on_receive_callback=None):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # This is a function passed from the UI to trigger when a message arrives
        self.on_receive_callback = on_receive_callback

    def connect(self):
        """Attempts to connect to the server and starts the listening thread."""
        try:
            self.client_socket.connect((self.host, self.port))
            # Start background thread for listening
            listener = threading.Thread(target=self._receive_messages, daemon=True)
            listener.start()
            return True
        except ConnectionRefusedError:
            return False

    def _receive_messages(self):
        """Constantly listens for data from the server."""
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break

                # If we get a message, send it to the UI using the callback function
                if self.on_receive_callback:
                    self.on_receive_callback(data.decode("utf-8"))
            except OSError:
                break

    def send_message(self, text):
        """Pushes data to the server."""
        try:
            self.client_socket.send(text.encode("utf-8"))
        except OSError:
            pass

    def disconnect(self):
        """Safely closes the OS socket."""
        try:
            self.client_socket.shutdown(socket.SHUT_RDWR)
            self.client_socket.close()
        except OSError:
            pass
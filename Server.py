import socket
import threading
import pickle

class FileServer:
    def __init__(self, port=5106):
        # Initialize server settings
        self.port = port
        self.server_socket = None
        self.running = True

    def start_server(self):
        # Create and start the server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('', self.port))
        self.server_socket.listen(5)
        print("Server listening for connections...")

        while self.running:
            # Accept client connections
            client_socket, address = self.server_socket.accept()
            print(f"Accepted connection from {address}")
            # Handle each client in a separate thread
            threading.Thread(target=self.process_client, args=(client_socket,)).start()

    def process_client(self, client_socket):
        # Create file streams for data transmission
        output = client_socket.makefile('wb')
        input = client_socket.makefile('rb')

        try:
            while True:
                # Receive commands and file name from client
                action, file_name = pickle.load(input)
                if action == "upload":
                    self.store_file(file_name, input, output)
                elif action == "download":
                    self.retrieve_file(file_name, output)
        except EOFError:
            print("Client has disconnected.")
        finally:
            # Close all resources properly
            input.close()
            output.close()
            client_socket.close()

    def store_file(self, file_name, input_stream, output_stream):
        # Store uploaded file
        saved_file_name = f"uploaded_{file_name}"
        try:
            with open(saved_file_name, 'wb') as file:
                while True:
                    data = pickle.load(input_stream)
                    if data == b'END':
                        break
                    file.write(data)
            print(f"File received and saved as {saved_file_name}.")
        except Exception as error:
            print(f"Error receiving file: {error}")

    def retrieve_file(self, file_name, output_stream):
        # Send file to client
        try:
            with open(file_name, 'rb') as file:
                while chunk := file.read(1024):
                    pickle.dump(chunk, output_stream)
                    output_stream.flush()
            pickle.dump(b'END', output_stream)
            output_stream.flush()
            print(f"File {file_name} sent successfully.")
        except Exception as error:
            print(f"Error sending file: {error}")

    def shutdown_server(self):
        # Shutdown the server
        self.running = False
        self.server_socket.close()
        print("Server shutting down.")

def control_server(server):
    # Control server shutdown through user input
    input("Press Enter to stop the server...")
    server.shutdown_server()

if __name__ == "__main__":
    my_server = FileServer()
    # Run server control in a separate thread
    threading.Thread(target=control_server, args=(my_server,)).start()
    my_server.start_server()

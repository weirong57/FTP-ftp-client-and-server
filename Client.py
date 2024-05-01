import socket
import pickle

class FileClient:
    def __init__(self):
        # Initialize socket and file streams
        self.socket = None
        self.output_stream = None
        self.input_stream = None

    def start(self):
        # Start the client and connect to server
        server_port = int(input("Enter port to connect: (e.g., 5106) "))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', server_port))
        print(f"Connected on port {server_port}")

        # Create file streams for data transmission
        
        self.output_stream = self.socket.makefile('wb')
        self.input_stream = self.socket.makefile('rb')

        try:
            self.handle_commands()
        finally:

            # Ensure resources are closed properly
            self.close_resources()

    def handle_commands(self):
        # Handle user commands for upload, download, or exit
        while True:
            action = input("Do you want to 'upload' or 'download' a file, or 'exit'? ")
            if action.lower() == "exit":
                print("Exiting...")
                break
            file_name = input("Enter file name: ")
            # Send command and file name to server
            
            pickle.dump((action, file_name), self.output_stream)
            self.output_stream.flush()

            if action == "upload":
                self.upload_file(file_name)
            elif action == "download":
                self.download_file(file_name)

    def upload_file(self, file_name):

        # Upload file to server
        try:
            with open(file_name, 'rb') as file:
                while chunk := file.read(1024):
                    pickle.dump(chunk, self.output_stream)
                    self.output_stream.flush()

                    # Indicate end of file transmission
            pickle.dump(b'END', self.output_stream)
            self.output_stream.flush()
            print("File uploaded successfully.")
        except Exception as e:
            print(f"Upload failed: {e}")

    def download_file(self, file_name):

        # Download file from server
        target_file = f"new_{file_name}"
        try:
            with open(target_file, 'wb') as file:
                while True:
                    data = pickle.load(self.input_stream)
                    if data == b'END':
                        break
                    file.write(data)
            print(f"File downloaded and saved as: {target_file}")
        except Exception as e:
            print(f"Download failed: {e}")

    def close_resources(self):

        # Close all resources properly
        if self.input_stream: self.input_stream.close()
        if self.output_stream: self.output_stream.close()
        if self.socket: self.socket.close()
        print("Disconnected.")

if __name__ == "__main__":
    fc = FileClient()
    fc.start()

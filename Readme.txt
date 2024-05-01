To update the readme for your server-client file transfer system described in `Server.py` and `Client.py`, you'll want it to be clear and informative about how to run and use the programs. Here's a suggestion on how you can structure the readme:

---

# File Transfer System

This system allows users to transfer files between a server and a client over a specified port. The server must be started before the client. Both scripts are written in Python and can be executed from a command prompt.

## Getting Started

### Prerequisites

Ensure that you have Python installed on your system. These scripts were tested with Python 3.x.

### Running the Server

1. Navigate to the project directory in the command prompt.
2. Run the server script by entering the following command:

   ```shell
   python Server.py
   ```

3. The server will wait for a connection from a client. Once connected, it will process file upload and download requests from the client.

### Running the Client

1. Navigate to the project directory in the command prompt.
2. Start the client script by entering the following command:

   ```shell
   python Client.py
   ```

3. When prompted, input the port number `5106` to connect to the server. Other numbers will cause a connection failure. To use a different port, modify `Server.java` to change the port number.

## Operations

Once connected, the client can perform the following operations:

- **Upload**: Send a file to the server.
- **Download**: Receive a file from the server.
- **Exit**: Close the connection.

Follow the on-screen prompts to upload or download files. For uploads, the server saves received files with a new name to avoid overwriting existing files. For downloads, ensure the file name provided exists on the server.

## Example Usage

- Start the server:
  ```shell
  \project2> python Server.py
  Press Enter to exit...
  Waiting for connection
  ```
  
- Connect with the client and perform operations:
  ```shell
  \project2> python Client.py
  Please input the port you want to connect: (eg: 5106) 5106
  Connected to localhost in port 5106
  ```

Follow the prompts to upload or download files as needed. Exit when done.
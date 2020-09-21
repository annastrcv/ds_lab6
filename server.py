import socketserver
import socket
import os


# receive 4096 bytes each time
BUFFER_SIZE = 4096

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        filenamesize = int.from_bytes(self.request.recv(2), 'big')
        filename = self.request.recv(filenamesize)
        filesize = self.request.recv(4)
        print(filename)
        print(filesize)
        print(filenamesize)

        filename = filename.decode('utf-8')
        filename = os.path.basename(filename)

        with open(filename, "wb") as f:
            while(True):
                # read 1024 bytes from the socket (receive)
                bytes_read = self.request.recv(BUFFER_SIZE)
                if not bytes_read:
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)



if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

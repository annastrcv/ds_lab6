import socket
import sys
import os

BUFFER_SIZE = 4096  # send 4096 bytes each time step

filename = "".join(sys.argv[1])
server_address = "".join(sys.argv[2])
server_port = "".join(sys.argv[3])

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((server_address, int(server_port)))
    # sock.sendall(bytes(filename + "\n", "utf-8"))

    filesize = os.path.getsize(filename)
    filenamesize = len(filename)

    sock.send(filenamesize.to_bytes(2, byteorder='big'))
    sock.send(f"{filename}".encode())
    sock.send(filesize.to_bytes(4, byteorder='big'))

    sent = 0

    with open(filename, "rb") as f:
        while (True):
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in
            # busy networks
            sock.sendall(bytes_read)
            # update the progress bar
            sent += len(bytes_read)
            print("\rProgress:{}%".format(100 * sent / filesize), end='')

print("File that was sent:     {}".format(filename))

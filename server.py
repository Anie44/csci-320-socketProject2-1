import socket
import os
import sys

IP = '127.0.0.1'  # default IP address of the server
PORT = 12000  # change to a desired port number
BUFFER_SIZE = 1024  # change to a desired buffer size


def get_file_info(data: bytes) -> (str, int):
    return data[8:].decode(), int.from_bytes(data[:8], byteorder='big')


def upload_file(conn_socket: socket, file_name: str, file_size: int):
    # create a new file to store the received data
    file_name += '.temp'
    # please do not change the above line!
    with open(file_name, 'wb') as file:
        retrieved_size = 0
        try:
            while retrieved_size < file_size:
                chunk, address = conn_socket.recvfrom(BUFFER_SIZE)
                file.write(chunk)
                retrieved_size += chunk
                conn_socket.sendto(b'received', address)
        except OSError as oe:
            print(oe)
            os.remove(file_name)


def start_server(ip, port):
    # create a TCP socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(1)
    print(f'Server ready and listening on {ip}:{port}')

    try:
        while True:
            (conn_socket, addr) = server_socket.accept()
            # TODO: section 1 step 2
            # expecting an 8-byte byte string for file size followed by file name
            info, address = server_socket.recvfrom(BUFFER_SIZE)
            file_name, file_size = get_file_info(info)
            print(f'Received: {file_name} with size = {file_size}')
            server_socket.sendto(b'go ahead', address)
            upload_file(conn_socket, file_name, file_size)
            conn_socket.close()
    except KeyboardInterrupt as ki:
        pass
    finally:
        server_socket.close()


if __name__ == '__main__':
    # get IP address from cmd line
    if len(sys.argv) == 2:
        IP = sys.argv[1]  # IP from cmdline argument

    start_server(IP, PORT)

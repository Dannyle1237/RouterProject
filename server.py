import socket
def createSocket(ip, port):
    # create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # bind the socket to a specific address and port
    server_address = (ip, port)
    sock.bind(server_address)

    # wait for incoming data
    while True:
        data, client_address = sock.recvfrom(4096)

        # process the data
        print(f"Received {len(data)} bytes from {client_address}: {data.decode()}")

        # send a response back to the client
        message = "Hello, client!"
        sock.sendto(message.encode(), client_address)
import socket
import threading
import requests

#bind_ip = '192.168.1.101'
bind_ip = '127.0.0.1'
bind_port = 5005

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

# print('Listening on {}:{}'.format(bind_ip, bind_port))
print('Listening on {', bind_ip, '}:{', bind_port, '}')


def handle_client_connection(client_socket):
    request = client_socket.recv(4096)
    print('Received {', request, '}')
    requests.post("http://"+bind_ip+":1234/rfidData", data={'rfid': request})
    # request should be b'\x5500529BD24E\r'  where 5500529BD24E is the rfid
    client_socket.send('ACK!'.encode('UTF-8'))
    client_socket.close()


while True:
    client_sock, address = server.accept()
    print('Accepted connection from {', address[0], '}:{', address[1], '}')
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)
        # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    )
    client_handler.start()

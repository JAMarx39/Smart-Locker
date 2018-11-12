import socket

# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
# client.connect((target, port))
client.connect(('127.0.0.1', 5005))

# send some data
client.send(b'\x5500529BD24E\r')

# receive the response data (4096 is recommended buffer size)
response = client.recv(4096)

print(response.decode('UTF-8'))
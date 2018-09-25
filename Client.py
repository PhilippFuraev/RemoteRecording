import socket

sock = socket.socket()
#sock.connect(('192.168.137.167', 9090))
sock.connect(('localhost', 9090))
connection=True
while connection:
    message = input()
    byteMessage = bytes(message, 'utf-8')
    if message=="close":
        sock.send(byteMessage)
        sock.close()
        connection=False
    if connection:
        sock.send(byteMessage)
        data = sock.recv(1024)
        serverMessage=data.decode()
        if (serverMessage[0:9]=='packages:'):
            numOfPackages = int(serverMessage[9:len(serverMessage)])
            print("downoloading speech...")
            f = open('test.flac', 'wb')
            for num in range (0, numOfPackages):
                fileBinary = sock.recv(1024)
                f.write(fileBinary)
            f.close()
            print("Done")
sock.close()
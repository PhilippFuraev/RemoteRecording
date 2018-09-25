import socket
from RecordingThread import RecordingThread
from RecordingThread import wavToFlac
import time
import os
sock = socket.socket()
sock.bind(('', 9090))
while True:
    sock.listen(1)
    conn, addr = sock.accept()

    print('connected:', addr)
    recordingThread = RecordingThread()
    connection=True
    while connection:
        data = conn.recv(1024)
        if data:
            message = data.decode()
            if message=="start":
                recordingThread.start()
                conn.send(data)
                print("start the record")
            if message=="stop":
                recordingThread.stop()
                recordingThread.join()
                wavToFlac()
                size = os.path.getsize("dialog.flac")
                numOfPackages = round(size/1024 + 0.5)
                conn.send(bytes("packages:" + numOfPackages.__str__(), 'utf-8'))
                print("stop the record")
                print("sending flac...")
                size = os.path.getsize("dialog.flac")
                numOfPackages = round(size/1024 + 0.5)
                print("number of packages:" + numOfPackages.__str__())
                f = open('dialog.flac', 'rb')
                byteFile = f.read(1024)
                while (byteFile):
                    conn.send(byteFile)
                    byteFile = f.read(1024)
                f.close()
                print("done sending")
                time.sleep(1)
                conn.send(bytes("done", 'utf-8'))
                #connection=False
            if message=="close":
                print("Closing the connection...")
                conn.close()
                print("Connection closed")
                connection=False
            #if connection:
            #    conn.send(data)
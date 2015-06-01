import sys
import socket

def main():

    ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssocket.bind(('', 80))
    print ssocket.getsockname()
    ssocket.listen(5)

    while 1:
        (csocket, caddr) = ssocket.accept()
        print caddr
        message = csocket.recv(1024)
        print message

if __name__ == '__main__':
	main()

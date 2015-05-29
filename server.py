import sys
import socket

def main():
	#if len(sys.argv) < 2:
	#	print 'Enter the IP address for the server.'
	#	exit()

	#ip_addr = sys.argv[1]

	ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ssocket.bind(('', 80))
	ssocket.listen(5)

	while 1:
		(csocket, caddr) = ssocket.accept()
		print caddr

if __name__ == '__main__':
	main()

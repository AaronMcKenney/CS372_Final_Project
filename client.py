import sys
import socket

def main():
	if len(sys.argv) < 2:
		print 'Enter the IP address for the server.'
		exit()

	saddr = sys.argv[1]
	csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	csocket.connect((saddr, 80))

if __name__ == '__main__':
	main()

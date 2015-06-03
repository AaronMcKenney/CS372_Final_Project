import sys
import socket
import string

from message import *

def enterLobby(csocket, msg):
	if msg == lobbyMsg.connected:
		lobbyRes = "N"
		while(lobbyRes != "Y" and lobbyRes != "y"):
			lobbyRes = raw_input("Ready to begin? (Y/N) ")
		csocket.send(lobbyMsg.ready)

	elif msg == lobbyMsg.waitOnOthers:
		print("Waiting on others...")

	elif msg == lobbyMsg.beginGame:
		print("Let the game begin!")

def main():
	if len(sys.argv) < 2:
		print('Enter the IP address for the server.')
		exit()

	saddr = sys.argv[1]
	csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	csocket.connect((saddr, 80))

	while(1):
		msg = csocket.recv(1024)
		if msg == 0:
			print "Didn't receive data from the server!"
			exit()

		if msg[0:headerLen] == lobbyMsg.head:
			enterLobby(csocket, msg)

if __name__ == '__main__':
	main()

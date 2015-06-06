import sys
import socket
import string

from message import *

def enterLobby(csocket, msg):
	if msg == LobbyMsg.connect:
		lobbyRes = "N"
		while(lobbyRes != "Y" and lobbyRes != "y"):
			lobbyRes = raw_input("Ready to begin? (Y/N) ")
		csocket.sendall(LobbyMsg.ready)

	elif msg == LobbyMsg.waitOnOthers:
		print("Waiting on others...")

	elif msg == LobbyMsg.beginGame:
		print("Let the game begin!")

def printStats(csocket, msg):
	print msg

	csocket.sendall(StatsMsg.ack)
	print 'Sent Ack!'

def main():
	if len(sys.argv) < 3:
		print('Enter your name and the IP address for the server.')
		exit()

	cname = sys.argv[1]
	saddr = sys.argv[2]
	csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	csocket.connect((saddr, 80))

	try:
		csocket.sendall(NameMsg.head + cname)
		while(1):
			try:
				msg = csocket.recv(1024)
				if msg == '':
					raise socket.error
			except socket.error as e:
				print("Didn't receive data from the server!")
				exit()

			if msg[0:headerLen] == LobbyMsg.head:
				enterLobby(csocket, msg)

			if msg[0:headerLen] == StatsMsg.head:
				printStats(csocket, msg[3:])

	finally:
			csocket.close()

if __name__ == '__main__':
	main()

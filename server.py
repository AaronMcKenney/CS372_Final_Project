import sys
import socket
import thread
import threading
import json
from random import shuffle

from message import *
from player import *

#Global vars
numConnections = 0
numReady = 0
everyoneReady = threading.Condition()
connections = []

#mode that the game is in and potential values (enum) for mode
lobby = 0
betweenCombat = 1
inCombat = 2

mode = lobby

def serverThread(ssocket):
	global numConnections, connections

	while 1:
		(csocket, caddr) = ssocket.accept()
		#Upon connection, get the client's name
		try:
			msg = csocket.recv(1024)
			if msg == '' or msg[0:headerLen] != NameMsg.head:
				raise socket.error
		except socket.error as e:
			csocket.close()
			return
		cname = msg[headerLen:]

		numConnections += 1
		if mode == lobby:
			#We are in the lobby
			connections.append((csocket, caddr, cname))
			print("New connection: " + cname + " at " + caddr[0])
			csocket.sendall(LobbyMsg.connect)
			thread.start_new_thread(clientThread, (csocket, caddr, cname))

def clientThread(csocket, caddr, cname):
	global numConnections, numReady, everyoneReady

	isReady = False

	#Recieve client messages
	try:
		msg = csocket.recv(1024)
		if msg == '':
			raise socket.error
	except socket.error as e:
		csocket.close()
		numConnections -= 1
		connections.pop(connections.index((csocket, caddr)))
		if isReady == True:
			numReady -= 1
		print caddr[0] + ' closed!'
		return

	#Client ready to begin
	if msg == LobbyMsg.ready:
		if isReady != True:
			numReady += 1
			isReady = True
			print(cname + " is ready!")

		if numReady == numConnections:
			#Notify main thread to start game
			everyoneReady.acquire()
			everyoneReady.notifyAll()
			everyoneReady.release()
		else:
			csocket.sendall(LobbyMsg.waitOnOthers)

	elif msg == LobbyMsg.notReady:
		if isReady != False:
			numReady -= 1
			isReady = False
			print(caddr[0] + " is not ready!")


def createPlayers():
	global connections

	charInfo = []
	charFile = open('characters.json', 'r')
	characters = json.load(charFile)
	characters = characters["Characters"]
	#print characters["Characters"][0]["Name"]
	shuffle(characters)

	plist = []

	for i, (csocket, caddr, cname) in enumerate(connections):
		plist.append(Player(csocket, caddr, cname, characters[i]))

	return plist

def main():
	global everyoneReady, mode

	ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		ssocket.bind(('', 80))
	except socket.error as msg:
		print("Bind failed. Error code: " + str(msg[0]))
		quit()

	ssocket.listen(5)
	print("Server ready")

	thread.start_new_thread(serverThread, (ssocket,))

	#If everyone is ready, start the game
	everyoneReady.acquire()
	while(numReady != numConnections or numConnections == 0):
		#Don't start the game until all players in lobby are ready
		everyoneReady.wait()
	everyoneReady.release()

	for client in connections:
		client[0].sendall(LobbyMsg.beginGame)
		mode = betweenCombat

	print("Ready set go!")
	players = createPlayers()
	for player in players:
		player.sendPartyStats(players)

if __name__ == '__main__':
	main()

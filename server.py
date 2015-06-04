import sys
import socket
import thread
import threading

from message import *

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
		numConnections += 1
		if mode == lobby:
			#We are in the lobby
			connections.append((csocket, caddr))
			print("New connection: " + caddr[0])
			csocket.send(lobbyMsg.connected)
			thread.start_new_thread(clientThread, (csocket, caddr))

def clientThread(csocket, caddr):
	global numConnections, numReady, everyoneReady

	isReady = False

	#Recieve client messages
	while 1:
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
		if msg == lobbyMsg.ready:
			if isReady != True:
				numReady += 1
				isReady = True
				print(caddr[0] + " is ready!")

			if numReady == numConnections:
				#Notify main thread to start game
				everyoneReady.acquire()
				everyoneReady.notifyAll()
				everyoneReady.release()
			else:
				csocket.send(lobbyMsg.waitOnOthers)

		elif msg == lobbyMsg.notReady:
			if isReady != False:
				numReady -= 1
				isReady = False
				print(caddr[0] + " is not ready!")


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
		client[0].send(lobbyMsg.beginGame)
		mode = betweenCombat

	print("Ready set go!")
	quit()

if __name__ == '__main__':
	main()

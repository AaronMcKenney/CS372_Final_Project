import socket

from character import *
from message import *

class Player:

	def __init__(self, psocket, paddr, pname, charinfo):
		self.sock = psocket
		self.addr = paddr
		self.name = pname
		self.character = Character(charinfo['Name'], charinfo['Description'], charinfo['Health'], charinfo['Mana'])

	def __del__(self):
		self.sock.close()

	#Two players are equal if all of their attributes match
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.__dict__ == other.__dict__
		else:
			return False
	def __ne__(self, other):
		return not self.__eq__(other)

	def send(self, data):
		self.sock.sendall(data)

	def recv(self):
		try:
			msg = self.sock.recv(1024)
			if msg == '':
				raise socket.error
			return msg
		except socket.error:
			self.sock.close()
			return ''

	def getStats(self):
		return "Player name: " + self.name + "\n" + self.character.getStats()

	def sendPartyStats(self, plist):
		ownStats = 'You:\n'
		otherPlayerStats = '\nYour Party:\n'

		for player in plist:
			if self.__eq__(player):
				ownStats += player.getStats()
			else:
				otherPlayerStats += player.getStats()

		#List your own stats first, and then list everyone elses
		self.send(StatsMsg.party + ownStats + otherPlayerStats)
		if self.recv() != StatsMsg.ack:
			print self.name + ' did not receive party stats'

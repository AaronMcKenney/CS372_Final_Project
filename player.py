import socket

from character import *
from message import *

class Player(object):

	def __init__(self, psocket, paddr, pname, charinfo):
		self.sock = psocket
		self.addr = paddr
		self.name = pname
		self.character = Character(charinfo['Name'], charinfo['Description'], charinfo['Health'], charinfo['Mana'], charinfo['Attacks'])

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

	def getName(self):
		return self.name
			
	def getStats(self):
		return "Player name: " + self.name + "\n" + self.character.getStats()

	def getAttacks(self):
		return self.character.getAttacks()
		
	def getNumAttacks(self):
		return self.character.getNumAttacks()

	def sendPartyStats(self, plist):
		ownStats = 'You:\n'
		if len(plist) != 1:
			otherPlayerStats = '\nYour Party:\n'
		else:
			otherPlayerStats = ''
			
		for player in plist:
			if self.__eq__(player):
				ownStats += player.getStats()
				ownStats += player.getAttacks()
			else:
				otherPlayerStats += player.getStats()
				otherPlayerStats += player.getAttacks()

		#List your own stats first, and then list everyone elses
		self.send(StatsMsg.party + ownStats + otherPlayerStats)
		if self.recv() != StatsMsg.ack:
			print self.name + ' did not receive party stats'

	def isConnected(self):
		self.send(ConnMsg.ping)
		if self.recv() != ConnMsg.pong:
			print self.name + ' disconnected!'
			return False
		return True
		
	def isAlive(self):
		return self.character.isAlive()
	
	def getLegalAttack(self, attackStr):
		#Takes in a client's chosen attack and ensures
		#that they picked a legal move
		#Returns -1 if bad/illegal, or index in attack list
		if len(attackStr) > optionLen + 1:
			return -1
		option = attackStr[0:optionLen]
		if option != AttackMsg.num:
			return -1
		try:
			attack = int(attackStr[optionLen:])
		except ValueError:
			return -1
		
		if attack < 1 or attack > self.character.getNumAttacks():
			return -1
		return attack
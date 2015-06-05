from character import *


class Player:

	def __init__(self, psocket, paddr, pname, charinfo):
		self.sock = psocket
		self.addr = paddr
		self.name = pname
		self.character = Character("Red Eye", 50, 50)

	#def sendPartyStats(self, plist):

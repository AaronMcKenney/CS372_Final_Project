class Character(object):

	def __init__(self, cname, cdesc, chealth, cmana, cattacks):
		self.name = cname
		self.description = cdesc
		self.maxHealth = chealth
		self.health = chealth
		self.maxMana = cmana
		self.mana = cmana
		self.attacks = cattacks

	def getStats(self):
		statsOut = 'Character name: ' + self.name + '\n'
		statsOut += '\tDescription: ' + self.description + '\n'
		statsOut += '\tHP: ' + str(self.health) + '/' + str(self.maxHealth) + '\n'
		statsOut += '\tMP: ' + str(self.mana) + '/' + str(self.maxMana) + '\n'

		return statsOut

	def getAttacks(self):
		attacksOut = '\tAttacks: \n'
		count = 0
		for attack in self.attacks:
			count += 1
			attacksOut += '\t\t' + str(count) + ". " + attack['Name'] + ": " + str(attack['Damage']) + '\n'
		
		return attacksOut
		
	def getNumAttacks(self):
		attacksOut = 0
		for attack in self.attacks:
			attacksOut += 1
		
		return attacksOut

	def isAlive(self):
		if self.health > 0:
			return True
		return False
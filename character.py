class Character:

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
		for attack in self.attacks:
			attacksOut += '\t\t' + attack['Name'] + ": " + str(attack['Damage']) + '\n'
		
		return attacksOut


class Monster(object):

	def __init__(self, mname, mdesc, mhealth, mattacks):
		self.name = mname
		self.description = mdesc
		self.maxHealth = mhealth
		self.health = mhealth
		self.attacks = mattacks

	def getStats(self):
		statsOut = 'Monster name: ' + self.name + '\n'
		statsOut += '\tDescription: ' + self.description + '\n'
		statsOut += '\tHP: ' + str(self.health) + '/' + str(self.maxHealth) + '\n'

		return statsOut

	def getAttacks(self):
		attacksOut = '\tAttacks: \n'
		for attack in self.attacks:
			attacksOut += '\t\t' + attack['Name'] + ": " + str(attack['Damage']) + '\n'
		
		return attacksOut
		
	def isAlive(self):
		if self.health > 0:
			return True
		return False


class Character:

	def __init__(self, cname, chealth, cmana):
		self.name = cname
		self.description = ''
		self.maxHealth = chealth
		self.health = chealth
		self.maxMana = cmana
		self.mana = cmana

	def getStats(self):
		statsOut = 'Character name: ' + self.name + '\n'
		statsOut += '\tDescription: ' + self.description + '\n'
		statsOut += '\tHP: ' + str(self.health) + '/' + str(self.maxHealth) + '\n'
		statsOut += '\tMP: ' + str(self.mana) + '/' + str(self.maxMana) + '\n'

		return statsOut

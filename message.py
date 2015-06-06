#Messages must have the same format between the client and server

#Headers must have the same length
#Headers must be unique
headerLen = 1

#Client sends name upon connecting to server
class NameMsg:
	head = 'N'

class LobbyMsg:
	head = 'L'

	#Server related lobby messages
	connect = head + ':C'
	waitOnOthers = head + ':W'
	beginGame = head + ':B'
	#Client related lobby messages
	ready = head + ':Y'
	notReady = head + ':N'

#Server sends stats to clients
#Client requests stats from clients
class StatsMsg:
	head = 'S'

	#Server related stats messages
	self = head + ':Y'
	party = head + ':P'
	enemies = head + ':E'
	#Cliient related stats messages
	ack = head + ':A'

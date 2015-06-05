#Messages must have the same format between the client and server

#Headers must have the same length
#Headers must be unique
headerLen = 1

class LobbyMsg:
	head = 'L'
	#Server related lobby messages
	connect = head + ':C'
	waitOnOthers = head + ':W'
	beginGame = head + ':B'
	#Client related lobby messages
	ready = head + ':Y'
	notReady = head + ':N'

class NameMsg:
	head = 'N'



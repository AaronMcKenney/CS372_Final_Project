import sys
import socket
import thread

#Global vars
numConnections = 0
ready = 0
connections = []

def clientThread(csocket, caddr):
    #Recieve client messages
    while 1:
        message = csocket.recv(1024)

        #Client (proper) disconnect
        if message == "Close":
            csocket.close()

            #Close if all connections lost
            global numConnections
            numConnections -= 1
            if numConnections < 1:
                break

        #Client ready to begin
        if message == "Ready":
            print(caddr[0] + " is ready!")
            global ready
            ready += 1

            #If everyone is ready, start the game
            if(ready == numConnections):
                for client in connections:
                    client[0].send("The game has begun!")


def main():
    ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ssocket.bind(('', 80))
    except socket.error as msg:
        print("Bind failed. Error code: " + str(msg[0]))

    ssocket.listen(5)
    print("Server ready")

    #Accept new connections
    while 1:
        (csocket, caddr) = ssocket.accept()

        #Add new connection to global list
        global connections
        connections.append((csocket, caddr))

        print("New connection: " + caddr[0])
        csocket.send("Connected")

        #Count new client in lounge
        global numConnections
        numConnections += 1

        thread.start_new_thread(clientThread, (csocket,caddr))

if __name__ == '__main__':
	main()

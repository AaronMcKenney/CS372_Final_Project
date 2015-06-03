import sys
import socket
import thread
import threading

#Global vars
numConnections = 0
ready = 0
everyoneReady = threading.Condition()
connections = []
beginGame = 0

def serverThread(ssocket):
    while 1:
        (csocket, caddr) = ssocket.accept()
        global numConnections
        numConnections += 1
        if beginGame == 0:
            #We are in the lobby
            global connections
            connections.append((csocket, caddr))
            print("New connection: " + caddr[0])
            csocket.send("Connected")
            thread.start_new_thread(clientThread, (csocket, caddr))

def clientThread(csocket, caddr):
    #Recieve client messages
    while 1:
        message = csocket.recv(1024)

        #Client disconnect
        if message == "Close" or message == 0:
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

            if ready == numConnections:
                global everyoneReady
                everyoneReady.acquire()
                everyoneReady.notifyAll()
                everyoneReady.release()


def main():
    ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ssocket.bind(('', 80))
    except socket.error as msg:
        print("Bind failed. Error code: " + str(msg[0]))

    ssocket.listen(5)
    print("Server ready")

    thread.start_new_thread(serverThread, (ssocket,))

    #If everyone is ready, start the game
    global everyoneReady
    everyoneReady.acquire()
    while(ready != numConnections or numConnections == 0):
        everyoneReady.wait()
    everyoneReady.release()

    for client in connections:
        client[0].send("The game has begun!")
        global beginGame
        beginGame = 1

    print("Ready set go!")
    quit()

if __name__ == '__main__':
	main()

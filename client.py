import sys
import socket
import string

def main():
    if len(sys.argv) < 2:
        print('Enter the IP address for the server.')
        exit()

    saddr = sys.argv[1]
    csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    csocket.connect((saddr, 80))

    while(1):
        message = csocket.recv(1024)
        print(message)
        break

    #Enter lounge
    if(message == "Connected"):
        response = "N"
        while(response != "Y" and response != "y"):
            response = raw_input("Ready to begin? (Y/N) ")
        csocket.send("Ready")

    while(1):
        message = csocket.recv(1024)
        print(message)
        break

        #Close connection for now
        #csocket.send("Close")
        #exit()

if __name__ == '__main__':
	main()

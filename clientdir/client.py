import socket
import os
import sys
import time

def get_input():
    command = str(input("Enter command:\n"))
    command = command.split(" ")
    command[0] = command[0].upper()
    return command

def list(client, connected):
    if connected == True:
        client.sendall("LIST".encode())
        print("\n" + client.recv(1024).decode() + "\n")
    else:
        print("Client is not connected\n")
        
#def retrieve
        
def store(client, connected, filename):
    if connected == True:
        try:
            filesize = os.path.getsize("./" + filename)
        except:
            print("Error locating file")
            return
            
        client.sendall(("STORE " + filename + " " + str(filesize)).encode())
        file = open(filename, 'rb')
        file_data = file.read(1024)
        client.sendall(file_data)
        file.close()
        
        print("\n" + client.recv(1024).decode() + "\n")
    else:
        print("Client is not connected\n")

def main():
    connected = False

    command = get_input()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while True:
        if command[0] == "CONNECT":
            if connected == False:
                try:
                    client.connect((command[1], int(command[2]))) # (ip, port)
                    print("Connected to host " + command[1] + " at port " + command[2])
                    connected = True
                except:
                    print("Connection error")
                    connected = False
                    print(command)
            else:
                print("Client already connected\n")
        elif command[0] == "LIST":
            list(client, connected)
        #elif command[0] == "RETRIEVE":
        elif command[0] == "STORE":
            store(client, connected, command[1])
        elif command[0] == "QUIT":
            if connected == True:
                client.sendall("QUIT".encode())
                client.close()
            print("Terminating connection ...\n")
            break  
        else:
            print("Valid commands are CONNECT, LIST, RETRIEVE, STORE, QUIT")
             #TODO nicer output for commands? use a dictionary?
             #TODO make sure correct number of parameters for each command
        
        command = get_input()
    

if __name__ == "__main__":
    main()

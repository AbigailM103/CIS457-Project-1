import socket
import os

# An FTP client program.
# Authors: Amela Aganovic, Abigail McDonald
# Version: Winter 2021

def get_input():
    command = str(input("Enter command:\n"))
    command = command.split(" ")
    command[0] = command[0].upper()
    return command

def main():
    command_list = ["CONNECT 127.0.0.1 4444: connect to the server",
    "LIST: display all files on server", 
    "RETRIEVE <filename>: retrieve the file named <filename> from the server",
    "STORE <filename>: store the file named <filename> on the server",
    "QUIT: terminate connection and shut down server"]
    
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
                    print("Connection error\n")
                    connected = False
                    print(command)
            else:
                print("Client already connected\n")
        elif command[0] == "LIST":
            list_files(client, connected)
        elif command[0] == "RETRIEVE" and len(command) > 1:
            retrieve(client, connected, command[1])
        elif command[0] == "STORE" and len(command) > 1:
            store(client, connected, command[1])
        elif command[0] == "QUIT":
            if connected == True:
                client.sendall("QUIT".encode())
                client.close()
            print("Terminating connection ...\n")
            break  
        else:
            print("VALID COMMANDS\n")
            print("--------------\n")
            for command in command_list:
                print(command + "\n")
        
        command = get_input()
        
def list_files(client, connected):
    if connected == True:
        client.sendall("LIST".encode())
        print("\n" + client.recv(1024).decode() + "\n")
    else:
        print("Client is not connected\n")
        
def retrieve(client, connected, filename):
    if connected == True:
        try:
            client.sendall(("RETRIEVE " + filename).encode())
            filesize = client.recv(1024).decode()
        
            file_data = client.recv(int(filesize), socket.MSG_WAITALL)
            file = open(filename, "wb")
            file.write(file_data)
            file.close()
            print("Client retrieved file: " + filename + "\n")
        except:
            print("Error retrieving file\n")
    else:
        print("Client is not connected\n")
        
def store(client, connected, filename):
    if connected == True:
        if os.path.isfile("./" + filename):
            filesize = os.path.getsize("./" + filename)
            client.sendall(("STORE " + filename + " " + str(filesize)).encode())
            file = open(filename, 'rb')
            file_data = file.read(1024)
            client.sendall(file_data)
            file.close()
            print("\n" + client.recv(1024).decode() + "\n")
        else:
            print("Error locating file\n")
    else:
        print("Client is not connected\n")

if __name__ == "__main__":
    main()

import socket
import os
    
def list_files(client):
    try:
        directory = os.getcwd()
        files = os.listdir(directory)
        files_list = "\n".join(files)
        client.sendall(files_list.encode())
    except:
        print("Error listing files\n")
        client.sendall("Error listing files".encode())
        
def retrieve(client, filename):
    try:
        filesize = os.path.getsize("./" + filename)
    except:
        print("Error locating file\n")
        client.sendall("File not found\n".encode())
        return
        
    client.sendall(str(filesize).encode())
    file = open(filename, 'rb')
    file_data = file.read(1024)
    client.sendall(file_data)
    file.close()

def store(client, filename, filesize):
    try:
        file = open(filename, "wb")
        file_data = client.recv(int(filesize), socket.MSG_WAITALL)
        file.write(file_data)
        file.close()
        client.sendall("Server stored file".encode())
        print("Server stored file: " + filename + "\n")
    except:
        print("Error storing file\n")
        client.sendall("Error storing file".encode())
    
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    ip = "127.0.0.1"
    port = 4444
    
    server.bind((ip, port))
    server.listen()
    print("Server is active\n")
    client, address = server.accept()
    
    while True:
        print(f"Connected: {address[0]}:{address[1]}")
        
        request = client.recv(1024).decode()
        
        request = request.split(" ")
        request[0] = request[0].upper()
    
        print("Request from client is " + str(request[0]))
        
        if request[0] == "LIST":
            list_files(client)
        elif request[0] == "RETRIEVE":
            print("Retrieve request is " + str(request[0]) + " " + str(request[1]))
            retrieve(client, request[1]);
        elif request[0] == "STORE":
            print("Store request is " + str(request[0]) + " " + str(request[1]) + " " + str(request[2]))
            store(client, request[1], request[2])
        elif request[0] == "QUIT":
            print("Shutting down server ...")
            server.close()
            break
            
if __name__ == "__main__":
    main()

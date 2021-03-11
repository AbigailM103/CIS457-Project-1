import socket
import os
    
def list(client):
    try:
        directory = os.getcwd()
        files = os.listdir(directory)
        files_list = "\n".join(files)
        client.sendall(files_list.encode())
    except:
        print("Error listing files\n")
        client.sendall("Error listing files".encode())
        
def store(client, filename, filesize):
    try:
        print("Storing file [" + filename + "] of size [" + filesize + "]\n")
        file = open(filename, "wb")
        file_data = client.recv(int(filesize), socket.MSG_WAITALL)
        file.write(file_data)
        file.close()
        client.sendall("File stored".encode())
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
        #client, address = server.accept()
        print(f"Connected: {address[0]}:{address[1]}")
        
        request = client.recv(1024).decode()
        
        request = request.split(" ")
        request[0] = request[0].upper()
    
        print("Request from client is " + str(request[0]))
        
        if request[0] == "LIST":
            list(client)
        elif request[0] == "STORE":
            print("Store request is " + str(request[0]) + " " + str(request[1]) + " " + str(request[2]))
            store(client, request[1], request[2])
        elif request[0] == "QUIT":
            print("Shutting down server ...")
            server.close()
            break
            
if __name__ == "__main__":
    main()

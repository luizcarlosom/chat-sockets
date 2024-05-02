import socket

HOST = '127.0.0.1'  
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT)) 

    while True:
        message = input("Cliente: ")
        client_socket.sendall(message.encode())
        
        if message == "xau":
            break
        
        data = client_socket.recv(1024)
        
        if not data:
            break
        
        print("Servidor:", data.decode())

print("Conexão encerrada.")
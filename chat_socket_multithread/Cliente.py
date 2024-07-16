import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 8080

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(data.decode())
        except:
            break

def send_files(client_socket, file_path):
    if os.path.isfile(file_path):
        client_socket.sendall(f"FILE:{os.path.basename(file_path)}".encode())
        with open(file_path, 'rb') as file:
            while (chunk := file.read(1024)):
                client_socket.sendall(chunk)
        client_socket.sendall(b"EOF")
        print("Arquivo enviado.")
    else:
        print("Arquivo não encontrado.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))

    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    while True:
        message = input()
        
        if message.startswith("sendfile"):
            file_path = message.split(" ", 1)[1]
            send_files(client_socket, file_path)
        else:
            client_socket.sendall(message.encode())
        
        if message == "xau":
            break

print("Conexão encerrada.")

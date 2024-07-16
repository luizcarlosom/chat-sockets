import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 8080

def handle_client(conn):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            
            if data.decode().startswith("FILE:"):
                file_name = data.decode().split(":", 1)[1]
                with open(file_name, 'wb') as file:
                    while True:
                        file_data = conn.recv(1024)
                        if file_data == b"EOF":
                            break
                        file.write(file_data)
                print(f"Arquivo {file_name} recebido.")
            else:
                print(data.decode())
        except:
            break

    conn.close()
    print("Conexão encerrada com o cliente")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Servidor esperando por conexões...")

    conn, addr = server_socket.accept()
    print(f"Conectado a: {addr}")

    threading.Thread(target=handle_client, args=(conn,)).start()

    while True:
        message = input()
        conn.sendall(message.encode())
        if message == "xau":
            break

    conn.close()
    print("Conexão encerrada.")

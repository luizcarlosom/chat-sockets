import socket

HOST = '127.0.0.1'  
PORT = 8080        

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))  
    server_socket.listen()            

    print("Servidor esperando por conexões...")
    conn, addr = server_socket.accept()
    print("Conectado a:", addr)

    while True:
        data = conn.recv(1024)

        if data.decode() == "xau":
            break
        
        print("Cliente:", data.decode())
        
        message = input("Servidor: ")
        
        if message == "xau":
            break
        
        conn.sendall(message.encode())
        

print("Conexão encerrada.")

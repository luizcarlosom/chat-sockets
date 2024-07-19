import socket
import threading

from colorama import Style, Fore, Back

HOST = '127.0.0.1'
PORT = 8080

def handle_client(conn, client_name):
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
                print(Fore.GREEN + f"Arquivo {file_name} recebido." + Style.RESET_ALL)
            else:
                print(Fore.GREEN + f'{client_name}: {data.decode()}'+ Style.RESET_ALL)
        except:
            break

    conn.close()
    print(Fore.RED + "Conexão encerrada com o cliente" + Style.RESET_ALL)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(Fore.BLUE + "Servidor esperando por conexões..." + Style.RESET_ALL)

    conn, addr = server_socket.accept()
    client_name = conn.recv(1024)
    client_name_decode = client_name.decode()

    print(Fore.YELLOW + f'Você foi conectado com {client_name_decode} no endereço: {addr}' + Style.RESET_ALL)

    threading.Thread(target=handle_client, args=(conn, client_name_decode)).start()

    while True:
        message = input()
        conn.sendall(message.encode())
        if message == "xau":
            break

    conn.close()
    print(Fore.RED + "Conexão encerrada." + Style.RESET_ALL)

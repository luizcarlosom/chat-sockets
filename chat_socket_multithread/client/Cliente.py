import socket
import threading
import os

from colorama import init, Style, Fore

init(autoreset=True)

HOST = '127.0.0.1'
PORT = 8080

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(Fore.GREEN + f'Servidor: {data.decode()}' + Style.RESET_ALL)
        except:
            break

def send_files(client_socket, file_path):
    if os.path.isfile(file_path):
        client_socket.sendall(f"FILE:{os.path.basename(file_path)}".encode())
        with open(file_path, 'rb') as file:
            while (chunk := file.read(1024)):
                client_socket.sendall(chunk)
        client_socket.sendall(b"EOF")
        print(Fore.GREEN + "Arquivo enviado." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Arquivo não encontrado." + Style.RESET_ALL)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_name = input(Fore.BLUE + "Digite seu nome: " + Style.RESET_ALL)

    client_socket.connect((HOST, PORT))
    client_socket.sendall(client_name.encode())

    print(Fore.YELLOW + f'{client_name}, você foi conectado com o servidor!' + Style.RESET_ALL)
    
    information_message = '''
        (= Instruções do Chat =)

        * Para encerrar a comunicação digite 'xau'
        
        * Para enviar um arquivo inicie a mensagem com 'sendfile'. 
            ex: sendfile ../Algoritmo de Dijkstra.pdf
    '''

    print(Fore.YELLOW + information_message + Style.RESET_ALL)

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

print(Fore.RED + "Conexão encerrada." + Style.RESET_ALL)

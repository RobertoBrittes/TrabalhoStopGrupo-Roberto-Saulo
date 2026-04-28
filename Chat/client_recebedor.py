import socket
from time import sleep

HOST = '127.0.0.1'
PORT = 5000

def iniciar_cliente():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((HOST, PORT))
        
        #envia para o servidor qual o seu tipo
        cliente.sendall("TIPO:CONSUMIDOR".encode())
        
        print("="*30)
        print("      BEM-VINDO AO CHAT!      ")
        print("="*30)
        
        #entra em um loop infinito de recebimento de mensagens
        while True:
            #recebe a mensagem e imprime ela
            mensagem = cliente.recv(1024).decode()
            print(mensagem)
            sleep(0.5)
            
if __name__ == "__main__":
    iniciar_cliente()

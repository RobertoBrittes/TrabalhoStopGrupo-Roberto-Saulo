import socket
from time import sleep

# Configurações (Devem ser iguais às do servidor)
HOST = '127.0.0.1' # Se for jogar no mesmo PC. Se for em rede, use o IP do PC onde o servidor está rodando.
PORT = 5000

def iniciar_cliente():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((HOST, PORT))
        
        cliente.sendall("TIPO:CONSUMIDOR".encode())
        
        print("="*30)
        print("      BEM-VINDO AO CHAT!      ")
        print("="*30)
        
        while True:
            mensagem = cliente.recv(1024).decode()
            print(mensagem)
            sleep(0.5)
            
if __name__ == "__main__":
    iniciar_cliente()
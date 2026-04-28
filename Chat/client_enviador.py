import socket
from time import sleep
import os
import subprocess

# Configurações (Devem ser iguais às do servidor)
HOST = '127.0.0.1' # Se for jogar no mesmo PC. Se for em rede, use o IP do PC onde o servidor está rodando.
PORT = 5000


def limpar_terminal():
    comando = "cls" if os.name == "nt" else "clear"
    subprocess.run(comando, shell=True)
    
def iniciar_cliente():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((HOST, PORT))
        
        #envia para o servidor qual o seu tipo
        cliente.sendall("TIPO:PRODUTOR".encode())
        
        print("="*30)
        print("      BEM-VINDO AO CHAT!      ")
        print("="*30)
        
        #armazena o nome do usuario e envia para o servidor
        nome = input("Qual seu nome: ")
        cliente.sendall(nome.encode())
        
        # entra em um loop infinito de envio de mensagens
        while True:
            #recebe a mensagem
            mensagem = input("Mensagem: ")
            #envia a mensagem para o servidor
            cliente.sendall(mensagem.encode())
            sleep(0.5)
            # limpa o terminal
            limpar_terminal()

if __name__ == "__main__":
    iniciar_cliente()
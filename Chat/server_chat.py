import socket
import threading
import random
import string
from time import sleep
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000

# Fila de mensagens
FILA = []

# Semáforo de acesso à fila
SEMAFORO_ACESSO = threading.Semaphore(1) # Apenas 1 thread pode acessar a fila por vez

# Quantidade de itens. Quem insere na fila, incrementa. Quem consome, decrementa.
SEMAFORO_ITENS = threading.Semaphore(0)  # A fila inicia com 0 elementos

clientes_consumidores = []

def produzir(mensagem):
    global FILA
    global SEMAFORO_ACESSO
    global SEMAFORO_ITENS

    # Aguarda acesso ao recurso
    SEMAFORO_ACESSO.acquire()
    # Inclui a mensagem na fila
    FILA.append(mensagem)
    # Libera o acesso ao recurso
    SEMAFORO_ACESSO.release()

    # Informa que há itens na fila.
    SEMAFORO_ITENS.release() 

def consumir():
    global FILA
    global SEMAFORO_ACESSO
    global SEMAFORO_ITENS

    # Aguarda até que existam itens na fila
    SEMAFORO_ITENS.acquire()

    # Aguarda acesso ao recurso
    SEMAFORO_ACESSO.acquire()
    # Verifica se há mensagens na fila
    if FILA:
        # Retira a primeira mensagem da fila
        mensagem = FILA.pop(0)
    # Libera o acesso ao recurso
    SEMAFORO_ACESSO.release()

    # Retorna a mensagem que estava na fila
    return mensagem

def thread_produtora(conn, addr):
    # Inclui mensagens na fila
    nome_usuario = conn.recv(1024).decode()
    if not nome_usuario:
        conn.close()
        return
    
    while True:
        msg_produzida = conn.recv(1024).decode()
        if not msg_produzida: break
        
        agora = datetime.now()
        hora_formatada = agora.strftime("%H:%M:%S")
        msg_final = f"[{nome_usuario} {addr[0]} {hora_formatada}]\n {msg_produzida}\n"
        produzir(msg_final)
        print("Mensagem enviada com sucesso!")
        sleep(1)
    
    conn.close()

def thread_distribuidora():
    global clientes_consumidores
    
    # Retira mensagens da fila
    while True:
        msg_da_fila = consumir()
        for cliente_conn in clientes_consumidores:
            try:
                cliente_conn.sendall(msg_da_fila.encode())
            except (BrokenPipeError, ConnectionResetError):
                clientes_consumidores.remove(cliente_conn)
            

def iniciar_servidor():
    global clientes_consumidores
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        
        print(f"Servidor escutando no IP: {HOST}, PORTA: {PORT}")
        
        # Inicia a thread que faz a distribucao das mensagens da fila para os clientes que recebem mensagens
        threading.Thread(target=thread_distribuidora, daemon=True).start()
        
        while True:
            conn, addr = server.accept()
            print(f"Usuário do IP: {addr[0]} se conectou")
            tipoClient = conn.recv(1024).decode()
            if tipoClient == "TIPO:PRODUTOR":
                print("Client identificado como produtor!")
                thread = threading.Thread(target=thread_produtora, args=(conn, addr))
                thread.start()
            else:
                print("Client identificado como consumidor!")
                clientes_consumidores.append(conn)

if __name__ == "__main__":
    iniciar_servidor()
    
import socket
import threading
from time import sleep

HOST = "0.0.0.0"
PORT = 9002

WAITING_TIME = 3

def atender_cliente(conn, addr):
    print(f"[Server] Nova conexão {addr}", flush=True)

    with conn:
        data = conn.recv(1024)

        mensagem = data.decode("utf-8")
        print(f"[Server] Recebido de {addr}: {mensagem}", flush=True )

        print(f"[Server] Processando mensagem..", flush=True )
        resposta = mensagem.upper()
        sleep(WAITING_TIME)
        
        conn.sendall(resposta.encode("utf-8"))

        print(f"[Server] Respondido para {addr}: {resposta}", flush=True)


    print(f"[Server] Conexão encerrada {addr}", flush=True)


def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        print(f"Servidor ouvindo em {HOST}:{PORT}")
        
        qtd_jogadores = print(input("Quantos jogadores: "))

        conexoes = []

        for i in range(qtd_jogadores):
            conn, addr = server.accept()
            print(f"O usuário {i+1} conectou, com o IP: {addr}")
            conexoes.append(conn)

        print("Conexão completa")
        thread = threading.Thread(
            target=atender_cliente,
            args=(conn, addr),
            daemon=True
        )

        thread.start()

if __name__ == "__main__":
    iniciar_servidor()
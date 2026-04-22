import socket
import threading
import random
import string
from time import sleep

HOST = "0.0.0.0"
PORT = 9002


#LISTA QUE GUARDA O NOME DE CADA JOGADOR
NOMES = []

conexoes = []
    
#DICIONARIO QUE GUARDA A RESPOSTA DE CADA JOGADOR
tema_nome = {}
animal = {}
cor = {}
alimento = {}
profissao = {}
time_de_futebol = {}
parte_do_corpo = {}
marca = {}

#GUARDA A PONTUACAO DE CADA JOGADOR
pontuacao_jogadores = {}

N_RODADAS = 3
LETRA_SORTEADA = ' '

semaforo = threading.Semaphore(0)
semaforo_resposta_enviada = threading.Semaphore(0)

def atender_cliente(conn, addr):
    global LETRA_SORTEADA, tema_nome, animal, cor, alimento, profissao, time_de_futebol, parte_do_corpo, marca, pontuacao_jogadores, semaforo
    
    nomeJogador = conn.recv(1024).decode()
    pontuacao_jogadores[nomeJogador] = 0
    
    for r in range(N_RODADAS):
        semaforo.acquire()
        
        conn.sendall(LETRA_SORTEADA.encode())
        
        resposta = conn.recv(1024).decode().split('/')
        
        tema_nome[nomeJogador] = resposta[0]
        animal[nomeJogador] = resposta[1]
        cor[nomeJogador] = resposta[2]
        alimento[nomeJogador] = resposta[3]
        profissao[nomeJogador] = resposta[4]
        time_de_futebol[nomeJogador] = resposta[5]
        parte_do_corpo[nomeJogador] = resposta[6]
        marca[nomeJogador] = resposta[7]
        
        semaforo_resposta_enviada.release()

def iniciar_servidor():
    global LETRA_SORTEADA, semaforo, conexoes
    
    #
    qtd_jogadores = int(input("Digite a quantidade de jogadores para esta partida: "))
        
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen() 
        
        
        threads = []
        for i in range(qtd_jogadores):
            conn, addr = server.accept();
            print(f"Jogador do IP: {addr} conectado!")
            conexoes.append(conn)
            thread = threading.Thread(target=atender_cliente, args=(conn, addr))
            threads.append(thread)
            thread.start()
        
        listaDeDicionarios = [tema_nome, animal, cor, alimento, profissao, time_de_futebol, parte_do_corpo, marca]
        for r in range(N_RODADAS):
            LETRA_SORTEADA = random.choice(string.ascii_uppercase)
            print(f"\nRodada {r+1} iniciada! Letra: {LETRA_SORTEADA}")

            for _ in range(qtd_jogadores):
                semaforo.release()
                
            for _ in range(qtd_jogadores):
                semaforo_resposta_enviada.acquire()
                
            # Verificar a validade
            for tema in listaDeDicionarios:
                
                #Cria uma lista de respostas para depois fazer a contagem
                todas_respostas = []
                for valor in tema.values():
                    # Limpa e coloca na lista
                    item_limpo = str(valor).strip().upper()
                    todas_respostas.append(item_limpo)
                
                for jogador, resposta in tema.items():
                    resp_limpa = resposta.strip().upper()
                    
                    if not resp_limpa or resp_limpa[0] != LETRA_SORTEADA:
                         continue
                    else:
                            # CONTAGEM: Verifica se mais alguém escreveu a mesma coisa
                        if todas_respostas.count(resp_limpa) == 1:
                            pontuacao_jogadores[jogador] += 3
                        else:
                            pontuacao_jogadores[jogador] += 1
                        
            placar_parcial = f"\n--- PLACAR APÓS A RODADA {r+1} ---\n"
            for jogador, pontos in pontuacao_jogadores.items():
                placar_parcial += f"{jogador}: {pontos} pts\n"
                            
            for tema in listaDeDicionarios:
                    tema.clear()
                    
            for c in conexoes:
                c.sendall(placar_parcial.encode())
                
            #Estava enviando junto com a mensagem debaixo entao demos uma pequena pausa
            sleep(0.5)
                
                        
                            
    maior_pontuacao = max(pontuacao_jogadores.values())
            
    vencedores_msg = "--- VENCEDOR(ES) ---\n"
    for jogador in pontuacao_jogadores:
        if pontuacao_jogadores[jogador] == maior_pontuacao:
                vencedores_msg += f"{jogador} com {maior_pontuacao} pontos\n"
            
    for c in conexoes:
        c.sendall(vencedores_msg.encode())
                
    
    for thread in threads:
        thread.join()
            

if __name__ == "__main__":
    iniciar_servidor()
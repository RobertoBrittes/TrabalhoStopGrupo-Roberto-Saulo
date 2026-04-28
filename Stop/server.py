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

#Semaforo que controla os jogadores, bloquando até que o servidor sorteie a letra e depois libera junto
semaforo = threading.Semaphore(0)

#Semaforo que faz o servidor esperar que todos os jogadores enviem suas respostas para continuar
semaforo_resposta_enviada = threading.Semaphore(0)

def atender_cliente(conn, addr):
    global LETRA_SORTEADA, tema_nome, animal, cor, alimento, profissao, time_de_futebol, parte_do_corpo, marca, pontuacao_jogadores, semaforo
    
    #Recebe o nome do jogador e inicializa a pontuação em 0
    nomeJogador = conn.recv(1024).decode()
    pontuacao_jogadores[nomeJogador] = 0
    
    
    for r in range(N_RODADAS):
        #aguarda o servidor liberar
        semaforo.acquire()
        
        #envia a letra sorteada para o cliente
        conn.sendall(LETRA_SORTEADA.encode())
        
        #recebe a string de resposta separada por '/' e transforma em uma lista
        resposta = conn.recv(1024).decode().split('/')
        
        # armazena as respostas nos dicionarios para corrigir depois
        tema_nome[nomeJogador] = resposta[0]
        animal[nomeJogador] = resposta[1]
        cor[nomeJogador] = resposta[2]
        alimento[nomeJogador] = resposta[3]
        profissao[nomeJogador] = resposta[4]
        time_de_futebol[nomeJogador] = resposta[5]
        parte_do_corpo[nomeJogador] = resposta[6]
        marca[nomeJogador] = resposta[7]
        
        # informa para o servidor que esse jogador ja terminou de enviar as respostas
        semaforo_resposta_enviada.release()

def iniciar_servidor():
    global LETRA_SORTEADA, semaforo, conexoes
    
    # define a quantidade de jogadores na partida
    qtd_jogadores = int(input("Digite a quantidade de jogadores para esta partida: "))
        
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen() 
        
        # aceita conexoes até a quantidade de jogadores fornecida e encaminha cada uma dessa conexoes para um thread
        #armazena as threads e as conexoes em uma lista
        threads = []
        for i in range(qtd_jogadores):
            conn, addr = server.accept();
            print(f"Jogador do IP: {addr} conectado!")
            conexoes.append(conn)
            thread = threading.Thread(target=atender_cliente, args=(conn, addr))
            threads.append(thread)
            thread.start()
            
        for conexao in conexoes:
            conexao.sendall(str(N_RODADAS).encode())
        
        # lista para facilitar a correcao de cada tema
        listaDeDicionarios = [tema_nome, animal, cor, alimento, profissao, time_de_futebol, parte_do_corpo, marca]
        for r in range(N_RODADAS):
            # faz o sorteio da letra e armazena
            LETRA_SORTEADA = random.choice(string.ascii_uppercase)
            print(f"\nRodada {r+1} iniciada! Letra: {LETRA_SORTEADA}")

            # libera os jogadores ao mesmo tempo
            for _ in range(qtd_jogadores):
                semaforo.release()
            
            # espera todos os jogadores enviarem as respostas para continuar
            for _ in range(qtd_jogadores):
                semaforo_resposta_enviada.acquire()
                
            # logica de pontuacao e correcao
            # percorre toda a lista de dicionários (temas)
            for tema in listaDeDicionarios:
                
                #Cria uma lista das respostas para depois verificar se não há repetido
                todas_respostas = []
                
                #percorre o dicionário pegando as respostas
                for valor in tema.values():
                    # Limpa e coloca na lista
                    item_limpo = str(valor).strip().upper()
                    todas_respostas.append(item_limpo)
                
                # aqui ele percorre o dicionario pegando o jogador e sua respectiva resposta
                for jogador, resposta in tema.items():
                    #limpa e armazena
                    resposta_limpa = resposta.strip().upper()
                    
                    #verifica se a resposta está vazia ou se a resposta nao corresponde a letra sorteada
                    if not resposta_limpa or resposta_limpa[0] != LETRA_SORTEADA:
                         continue
                    else:
                            #verifica se mais alguém escreveu a mesma coisa e pontua o jogador partindo desse resultado
                        if todas_respostas.count(resposta_limpa) == 1:
                            pontuacao_jogadores[jogador] += 3
                        else:
                            pontuacao_jogadores[jogador] += 1
                        
            # monta a string do placar parcial para enviar aos jogadores
            placar_parcial = f"\n--- PLACAR APÓS A RODADA {r+1} ---\n"
            for jogador, pontos in pontuacao_jogadores.items():
                placar_parcial += f"{jogador}: {pontos} pts\n"
                            
            # limpa os dicionários para começar a próxima rodada
            for tema in listaDeDicionarios:
                    tema.clear()
            
            # envia o placar parcial para todos os jogadores conectados
            for c in conexoes:
                c.sendall(placar_parcial.encode())
                
            #Estava enviando junto com a mensagem debaixo entao demos uma pequena pausa
            sleep(0.5)
                
                        
    # verifica qual foi a maior pontuação
    maior_pontuacao = max(pontuacao_jogadores.values())
    
    # procura o(s) jogador(es) que tiveram essa pontuação maxima
    vencedores_msg = "--- VENCEDOR(ES) ---\n"
    for jogador in pontuacao_jogadores:
        if pontuacao_jogadores[jogador] == maior_pontuacao:
                vencedores_msg += f"{jogador} com {maior_pontuacao} pontos\n"
            
    # envia quem foi o vencedor para todos os jogadores
    for c in conexoes:
        c.sendall(vencedores_msg.encode())
                
    # espera todas as threads serem concluidas
    for thread in threads:
        thread.join()
            

if __name__ == "__main__":
    iniciar_servidor()
import socket

# Configurações (Devem ser iguais às do servidor)
HOST = '127.0.0.1' # Se for jogar no mesmo PC. Se for em rede, use o IP do PC onde o servidor está rodando.
PORT = 9002

def iniciar_cliente():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((HOST, PORT))

        print("="*30)
        print("      BEM-VINDO AO STOP!      ")
        print("="*30)

        nome = input("Digite seu nome para entrar na partida: ")
        cliente.sendall(nome.encode())
        print("\nAguardando os outros jogadores se conectarem...\n")

        for r in range(3):
            
            letra_sorteada = cliente.recv(1024).decode()
            if not letra_sorteada:
                break
                
            print("="*30)
            print(f"RODADA {r+1} - A LETRA É: >>> {letra_sorteada} <<<")
            print("="*30)
            
            print(f"Atenção: Suas respostas devem começar com a letra '{letra_sorteada}'!\n")
            
            resp_nome = input("1. Nome/Tema: ")
            resp_animal = input("2. Animal: ")
            resp_cor = input("3. Cor: ")
            resp_alimento = input("4. Alimento: ")
            resp_profissao = input("5. Profissão: ")
            resp_time = input("6. Time de Futebol: ")
            resp_corpo = input("7. Parte do Corpo: ")
            resp_marca = input("8. Marca: ")
            
            respostas_juntas = f"{resp_nome}/{resp_animal}/{resp_cor}/{resp_alimento}/{resp_profissao}/{resp_time}/{resp_corpo}/{resp_marca}"
            
            cliente.sendall(respostas_juntas.encode())
            print("\nRespostas enviadas! Aguardando os outros jogadores terminarem...")
            
            placar_parcial = cliente.recv(4096).decode()
            print(placar_parcial)
            
        print("\nCalculando o resultado final...")
        resultado_final = cliente.recv(4096).decode()
        print(resultado_final)
        
        cliente.close()
        input("\nPressione ENTER para sair.")

if __name__ == "__main__":
    iniciar_cliente()
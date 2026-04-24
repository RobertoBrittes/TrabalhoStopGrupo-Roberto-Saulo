# Jogo STOP - Cliente/Servidor em Python

Este projeto implementa o jogo **STOP** utilizando comunicação via sockets em Python, com suporte a múltiplos jogadores através de threads.

---

## Estrutura do Projeto

- `server.py` = Responsável por gerenciar o jogo (rodadas, pontuação, jogadores)
- `client.py` = Interface do jogador (envio de respostas e recebimento de resultados)

---

## ▶️ Como Executar

### 🔹 1. Iniciar o Servidor

Abra o diretório do STOP

No terminal, execute:

```bash
python server.py
```

---

O servidor irá solicitar:

`Digite a quantidade de jogadores para esta partida:`

Digite o número de jogadores que irão participar.

---

### 🔹 2. Iniciar os Clientes

Cada jogador deve executar:

```bash
python client.py
```

---

## Configuração de Rede

 **Por padrão, o jogo está configurado para rodar localmente (localhost / 127.0.0.1) na porta 9002.**

No arquivo client.py, configure o IP do servidor:

```python
HOST = '127.0.0.1'
```
**Casos:**\
Mesmo computador:\
Use 127.0.0.1

Computadores diferentes:\
Substitua pelo IP do computador onde o servidor está rodando, por exemplo:
```python
HOST = '192.168.0.10'
```

---

##  Como o Jogo Funciona
O servidor define o número de jogadores e aguarda conexões.\
Cada jogador informa seu nome ao entrar.\
O jogo ocorre em 3 rodadas.\
Em cada rodada:\
O servidor sorteia uma letra\
Os jogadores devem preencher categorias com palavras iniciadas pela letra
###  Categorias:
Nome\
Animal\
Cor\
Alimento\
Profissão\
Time de Futebol\
Parte do Corpo\
Marca

---

## Sistema de Pontuação
✅ Resposta válida e única: +3 pontos\
⚠️ Resposta válida mas repetida: +1 ponto\
❌ Resposta inválida ou vazia: 0 pontos

---

## Final do Jogo

Após todas as rodadas:

O servidor calcula a pontuação final
Exibe o(s) vencedor(es)


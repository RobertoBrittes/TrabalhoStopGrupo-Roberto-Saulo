# Sistema de Chat (Python + Sockets)

Este projeto implementa um sistema de chat, utilizando **sockets TCP**, **threads** e **semáforos** para controle de concorrência.

---

## Estrutura do Projeto

- `server_chat.py` = Servidor central responsável por gerenciar mensagens
- `client_enviador.py` = Cliente que envia mensagens (produtor)
- `client_recebedor.py` = Cliente que recebe mensagens (consumidor)

---

## Como Executar

### 🔹 1. Iniciar o Servidor

No terminal:

```bash
python server_chat.py
```

**Saída esperada:**\
Servidor escutando no IP: 127.0.0.1, PORTA: 5000\

---

### 🔹 2. Iniciar Clientes

#### Cliente Enviador (Produtor)
```bash
python3 client_enviador.py
```
- Digite seu nome
- Digite mensagens que serão enviadas ao chat\
#### Cliente Recebedor (Consumidor)
```bash
python client_recebedor.py
```
- Apenas recebe e exibe mensagens em tempo real

---

## Configuração de Rede

Nos arquivos de cliente, configure o IP do servidor:

```python
HOST = '127.0.0.1'
PORT = 5000
```
**Casos:**\
Mesmo computador:
Use 127.0.0.1

Computadores diferentes:
Use o IP da máquina do servidor:
```python
HOST = '192.168.X.X'
```

## Como o Sistema Funciona
### Arquitetura

O sistema segue o padrão:

Produtor (envia mensagens) → Servidor → Fila → Consumidor (recebe mensagens)\

---

### Threads no Servidor

O servidor utiliza múltiplas threads:

Thread produtora:
Recebe mensagens dos clientes enviadores\
Thread distribuidora:
Retira mensagens da fila e envia para os consumidores\

---

### Fila de Mensagens

As mensagens são armazenadas em uma lista (fila):

```python
FILA = []
```
**Fluxo:**

Produtor envia mensagem\
Servidor coloca na fila\
Consumidor recebe da fila\
Controle de Concorrência (Semáforos)

---

O sistema utiliza dois semáforos principais:

### 🔹 1. Acesso à Fila
```python
SEMAFORO_ACESSO = threading.Semaphore(1)
```

Garante que apenas uma thread por vez acesse a fila


### 🔹 2. Controle de Itens
```python
SEMAFORO_ITENS = threading.Semaphore(0)
```
Controla quantas mensagens existem na fila\
Consumidor só lê quando há mensagens disponíveis

---

### Fluxo de Mensagens
**Cliente enviador:** \
Conecta ao servidor\
Se identifica como "TIPO:PRODUTOR"\
Envia mensagens



**Servidor:**\
Adiciona horário e IP\
Armazena na fila\

**Thread distribuidora:**\
Retira da fila\
Envia para todos os consumidores\
Clientes recebedores exibem as mensagens

---

## Formato da Mensagem

As mensagens enviadas possuem o formato:

```
[Nome IP Hora]
Mensagem
```

Exemplo:

```
[João 192.168.0.5 14:32:10]
Olá, pessoal!
```

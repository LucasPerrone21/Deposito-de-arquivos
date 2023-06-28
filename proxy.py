import socket
from classes import *
import threading
import time
import subprocess

listaClientes = []
listaServidores = []



def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 7777))
    server.listen()
    print('Servidor iniciado!')
    while True:
        try:
            cliente_socket, endereco = server.accept()
            threading.Thread(target=identifica_id, args=(cliente_socket, endereco)).start()
        except:
            print('Erro na conexão!')
            break

def identifica_id(socket, addr):
    id = socket.recv(1024).decode('utf-8')
    if id == "Servidor":
        id_servidor = str(len(listaServidores))
        socket.send(id_servidor.encode('utf-8'))
        listaServidores.append(Servidor(id_servidor, socket))
        print(f'Servidor {len(listaServidores)} - conectado!')
    elif id == "Cliente":
        recepcao_clientes(socket, addr)



def recepcao_clientes(cliente_socket, endereco):
    '''
    função que recebe os clientes, registra e fica responsável por receber os arquivos e gerencia-los

    parametros: cliente_socket, endereco
    '''


    while True:
        username = cliente_socket.recv(1024).decode('utf-8')
        valor = True
        for c in range(len(listaClientes)):
            if listaClientes[c].username == username:
                valor = False
                break
        if valor:
            cliente_socket.send('True'.encode())
            usuario = Cliente(username, cliente_socket)
            listaClientes.append(usuario)
            print(f'Cliente {username} conectado! e registrado!')
            break
        else:
            cliente_socket.send('False'.encode())
            continue
    


# Gerenciar com os servidores


    while True:
        comando = cliente_socket.recv(1024).decode()
        comando = eval(comando)
        if comando[0] =="Deposito" :
            nome_arquivo = comando[1]
            numero_copias = comando[2]


            deposito(usuario, nome_arquivo, numero_copias)

            
        elif comando[0] == "Saque":
            saque(cliente_socket)


def deposito(usuario, nome_arquivo ,numero_copias):
    '''
    função que gerencia os servidores

    parametros: usuario: Cliente , nome_arquivo: str, numero_copias: int
    '''
    if len(listaServidores) < numero_copias:
        vezes = numero_copias - len(listaServidores) 
        for c in range(vezes):
            subprocess.Popen('python servidor.py')
            print('Servidor criado!')
            time.sleep(2)
    
    print('listaServidores: ', listaServidores)

    for c in range(numero_copias):
        listaServidores[c].socket.send(str(['Depositar', usuario.username , nome_arquivo]).encode('utf-8'))
    

    dados = usuario.socket.recv(1024)

    while dados:
        for c in range(numero_copias):
            listaServidores[c].socket.send(dados)
        if not dados:
            break
        dados = usuario.socket.recv(1024)
        try:
            tentativa = dados.decode('utf-8')
            if tentativa == 'ack':
                break
        except:
            pass
    print('Arquivo enviado para os servidores')










#    for c in range(numero_copias):
#        listaServidores[c].socket.send(str(['Depositar', usuario.username , nome_arquivo]).encode('utf-8'))
 #       dados = usuario.socket.recv(1024)
  #      while dados:
   #         listaServidores[c].socket.sendall(dados)
    #        dados = usuario.socket.recv(1024)
     #       try:
      #          if dados.decode('utf-8') == 'Fim' and c == numero_copias-1:
       #             b
        #    if not dados:
         #       break


def saque():
    pass


main()
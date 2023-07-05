import socket
from classes import *
import threading
import time
import subprocess
import random

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
        id_servidor = int(id_servidor)
        listaServidores.append(Servidor(id_servidor, socket))
        print(f'Servidor {id_servidor} - conectado!')
    elif id == "Cliente":
        recepcao_clientes(socket, addr)

def recvall(sock,buffer_size):
    '''
    Função que recebe os arquivos dos clientes e os armazena no servidor
    '''
    data = b''
    while True:
        part = sock.recv(buffer_size)
        data += part
        if len(part) < buffer_size:
            break
    return data

def recuperacao(user, nome_arquivo):
    '''
    Função que recupera os arquivos dos clientes e os armazena no servidor
    '''
    for c in range(len(user.arquivos)):
        if user.arquivos[c].nome_arquivo == nome_arquivo:
            arquivo = user.arquivos[c]
            n_server = random.choice(arquivo.localizacao)
            listaServidores[n_server].socket.send(str(['Recuperar', user.username, nome_arquivo]).encode('utf-8'))
            arquivo = recvall(listaServidores[n_server].socket, 1024)
            listaServidores[n_server].socket.send('ack'.encode('utf-8'))
            user.socket.sendall(arquivo)
            print('Arquivo recuperado com sucesso!')
            return True

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
            time.sleep(1)

    for c in range(numero_copias):
        listaServidores[c].socket.send(str(['Depositar', usuario.username , nome_arquivo]).encode('utf-8'))
    

    arquivo=recvall(usuario.socket, 1024)
    usuario.socket.send('ack'.encode('utf-8'))
    dados = Arquivo(nome_arquivo)
    for c in range(numero_copias):
        listaServidores[c].socket.sendall(arquivo)
        dados.localizacao.append(listaServidores[c].id)
        print('Arquivo enviado para o servidor ', c)
    usuario.arquivos.append(dados)
    print('Arquivo enviado para os servidores')

def deletar_arquivo(usuario, nome_arquivo,servidor_socket):
    '''
    função que deleta os arquivos dos clientes e os servidores

    parametros: usuario: Cliente , nome_arquivo: str
    '''
    for c in range(len(usuario.arquivos)):
        if usuario.arquivos[c].nome_arquivo == nome_arquivo:
            servidor_socket.send(str(['Deletar', usuario.username, nome_arquivo]).encode('utf-8'))
    return True
    

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

            
        elif comando[0] == "Recuperar":
            nome_arquivo = comando[1]
            recuperacao(usuario, nome_arquivo)

        elif comando[0] == 'EDC':
            nome_arquivo = comando[1]
            numero_copias = comando[2]
            for c in range(len(usuario.arquivos)):
                if usuario.arquivos[c].nome_arquivo == nome_arquivo:
                    arquivo = usuario.arquivos[c]

                    if len(arquivo.localizacao) < numero_copias:
                        n_server = random.choice(arquivo.localizacao)
                        listaServidores[n_server].socket.send(str(['Recuperar', usuario.username, nome_arquivo]).encode('utf-8'))
                        arquivo_recuperado = recvall(listaServidores[n_server].socket, 1024)
                        listaServidores[n_server].socket.send('ack'.encode('utf-8'))


                        if len(listaServidores) < numero_copias:
                            vezes = numero_copias - len(listaServidores) 

                        for c in range(vezes):
                            subprocess.Popen('python servidor.py')
                            time.sleep(1)

                        for c in range(numero_copias):
                            print(c)
                            print(arquivo.localizacao)
                            if c in arquivo.localizacao:
                                continue
                            else:
                                listaServidores[c].socket.send(str(['Depositar', usuario.username , nome_arquivo]).encode('utf-8'))
                                listaServidores[c].socket.sendall(arquivo_recuperado)
                                arquivo.localizacao.append(listaServidores[c].id)
                                print(arquivo.localizacao)
                                print('Arquivo enviado para o servidor ', c)

                    elif len(arquivo.localizacao) > numero_copias:
                        vezes = len(arquivo.localizacao) - numero_copias
                        anterior_servidores = arquivo.localizacao
                        atual_servidores = []
                        for c in anterior_servidores:
                            atual_servidores.append(c)
                        for c in anterior_servidores:
                            listaServidores[c].socket.send(str(['Deletar', usuario.username, nome_arquivo]).encode('utf-8'))
                            atual_servidores.remove(c)
                            print('Arquivo deletado do servidor ', c)
                        arquivo.localizacao = atual_servidores

        elif comando[0] == 'Deletar':
            nome_arquivo = comando[1]
            print('Deletando arquivo...')
            for c in range(len(usuario.arquivos)):
                print('entrei no loop')
                if usuario.arquivos[c].nome_arquivo == nome_arquivo:
                    arquivo = usuario.arquivos[c]
                    print('achei o arquivo')
                    print(arquivo.localizacao)
                    for c in range(len(arquivo.localizacao)):
                        listaServidores[arquivo.localizacao[c]].socket.send(str(['Deletar', usuario.username, nome_arquivo]).encode('utf-8'))
                        print('enviei o comando para o servidor')
                    usuario.arquivos.remove(arquivo)
                    print('Arquivo deletado com sucesso!')
                    break
            





main()
import socket
from classes import Arquivo
import os

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(('localhost', 7777))
    server.send('Servidor'.encode('utf-8'))
    numero_server = server.recv(1024).decode()
    if not os.path.exists(f'Conjunto Servidores/Servidor{numero_server}'):
        os.mkdir(f'Conjunto Servidores/Servidor{numero_server}')
        print("Pasta criada com sucesso!")
    else:
        print("A pasta já existe.")

    
    print(f'Servidor {numero_server} conectado!')

    while True:
        try:
            msg = eval(server.recv(1024).decode('utf-8'))
            if msg[0] == 'Depositar':
                username = msg[1]
                nome_arquivo = msg[2]
                depositar(username, nome_arquivo, numero_server,server)
            elif msg[0] == 'Recuperar':
                recuperar(msg[1], msg[2])
        
        except:
            print('Erro na conexão!')
            break

def depositar(username, nome_arquivo,numero_server,server):
    '''
    Função que recebe os arquivos dos clientes e os armazena no servidor
    '''


    endereco_cliente = f'Conjunto Servidores/Servidor{numero_server}/{username}'
    if not os.path.exists(endereco_cliente):
        os.makedirs(endereco_cliente)
        print("Pasta de usuário criada com sucesso!")
    
    endereco_arquivo = os.path.join(endereco_cliente, nome_arquivo)
    
    with open(endereco_arquivo, 'wb') as arquivo:
        while True:
            dados = server.recv(1024)
            if not dados:
                break
            arquivo.write(dados)
    
    return True


    
def recuperar():
    pass


main()
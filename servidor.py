import socket
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
                username = msg[1]
                nome_arquivo = msg[2]
                recuperar(username, nome_arquivo, numero_server,server)

            elif msg[0] == 'Deletar':
                username = msg[1]
                nome_arquivo = msg[2]
                delete(username, nome_arquivo, numero_server,server)
                   
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
        dados = recvall(server, 1024)
        arquivo.write(dados)
        return True

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
    
def recuperar(username, nome_arquivo,numero_server,server):
    '''
    Função que recupera os arquivos dos clientes e os armazena no servidor
    '''
    localizacao = f'Conjunto Servidores/Servidor{numero_server}/{username}/{nome_arquivo}'
    with open(localizacao, 'rb') as arquivo:
        dados = arquivo.read()
        server.sendall(dados)
        try:
            if server.recv(1024) == 'ack':
                print('Arquivo recuperado com sucesso!')
            return True
        except:
            return False

def delete(username, nome_arquivo,numero_server,server):
    '''
    Função que deleta os arquivos dos clientes
    '''
    localizacao = f'Conjunto Servidores/Servidor{numero_server}/{username}/{nome_arquivo}'
    if os.path.exists(localizacao):
        os.remove(localizacao)
        print("Arquivo deletado com sucesso!")
        return True
    else:
        print("O arquivo não existe!")
        return False


main()
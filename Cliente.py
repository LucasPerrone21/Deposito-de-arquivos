import PySimpleGUI as sg
import socket

def caca_nome(str):
    namefile =''
    c=len(str)
    while c != 0 and str[c-1] != '/':
        namefile += str[c-1]
        c -=1
    
    return namefile[::-1]

def envio(endereco_arquivo):
    with open(endereco_arquivo, 'rb') as arquivo:
        dados = arquivo.read()
        cliente.sendall(dados)
    print('Arquivo enviado para o servidor')
    if cliente.recv(1024).decode('utf-8') == 'ack':
        print('Fim do envio')
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

sg.theme('LightBlue6')

# Criando o socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('localhost', 7777))
cliente.send('Cliente'.encode('utf-8'))

#realizar tratamento de erro
while True:
    username = sg.popup_get_text('Digite seu nome de usuário:')
    if username == '':
        sg.popup_error('Você precisa digitar um nome de usuário válido!')
    else:
        cliente.send(username.encode('utf-8'))
        resposta = cliente.recv(1024).decode('utf-8')
        if resposta == 'True':
            sg.popup_ok(f'Bem-vindo {username}!')
            break
        elif(resposta == 'False'):
            sg.popup_error('Nome de usuário já está em uso!')
            continue


# Definindo o layout da tela
layout = [
    [sg.Text('Lista de arquivos depositados no servidor:')],
    [sg.Listbox(values=[], size=(30, 6), key='item_list')],
    [sg.Button('Depositar'), sg.Button('Recuperar'),sg.Button('Deletar'),  sg.Button('Editar Número de Cópias')]
]

# Criando a janela
window = sg.Window(f'Seja Bem-vindo {username}', layout)

# Loop para ler os eventos e atualizar a janela
while True:
    event, values = window.read()

    # Verificar se o usuário fechou a janela
    if event == sg.WINDOW_CLOSED:
        break

    # Verificar qual botão foi clicado
    if event == 'Depositar':
        n_copias = int(sg.popup_get_text('Digite o número de cópias que deseja depositar:'))
        try:
            endereco_arquivo = sg.popup_get_file('Selecione o arquivo que deseja depositar no servidor:')
            namefile = caca_nome(endereco_arquivo)
            cliente.send(str(['Deposito', namefile ,n_copias]).encode())
            envio(endereco_arquivo)
            itens_existentes = window['item_list'].Values
            print(itens_existentes)
            itens_existentes.append(namefile)
            print(itens_existentes)
            window['item_list'].update(values=itens_existentes)          
        except:
            print('deu ruim')
            pass
    
    if event == 'Recuperar':
        selected_item = values['item_list'][0] if values['item_list'] else None
        if selected_item:
            cliente.send(str(['Recuperar', selected_item]).encode('utf-8'))
            pasta = sg.popup_get_folder('Selecione a pasta onde deseja salvar o arquivo:')
            with open (pasta+'/'+selected_item, 'wb') as arquivo:
                dados = recvall(cliente, 1024)
                arquivo.write(dados)
            sg.popup_ok('Arquivo recuperado com sucesso!')
    
    if event == 'Editar Número de Cópias':
        selected_item = values['item_list'][0] if values['item_list'] else None
        if selected_item:
            n_copias = int(sg.popup_get_text('Digite o novo número de cópias:'))
            cliente.send(str(['EDC', selected_item, n_copias]).encode('utf-8'))
            sg.popup_ok('Número de cópias atualizado com sucesso!')
            if n_copias == 0:
                itens_existentes = window['item_list'].Values
                itens_existentes.remove(selected_item)
                window['item_list'].update(values=itens_existentes)
                print('tentei fazer o update')

    if event == 'Deletar':
        selected_item = values['item_list'][0] if values['item_list'] else None
        if selected_item:
            cliente.send(str(['Deletar', selected_item]).encode('utf-8'))
            itens_existentes = window['item_list'].Values
            print(itens_existentes)
            itens_existentes.remove(selected_item)
            window['item_list'].update(values=itens_existentes)
            print('tentei fazer o update')
            sg.popup_ok('Arquivo deletado com sucesso!')
window.close()
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
        

sg.theme('DarkAmber')

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
    [sg.Button('Depositar'), sg.Button('Recuperar')]
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
            cliente.send('ack'.encode())
            
                
        except:
            pass
    
    if event == 'Recuperar':
        pass
window.close()
import os
import win32api
import win32file
import win32security
from win10toast import ToastNotifier
import socket

# Função para obter o nome do usuário associado à última modificação do arquivo
def obter_usuario_modificador(caminho_arquivo):
    try:
        # Obtém as informações de segurança do arquivo
        info_seguranca = win32security.GetFileSecurity(caminho_arquivo, win32security.OWNER_SECURITY_INFORMATION)

        # Obtém o SID do modificador do arquivo
        sid_modificador = info_seguranca.GetSecurityDescriptorOwner()

        # Obtém o nome do usuário associado ao SID
        nome_usuario, _, _ = win32security.LookupAccountSid(None, sid_modificador)
        return nome_usuario
    except Exception as e:
        print(f"Erro ao obter o usuário modificante: {e}")
        return None


# Função para enviar uma notificação ao usuário
def enviar_notificacao(usuario, mensagem):
    try:
        toaster = ToastNotifier()
        toaster.show_toast(f"Notificação para {usuario}", mensagem, duration=10)
    except Exception as e:
        print(f"Erro ao enviar notificação: {e}")



# Função para enviar uma notificação para um computador remoto na rede
def enviar_notificacao_remota(ip_destino, porta_destino, mensagem):
    try:
        # Cria um socket TCP/IP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((socket.gethostname(), 12546))

        
        # Conecta ao endereço remoto
        sock.connect((ip_destino, porta_destino))

        # Envia a mensagem
        sock.sendall(mensagem.encode())

        # Fecha o socket
        sock.close()
    except Exception as e:
        print(f"Erro ao enviar notificação: {e}")


# Exemplo de uso
arquivo = r"C:\Users\marcos.silvaext\Documents\01 - INPUT_DATA\teste_1_linha.xlsx"
usuario_modificador = obter_usuario_modificador(arquivo)
""" ip_destino = '10.20.33.29'
porta_destino = 5432
mensagem = f'Este é um exemplo de notificação remota'
enviar_notificacao_remota(ip_destino, porta_destino, mensagem) """


if usuario_modificador:
    mensagem = f"Um novo arquivo foi modificado: {arquivo}"
    enviar_notificacao(usuario_modificador, mensagem)
    # print(f"O usuário '{usuario_modificador}' modificou o arquivo '{mensagem}'.")
else:
    print("Não foi possível determinar o usuário modificante do arquivo.")






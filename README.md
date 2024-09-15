# Calculadora-versionada
Programa básico que implementa uma simples calculadora e efetiva seu versionamento através  do repositório presente no github



pyinstaller --onefile --add-binary "/usr/lib/x86_64-linux-gnu/libpython3.10.so.1.0:." calc.py




import os
import sys
import platform
import subprocess
import stat
import requests
import time


ARQUIVO_VERSAO_LOCAL = "versao_atual.txt"

def carregar_versao_local():
    if os.path.exists(ARQUIVO_VERSAO_LOCAL):
        with open(ARQUIVO_VERSAO_LOCAL, "r") as arquivo:
            return arquivo.read().strip()
    return "1.0.0"  


def salvar_versao_local(nova_versao):
    with open(ARQUIVO_VERSAO_LOCAL, "w") as arquivo:
        arquivo.write(nova_versao)
    print(f"Versão {nova_versao} salva localmente.")

def verificar_nova_versao():
    try:
        url_versao = "https://raw.githubusercontent.com/VitorSquina/Calculadora-versionada/main/versao"
        response = requests.get(url_versao)

        if response.status_code == 200:
            versao_remota = response.text.strip()
            versao_local = carregar_versao_local()
            
            if versao_local != versao_remota:
                print(f"Nova versão disponível: {versao_remota}. Atualizando a calculadora...")
                atualizar_calculadora(versao_remota)  # Passando a versao_remota corretamente
            else:
                print("Você já está usando a versão mais recente.")
        else:
            print("Não foi possível verificar a versão mais recente.")
    except Exception as e:
        print(f"Erro ao verificar versão: {e}")

def baixar_arquivo_com_curl(url, destino):
    try:
        comando = f'curl -L {url} -o {destino}'  
        resultado = os.system(comando)
        if resultado == 0:
            print(f"Arquivo baixado com sucesso: {destino}")
        else:
            print(f"Erro ao baixar arquivo com curl. Código de retorno: {resultado}")
    except Exception as e:
        print(f"Erro ao baixar arquivo usando curl: {e}")

def atualizar_calculadora(versao_remota):
    try:
        url_exe = f"https://github.com/VitorSquina/Calculadora-versionada/releases/download/{versao_remota}/calc.exe"
        print(f"Baixando a nova versão de: {url_exe}")
        
        destino_arquivo = "calc.exe"  # Nome do arquivo de destino
        baixar_arquivo_com_curl(url_exe, destino_arquivo)

        salvar_versao_local(versao_remota)
        print("Atualização concluída! Reiniciando a calculadora...")

        # Verifica o sistema operacional e tenta executar o arquivo corretamente
        if platform.system() == "Windows":
            os.startfile(destino_arquivo)  # Reinicia no Windows
        else:
            print(f"Arquivo {destino_arquivo} baixado. Execute manualmente em um ambiente Windows.")  # Aviso para Linux

        sys.exit()  # Fecha a instância atual da calculadora

    except Exception as e:
        print(f"Erro ao baixar nova versão: {e}")

def dar_permissao_execucao(novo_arquivo):
    st = os.stat(novo_arquivo)
    os.chmod(novo_arquivo, st.st_mode | stat.S_IEXEC)

def soma(x, y):
    return x + y

def subtracao(x, y):
    return x - y

def multiplicacao(x, y):
    return x * y

def divisao(x, y):
    if y == 0:
        return "Erro: Divisão por zero"
    return x / y

def menu():
    print("\nEscolha a operação:")
    print("1 - Soma")
    print("2 - Subtração")
    print("3 - Multiplicação")
    print("4 - Divisão")
    print("5 - Atualizar")
    print("6 - Sair")

def operacao_calculadora():
    while True:
        menu()
        escolha = input("Digite sua escolha: ")

        if escolha == '6':
            print("Saindo da calculadora...")
            break

        if escolha in ['1', '2', '3', '4']:
            try:
                num1 = float(input("Digite o primeiro número: "))
                num2 = float(input("Digite o segundo número: "))

                if escolha == '1':
                    print(f"Resultado: {soma(num1, num2)}")
                elif escolha == '2':
                    print(f"Resultado: {subtracao(num1, num2)}")
                elif escolha == '3':
                    print(f"Resultado: {multiplicacao(num1, num2)}")
                elif escolha == '4':
                    print(f"Resultado: {divisao(num1, num2)}")

            except ValueError:
                print("Erro: Entrada inválida. Por favor, insira números válidos.")

        elif escolha == '5':
            print("Verificando atualização...")
            verificar_nova_versao()

        else:
            print("Escolha inválida, tente novamente.")

if __name__ == "__main__":
    operacao_calculadora()

import os
import sys
import platform
import subprocess
import stat
import requests
import tkinter as tk
from tkinter import messagebox

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
                atualizar_calculadora(versao_remota)
            else:
                messagebox.showinfo("Atualização", "Você já está usando a versão mais recente.")
        else:
            messagebox.showerror("Erro", "Não foi possível verificar a versão mais recente.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao verificar versão: {e}")

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
        sistema_operacional = platform.system()

        if sistema_operacional == "Windows":
            url_exe = f"https://github.com/VitorSquina/Calculadora-versionada/releases/download/{versao_remota}/calc.exe"
            destino_arquivo = "calc.exe"
        elif sistema_operacional == "Linux":
            url_exe = f"https://github.com/VitorSquina/Calculadora-versionada/releases/download/{versao_remota}/calc-linux"
            destino_arquivo = "calc-linux"
        else:
            messagebox.showerror("Erro", f"Sistema operacional {sistema_operacional} não suportado.")
            return

        print(f"Baixando a nova versão de: {url_exe}")
        baixar_arquivo_com_curl(url_exe, destino_arquivo)

        
        if sistema_operacional == "Linux":
            dar_permissao_execucao(destino_arquivo)

        salvar_versao_local(versao_remota)
        print("Atualização concluída! Reiniciando a calculadora...")

        # Reinicia 
        if sistema_operacional == "Windows":
            os.startfile(destino_arquivo)
        elif sistema_operacional == "Linux":
            os.execv(f"./{destino_arquivo}", [f"./{destino_arquivo}"])
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar nova versão: {e}")

def dar_permissao_execucao(novo_arquivo):
    st = os.stat(novo_arquivo)
    os.chmod(novo_arquivo, st.st_mode | stat.S_IEXEC)

def clique_botao(valor):
    entrada.insert(tk.END, valor)

def limpar():
    entrada.delete(0, tk.END)

def calcular():
    try:
        expressao = entrada.get()
        resultado = eval(expressao)
        limpar()
        entrada.insert(tk.END, resultado)
    except Exception as e:
        limpar()
        entrada.insert(tk.END, "Erro")

def criar_interface_calculadora():
    janela = tk.Tk()
    janela.title("Calculadora")

    global entrada
    entrada = tk.Entry(janela, width=35, borderwidth=5)
    entrada.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

    # Botões numéricos e operacionais
    botoes = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
        ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
    ]

    for (texto, linha, coluna) in botoes:
        if texto == '=':
            tk.Button(janela, text=texto, width=10, height=2, command=calcular).grid(row=linha, column=coluna)
        else:
            tk.Button(janela, text=texto, width=10, height=2, command=lambda valor=texto: clique_botao(valor)).grid(row=linha, column=coluna)

    tk.Button(janela, text='C', width=10, height=2, command=limpar).grid(row=4, column=2)
    tk.Button(janela, text='Atualizar', width=10, height=2, command=verificar_nova_versao).grid(row=5, column=0, columnspan=4)  # Parêntese fechado corretamente

    janela.mainloop()

if __name__ == "__main__":
    criar_interface_calculadora()
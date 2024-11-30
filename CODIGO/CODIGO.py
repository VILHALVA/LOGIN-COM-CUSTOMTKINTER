import customtkinter
import sqlite3
import os
import hashlib  
from tkinter import messagebox  

def obter_caminho_db():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "DATABASE.db")

def criar_banco_de_dados():
    caminho_db = obter_caminho_db()
    if not os.path.exists(caminho_db):
        conn = sqlite3.connect(caminho_db)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE usuarios (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            usuario TEXT NOT NULL,
                            senha TEXT NOT NULL
                          )''')
        conn.commit()
        conn.close()

def exibir_mensagem(msg):
    messagebox.showinfo("Mensagem", msg)

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def processar_usuario(usuario, senha_usuario, acao):
    caminho_db = obter_caminho_db()
    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()
    senha_criptografada = criptografar_senha(senha_usuario)

    if acao == "cadastrar":
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
        if not cursor.fetchone():
            cursor.execute('''CREATE TABLE usuarios (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                usuario TEXT NOT NULL,
                                senha TEXT NOT NULL
                              )''')
            conn.commit()

        cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
        if cursor.fetchone():
            exibir_mensagem("Este usuário já está cadastrado!")
            conn.close()
            return
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha_criptografada))
        conn.commit()
        exibir_mensagem("Cadastro realizado com sucesso!")
    
    elif acao == "login":
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha_criptografada))
        if cursor.fetchone():
            exibir_mensagem(f"Bem-vindo, {usuario}!")
        else:
            exibir_mensagem("Usuário ou senha incorretos.")
    
    conn.close()

def cadastrar():
    usuario_input = usuario.get()
    senha_usuario = senha.get()
    if not usuario_input or not senha_usuario:
        exibir_mensagem("Por favor, preencha ambos os campos!")
    else:
        processar_usuario(usuario_input, senha_usuario, "cadastrar")

def login():
    usuario_input = usuario.get()
    senha_usuario = senha.get()
    if not usuario_input or not senha_usuario:
        exibir_mensagem("Por favor, preencha ambos os campos!")
    else:
        processar_usuario(usuario_input, senha_usuario, "login")

criar_banco_de_dados()

janela = customtkinter.CTk()
janela.geometry("800x500")

texto = customtkinter.CTkLabel(janela, text="CADASTRO E LOGIN")
texto.pack(padx=10, pady=10)

usuario = customtkinter.CTkEntry(janela, placeholder_text="SEU USUÁRIO")
usuario.pack(padx=10, pady=10)

senha = customtkinter.CTkEntry(janela, placeholder_text="SUA SENHA", show="*")
senha.pack(padx=10, pady=10)

botao_cadastrar = customtkinter.CTkButton(janela, text="CADASTRAR", command=cadastrar)
botao_cadastrar.pack(padx=10, pady=10)

botao_login = customtkinter.CTkButton(janela, text="LOGIN", command=login)
botao_login.pack(padx=10, pady=10)

janela.mainloop()

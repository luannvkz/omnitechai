import tkinter as tk
from tkinter import messagebox

from config import USUARIO, SENHA


class Login:
    def __init__(self, root, ao_entrar):
        self.root, self.ao_entrar = root, ao_entrar
        self.frame = tk.Frame(root, padx=30, pady=30)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.frame, text="🤖 Omni Tech - Login", font=("Segoe UI", 16, "bold")).pack(pady=10)
        tk.Label(self.frame, text="Usuário").pack(anchor="w")
        self.user = tk.Entry(self.frame, width=28)
        self.user.pack(pady=4)
        tk.Label(self.frame, text="Senha").pack(anchor="w")
        self.senha = tk.Entry(self.frame, width=28, show="*")
        self.senha.pack(pady=4)
        tk.Button(self.frame, text="Entrar", width=20, command=self.entrar).pack(pady=12)
        self.senha.bind("<Return>", lambda e: self.entrar())
        self.user.focus()

    def entrar(self):
        if self.user.get() == USUARIO and self.senha.get() == SENHA:
            self.frame.destroy()
            self.ao_entrar(self.user.get())
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

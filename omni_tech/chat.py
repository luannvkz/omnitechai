import threading
import tkinter as tk

from config import NOME_BOT, ICONE_USER, ICONE_BOT, TEMAS
import ia


class Chat:
    def __init__(self, root, usuario):
        self.root, self.usuario = root, usuario
        self.tema, self.historico = "escuro", []

        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        topo = tk.Frame(self.frame)
        topo.pack(fill="both", expand=True)
        self.scroll = tk.Scrollbar(topo)
        self.scroll.pack(side="right", fill="y")
        self.texto = tk.Text(topo, wrap="word", state="disabled", relief="flat",
                             font=("Segoe UI", 11), padx=10, pady=10,
                             yscrollcommand=self.scroll.set)
        self.texto.pack(side="left", fill="both", expand=True)
        self.scroll.config(command=self.texto.yview)

        base = tk.Frame(self.frame)
        base.pack(fill="x", padx=8, pady=8)
        self.entrada = tk.Entry(base, font=("Segoe UI", 11), relief="flat")
        self.entrada.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 6))
        self.entrada.bind("<Return>", lambda e: self.enviar())
        self.btn_enviar = tk.Button(base, text="Enviar", command=self.enviar)
        self.btn_enviar.pack(side="left", padx=2)
        self.btn_limpar = tk.Button(base, text="Limpar", command=self.limpar)
        self.btn_limpar.pack(side="left", padx=2)
        self.btn_tema = tk.Button(base, text="Alternar Tema", command=self.alternar_tema)
        self.btn_tema.pack(side="left", padx=2)
        self.base = base

        self.aplicar_tema()
        self.mostrar(NOME_BOT, ICONE_BOT, "Olá, " + usuario + "! Pergunte algo sobre TI.", "bot")
        self.entrada.focus()

    def aplicar_tema(self):
        t = TEMAS[self.tema]
        for w in (self.frame, self.base):
            w.config(bg=t["bg"])
        self.texto.config(bg=t["bg"], fg=t["fg"])
        self.entrada.config(bg=t["entrada"], fg=t["fg"], insertbackground=t["fg"])
        for b in (self.btn_enviar, self.btn_limpar, self.btn_tema):
            b.config(bg=t["botao"], fg=t["fg"], relief="flat", padx=10)
        self.texto.tag_config("nome_user", justify="right", foreground="#6ea8fe",
                              font=("Segoe UI", 9, "bold"), lmargin1=120, lmargin2=120, rmargin=5)
        self.texto.tag_config("msg_user", justify="right", background=t["user"],
                              lmargin1=120, lmargin2=120, rmargin=5, spacing3=14)
        self.texto.tag_config("nome_bot", justify="left", foreground="#7ddc9a",
                              font=("Segoe UI", 9, "bold"), lmargin1=5, lmargin2=5, rmargin=120)
        self.texto.tag_config("msg_bot", justify="left", background=t["bot"],
                              lmargin1=5, lmargin2=5, rmargin=120, spacing3=14)

    def alternar_tema(self):
        self.tema = "claro" if self.tema == "escuro" else "escuro"
        self.aplicar_tema()

    def mostrar(self, nome, icone, msg, tipo):
        self.texto.config(state="normal")
        self.texto.insert("end", icone + " " + nome + "\n", "nome_" + tipo)
        self.texto.insert("end", " " + msg + " \n", "msg_" + tipo)
        self.texto.config(state="disabled")
        self.texto.see("end")

    def enviar(self):
        msg = self.entrada.get().strip()
        if not msg:
            return
        self.entrada.delete(0, "end")
        self.mostrar(self.usuario, ICONE_USER, msg, "user")
        self.historico.append({"role": "user", "content": msg})
        self.btn_enviar.config(state="disabled")
        self.root.after(800, lambda: threading.Thread(target=self.pedir_ia, daemon=True).start())

    def pedir_ia(self):
        resposta = ia.responder(self.historico)
        self.root.after(0, lambda: self.receber(resposta))

    def receber(self, resposta):
        self.historico.append({"role": "assistant", "content": resposta})
        self.mostrar(NOME_BOT, ICONE_BOT, resposta, "bot")
        self.btn_enviar.config(state="normal")

    def limpar(self):
        self.texto.config(state="normal")
        self.texto.delete("1.0", "end")
        self.texto.config(state="disabled")
        self.historico = []

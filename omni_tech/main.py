import tkinter as tk

from login import Login
from chat import Chat

root = tk.Tk()
root.title("Omni Tech - Chatbot")
root.geometry("640x520")
Login(root, lambda usuario: Chat(root, usuario))
root.mainloop()

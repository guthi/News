import tkinter as tk
from tkinter import messagebox, ttk

class NewsView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        root.title("Impacto das Notícias na Sua Profissão")

        self.label_profissao = tk.Label(root, text="Digite sua profissão:")
        self.label_profissao.pack(pady=10)

        self.entry_profissao = tk.Entry(root, width=40)
        self.entry_profissao.pack(pady=5)

        self.button_analisar = tk.Button(root, text="Analisar Impacto", command=self.controller.analisar_impacto)
        self.button_analisar.pack(pady=20)

        self.progress_bar = ttk.Progressbar(root, length=300, mode='determinate', maximum=100)
        self.progress_bar.pack(pady=10)

        self.result_text = tk.Text(root, height=20, width=70)
        self.result_text.pack(pady=10)

    def get_profissao(self):
        return self.entry_profissao.get()

    def show_result(self, text):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)

    def show_warning(self, msg):
        messagebox.showwarning("Aviso", msg)

    def show_error(self, msg):
        messagebox.showerror("Erro", msg)

    def update_progress(self, value):
        self.progress_bar['value'] = value
        self.progress_bar.update()

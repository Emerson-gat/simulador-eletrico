import tkinter as tk
from tkinter import messagebox


def abrir_modulo_lei_ohm():

    janela = tk.Toplevel()

    janela.title("Lei de Ohm")

    janela.geometry("900x700")

    tk.Label(
        janela,
        text="⚡ Lei de Ohm",
        font=("Arial", 20, "bold")
    ).pack(pady=10)

    tk.Label(
        janela,
        text="Tensão (V)"
    ).pack()

    entrada_v = tk.Entry(janela)
    entrada_v.pack()

    tk.Label(
        janela,
        text="Resistência (Ω)"
    ).pack()

    entrada_r = tk.Entry(janela)
    entrada_r.pack()

    resultado = tk.Text(
        janela,
        height=20,
        width=80
    )

    resultado.pack(pady=10)

    def calcular():

        try:

            v = float(
                entrada_v.get()
            )

            r = float(
                entrada_r.get()
            )

            i = v / r

            resultado.delete(
                "1.0",
                tk.END
            )

            resultado.insert(
                tk.END,

f"""
======================================
LEI DE OHM
======================================

I = V / R

I = {v} / {r}

I = {i:.4f} A

Resultado:

Corrente = {i:.4f} A
"""
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                str(erro)
            )

    tk.Button(
        janela,
        text="CALCULAR",
        command=calcular
    ).pack(pady=10)
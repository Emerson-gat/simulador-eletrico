import tkinter as tk
from tkinter import messagebox


def abrir_modulo_potencia():

    janela = tk.Toplevel()

    janela.title(
        "Potência Elétrica"
    )

    janela.geometry(
        "900x700"
    )

    tk.Label(
        janela,
        text="🔥 Potência Elétrica",
        font=("Arial", 20, "bold")
    ).pack(pady=10)

    tk.Label(
        janela,
        text="Tensão (V)"
    ).pack()

    entrada_v = tk.Entry(
        janela
    )

    entrada_v.pack()

    tk.Label(
        janela,
        text="Corrente (A)"
    ).pack()

    entrada_i = tk.Entry(
        janela
    )

    entrada_i.pack()

    resultado = tk.Text(
        janela,
        height=20,
        width=80
    )

    resultado.pack(
        pady=10
    )

    def calcular():

        try:

            v = float(
                entrada_v.get()
            )

            i = float(
                entrada_i.get()
            )

            p = v * i

            resultado.delete(
                "1.0",
                tk.END
            )

            resultado.insert(
                tk.END,

f"""
======================================
POTÊNCIA ELÉTRICA
======================================

P = V × I

P = {v} × {i}

P = {p:.2f} W

Resultado:

Potência = {p:.2f} W
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
    ).pack(
        pady=10
    )
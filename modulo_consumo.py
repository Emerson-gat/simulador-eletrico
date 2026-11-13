import tkinter as tk
from tkinter import messagebox


def abrir_modulo_consumo():

    janela = tk.Toplevel()

    janela.title(
        "Consumo de Energia"
    )

    janela.geometry(
        "900x700"
    )

    tk.Label(
        janela,
        text="🏠 Consumo de Energia",
        font=("Arial", 20, "bold")
    ).pack(
        pady=10
    )

    tk.Label(
        janela,
        text="Potência (W)"
    ).pack()

    entrada_potencia = tk.Entry(
        janela
    )

    entrada_potencia.pack()

    tk.Label(
        janela,
        text="Horas por dia"
    ).pack()

    entrada_horas = tk.Entry(
        janela
    )

    entrada_horas.pack()

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

            potencia = float(
                entrada_potencia.get()
            )

            horas = float(
                entrada_horas.get()
            )

            consumo = (
                potencia / 1000
            ) * horas * 30

            custo = consumo * 1.0

            resultado.delete(
                "1.0",
                tk.END
            )

            resultado.insert(
                tk.END,

f"""
======================================
CONSUMO DE ENERGIA
======================================

Potência = {potencia} W

Horas por dia = {horas}

Consumo Mensal:

({potencia}/1000)

× {horas}

× 30

= {consumo:.2f} kWh

Conta estimada:

R$ {custo:.2f}
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

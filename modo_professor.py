import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def abrir_modo_professor():

    janela = tk.Toplevel()

    janela.title(
        "Modo Professor"
    )

    janela.state("zoomed")

    janela.configure(
        bg="#101820"
    )

    titulo = tk.Label(
        janela,
        text="👨‍🏫 MODO PROFESSOR",
        bg="#101820",
        fg="white",
        font=("Arial", 24, "bold")
    )

    titulo.pack(
        pady=20
    )

    painel = tk.Frame(
        janela,
        bg="#1C2833"
    )

    painel.pack(
        fill="x",
        padx=20,
        pady=10
    )

    tk.Label(
        painel,
        text="Tema",
        bg="#1C2833",
        fg="white"
    ).pack()

    tema = ttk.Combobox(
        painel,
        width=50,
        values=[
            "Lei de Ohm",
            "Potência Elétrica",
            "Consumo de Energia",
            "Sistemas Lineares",
            "Método de Jacobi",
            "Método Gauss-Seidel"
        ]
    )

    tema.pack(
        pady=5
    )

    tk.Label(
        painel,
        text="Quantidade de Questões",
        bg="#1C2833",
        fg="white"
    ).pack()

    questoes = tk.Entry(
        painel
    )

    questoes.insert(
        0,
        "5"
    )

    questoes.pack(
        pady=5
    )

    resultado = tk.Text(
        janela,
        bg="black",
        fg="#00FF88",
        font=("Consolas", 11)
    )

    resultado.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    def gerar_lista():

        resultado.delete(
            "1.0",
            tk.END
        )

        assunto = tema.get()

        if not assunto:

            messagebox.showwarning(
                "Aviso",
                "Escolha um tema."
            )

            return

        lista = f"""
====================================
LISTA DE EXERCÍCIOS
====================================

Tema: {assunto}

"""

        if assunto == "Lei de Ohm":

            lista += """
1) Calcule a corrente para:

V = 220V
R = 10Ω


2) Calcule a corrente para:

V = 127V
R = 25Ω


3) Calcule a resistência:

V = 220V
I = 20A


4) Calcule a tensão:

I = 5A
R = 30Ω


5) Explique a Lei de Ohm.
"""

        elif assunto == "Potência Elétrica":

            lista += """
1) Calcule P:

V=220V
I=20A

2) Calcule P:

V=127V
I=10A

3) O que representa Watt?

4) Qual equipamento possui maior potência?

5) Explique potência elétrica.
"""

        elif assunto == "Consumo de Energia":

            lista += """
1) Chuveiro 5500W por 1h.

2) TV 150W por 5h.

3) Geladeira 300W por 24h.

4) Compare consumos.

5) Calcule custo mensal.
"""

        elif assunto == "Sistemas Lineares":

            lista += """
1)

x+y=5
x-y=1

2)

2x+y=7
x-y=2

3)

x+y+z=6
x-y=2
y+z=5

4) Forma matricial.

5) Aplicações.
"""

        resultado.insert(
            tk.END,
            lista
        )

    def gerar_gabarito():

        resultado.insert(
            tk.END,
            """

====================================
GABARITO (MODELO)
====================================

As respostas deverão ser
calculadas e conferidas
automaticamente em futuras versões.

"""
        )

    botoes = tk.Frame(
        janela,
        bg="#101820"
    )

    botoes.pack(
        pady=10
    )

    tk.Button(
        botoes,
        text="GERAR LISTA",
        bg="#00C853",
        fg="white",
        font=("Arial", 12, "bold"),
        command=gerar_lista
    ).pack(
        side="left",
        padx=10
    )

    tk.Button(
        botoes,
        text="GERAR GABARITO",
        bg="#2962FF",
        fg="white",
        font=("Arial", 12, "bold"),
        command=gerar_gabarito
    ).pack(
        side="left",
        padx=10
    )

    tk.Button(
        botoes,
        text="FECHAR",
        bg="#E53935",
        fg="white",
        font=("Arial", 12, "bold"),
        command=janela.destroy
    ).pack(
        side="left",
        padx=10
    )
def desenhar_circuito(canvas, corrente):

    canvas.delete("all")

    if corrente < 2:
        cor = "#00ff66"
        status = "BAIXA CORRENTE"
    elif corrente < 10:
        cor = "#ffaa00"
        status = "CORRENTE MODERADA"
    else:
        cor = "#ff3333"
        status = "CORRENTE ELEVADA"

    largura = int(canvas["width"])
    altura = int(canvas["height"])

    # Título

    canvas.create_text(
        largura // 2,
        20,
        text="SIMULAÇÃO ELÉTRICA",
        fill="white",
        font=("Arial", 16, "bold")
    )

    # Fonte

    canvas.create_rectangle(
        40,
        70,
        120,
        140,
        outline="#00ffff",
        width=3
    )

    canvas.create_text(
        80,
        90,
        text="FONTE",
        fill="white",
        font=("Arial", 10, "bold")
    )

    canvas.create_text(
        80,
        115,
        text="+ V",
        fill="#00ffff",
        font=("Arial", 14, "bold")
    )

    # Fio superior

    canvas.create_line(
        120,
        105,
        260,
        105,
        fill=cor,
        width=4,
        arrow="last"
    )

    # Resistor / carga

    canvas.create_rectangle(
        260,
        75,
        420,
        135,
        outline="#ffffff",
        width=3
    )

    canvas.create_text(
        340,
        105,
        text="CARGA",
        fill="white",
        font=("Arial", 12, "bold")
    )

    # Fio até medidor

    canvas.create_line(
        420,
        105,
        560,
        105,
        fill=cor,
        width=4,
        arrow="last"
    )

    # Medidor

    canvas.create_oval(
        560,
        70,
        650,
        140,
        outline="#00ff88",
        width=3
    )

    canvas.create_text(
        605,
        95,
        text="A",
        fill="#00ff88",
        font=("Arial", 18, "bold")
    )

    canvas.create_text(
        605,
        120,
        text=f"{corrente:.2f}",
        fill="#00ff88",
        font=("Arial", 10, "bold")
    )

    # Retorno

    canvas.create_line(
        605,
        140,
        605,
        200,
        fill=cor,
        width=4
    )

    canvas.create_line(
        605,
        200,
        80,
        200,
        fill=cor,
        width=4,
        arrow="last"
    )

    canvas.create_line(
        80,
        200,
        80,
        140,
        fill=cor,
        width=4
    )

    # Indicador principal

    canvas.create_text(
        largura // 2,
        240,
        text=f"{corrente:.2f} A",
        fill=cor,
        font=("Arial", 24, "bold")
    )

    # Status

    canvas.create_text(
        largura // 2,
        270,
        text=status,
        fill=cor,
        font=("Arial", 12, "bold")
    )

    # Legenda

    canvas.create_text(
        largura // 2,
        300,
        text="Fluxo de corrente representado pelas setas",
        fill="white",
        font=("Arial", 10)
    )
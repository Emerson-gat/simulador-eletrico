# ==========================================
# EXPLICACOES_DIDATICAS.PY
# Sistema de explicações para o simulador
# ==========================================


def explicar_corrente(corrente):

    if corrente < 2:

        return (
            "A corrente elétrica é baixa. "
            "Situação comum em equipamentos "
            "eletrônicos pequenos e lâmpadas LED."
        )

    elif corrente < 10:

        return (
            "A corrente elétrica é moderada. "
            "Situação comum em computadores, "
            "micro-ondas e eletrodomésticos."
        )

    elif corrente < 20:

        return (
            "A corrente elétrica é elevada. "
            "O circuito já exige atenção "
            "quanto ao dimensionamento."
        )

    else:

        return (
            "A corrente elétrica é muito alta. "
            "É necessário utilizar cabos e "
            "disjuntores adequados."
        )


def explicar_resistencia(resistencia):

    if resistencia > 100:

        return (
            "A resistência é alta. "
            "O equipamento limita bastante "
            "a passagem da corrente."
        )

    elif resistencia > 20:

        return (
            "A resistência é moderada. "
            "Permite uma corrente controlada."
        )

    else:

        return (
            "A resistência é baixa. "
            "A corrente elétrica pode aumentar "
            "consideravelmente."
        )


def explicar_potencia(potencia):

    if potencia < 100:

        return (
            "Consumo pequeno de energia. "
            "Exemplo: lâmpadas LED."
        )

    elif potencia < 1000:

        return (
            "Consumo intermediário. "
            "Exemplo: computadores e TVs."
        )

    elif potencia < 3000:

        return (
            "Consumo elevado. "
            "Exemplo: fornos e micro-ondas."
        )

    else:

        return (
            "Consumo muito elevado. "
            "Exemplo: chuveiros elétricos."
        )


def explicar_equipamento(nome):

    explicacoes = {

        "Lampada LED 9W":
        "Lâmpadas LED possuem baixo consumo e alta eficiência.",

        "Lampada LED 15W":
        "Modelo mais potente para ambientes maiores.",

        "Televisao 55":
        "A televisão converte energia elétrica em imagem e som.",

        "Computador":
        "Computadores utilizam fontes eletrônicas para alimentar seus componentes.",

        "Ventilador":
        "Transforma energia elétrica em movimento mecânico.",

        "Geladeira":
        "Utiliza um compressor elétrico para remover calor do interior.",

        "Microondas":
        "Transforma energia elétrica em ondas eletromagnéticas para aquecimento.",

        "Chuveiro 5500W":
        "Um dos maiores consumidores de energia residencial. Sua resistência converte energia elétrica em calor.",

        "Chuveiro 6800W":
        "Modelo de alta potência que exige circuito dedicado e cabeamento adequado.",

        "Ar Condicionado 12000 BTU":
        "Utiliza compressor e ventiladores para realizar troca térmica.",

        "Forno Eletrico":
        "Transforma energia elétrica em calor para cozimento."
    }

    return explicacoes.get(
        nome,
        "Equipamento sem descrição cadastrada."
    )


def gerar_aula(
    equipamento,
    tensao,
    resistencia,
    corrente,
    potencia
):

    texto = ""

    texto += (
        f"Equipamento analisado: {equipamento}\n\n"
    )

    texto += (
        f"Tensão aplicada: {tensao:.2f} V\n"
    )

    texto += (
        f"Resistência encontrada: "
        f"{resistencia:.2f} Ω\n"
    )

    texto += (
        f"Corrente elétrica: "
        f"{corrente:.2f} A\n"
    )

    texto += (
        f"Potência: "
        f"{potencia:.2f} W\n\n"
    )

    texto += (
        explicar_equipamento(
            equipamento
        )
    )

    texto += "\n\n"

    texto += (
        explicar_corrente(
            corrente
        )
    )

    texto += "\n\n"

    texto += (
        explicar_resistencia(
            resistencia
        )
    )

    texto += "\n\n"

    texto += (
        explicar_potencia(
            potencia
        )
    )

    return texto
def calcular_corrente(tensao, resistencia):

    if resistencia <= 0:
        raise ValueError(
            "A resistência deve ser maior que zero."
        )

    return tensao / resistencia


def calcular_potencia(tensao, corrente):

    return tensao * corrente


def calcular_resistencia(tensao, corrente):

    if corrente <= 0:
        raise ValueError(
            "A corrente deve ser maior que zero."
        )

    return tensao / corrente

def calcular_corrente_por_potencia(
    tensao,
    potencia
):

    return potencia / tensao

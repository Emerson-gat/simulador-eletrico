# ==========================================
# INSTALACOES_REAIS.PY
# Regras didáticas para instalações elétricas
# ==========================================


def disjuntor_recomendado(corrente):

    if corrente <= 10:
        return "10 A"

    elif corrente <= 16:
        return "16 A"

    elif corrente <= 20:
        return "20 A"

    elif corrente <= 25:
        return "25 A"

    elif corrente <= 32:
        return "32 A"

    elif corrente <= 40:
        return "40 A"

    elif corrente <= 50:
        return "50 A"

    elif corrente <= 63:
        return "63 A"

    return "Acima de 63 A"


def bitola_recomendada(corrente):

    if corrente <= 10:
        return "1.5 mm²"

    elif corrente <= 20:
        return "2.5 mm²"

    elif corrente <= 32:
        return "4 mm²"

    elif corrente <= 40:
        return "6 mm²"

    elif corrente <= 50:
        return "10 mm²"

    elif corrente <= 63:
        return "16 mm²"

    return "Projeto específico"


def classificacao_risco(corrente):

    if corrente < 5:

        return (
            "BAIXO",
            "✅ Circuito com baixa corrente."
        )

    elif corrente < 20:

        return (
            "MODERADO",
            "⚠ Corrente moderada."
        )

    elif corrente < 40:

        return (
            "ALTO",
            "🔥 Corrente elevada."
        )

    return (
        "CRÍTICO",
        "🚨 Corrente extremamente elevada."
    )


def consumo_hora(potencia):

    return potencia / 1000


def consumo_mensal(
    potencia,
    horas_dia=1
):

    kw = potencia / 1000

    return kw * horas_dia * 30


def custo_estimado(
    potencia,
    horas_dia=1,
    tarifa=1.0
):

    consumo = consumo_mensal(
        potencia,
        horas_dia
    )

    return consumo * tarifa


def relatorio_instalacao(
    tensao,
    corrente,
    potencia
):

    nivel, mensagem = classificacao_risco(
        corrente
    )

    return {

        "tensao": tensao,

        "corrente":
        round(corrente, 2),

        "potencia":
        round(potencia, 2),

        "disjuntor":
        disjuntor_recomendado(
            corrente
        ),

        "bitola":
        bitola_recomendada(
            corrente
        ),

        "risco":
        nivel,

        "mensagem":
        mensagem,

        "consumo_hora":
        round(
            consumo_hora(
                potencia
            ),
            2
        ),

        "consumo_mensal":
        round(
            consumo_mensal(
                potencia
            ),
            2
        ),

        "custo_estimado":
        round(
            custo_estimado(
                potencia
            ),
            2
        )

    }
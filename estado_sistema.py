import numpy as np

# Snapshot inicial para permitir restauração rápida a qualquer momento
_PADRAO_INICIAL = {
    "nome": "Sistema Padrão (Atividade Prática)",
    "A": np.array([
        [1.0, 1.0, 1.0],
        [4.0, 4.0, 2.0],
        [2.0, 1.0, -1.0]
    ], dtype=float),
    "b": np.array([1.0, 2.0, 0.0], dtype=float),
    "tol": 1e-4,
    "max_iter": 100
}

# Estado global compartilhado entre todos os módulos do simulador
_SISTEMA_ATUAL = {
    "nome": _PADRAO_INICIAL["nome"],
    "A": _PADRAO_INICIAL["A"].copy(),
    "b": _PADRAO_INICIAL["b"].copy(),
    "tol": _PADRAO_INICIAL["tol"],
    "max_iter": _PADRAO_INICIAL["max_iter"]
}

_HISTORICO_SISTEMAS = []
_OBSERVADORES = []


def registrar_observador(callback):
    """Permite que janelas abertas sejam notificadas automaticamente ao alterar o sistema."""
    if callback not in _OBSERVADORES:
        _OBSERVADORES.append(callback)


def remover_observador(callback):
    """Remove o callback quando uma janela é fechada."""
    if callback in _OBSERVADORES:
        _OBSERVADORES.remove(callback)


def _notificar_observadores():
    for callback in list(_OBSERVADORES):
        try:
            callback()
        except Exception:
            remover_observador(callback)


def obter_sistema():
    return (
        _SISTEMA_ATUAL["A"].copy(),
        _SISTEMA_ATUAL["b"].copy(),
        _SISTEMA_ATUAL["tol"],
        _SISTEMA_ATUAL["max_iter"],
        _SISTEMA_ATUAL["nome"]
    )


def atualizar_sistema(A, b, tol=1e-4, max_iter=100, nome="Sistema Personalizado"):
    A_novo = np.array(A, dtype=float)
    b_novo = np.array(b, dtype=float)

    _SISTEMA_ATUAL["A"] = A_novo
    _SISTEMA_ATUAL["b"] = b_novo
    _SISTEMA_ATUAL["tol"] = float(tol)
    _SISTEMA_ATUAL["max_iter"] = int(max_iter)
    _SISTEMA_ATUAL["nome"] = nome

    # Salva no histórico recente (máximo de 10 registros)
    _HISTORICO_SISTEMAS.append({
        "nome": nome,
        "A": A_novo.copy(),
        "b": b_novo.copy(),
        "tol": float(tol),
        "max_iter": int(max_iter)
    })
    if len(_HISTORICO_SISTEMAS) > 10:
        _HISTORICO_SISTEMAS.pop(0)

    _notificar_observadores()


def restaurar_padrao():
    atualizar_sistema(
        _PADRAO_INICIAL["A"],
        _PADRAO_INICIAL["b"],
        tol=_PADRAO_INICIAL["tol"],
        max_iter=_PADRAO_INICIAL["max_iter"],
        nome=_PADRAO_INICIAL["nome"]
    )


def obter_historico():
    return list(_HISTORICO_SISTEMAS)


def formatar_equacoes(A, b):
    variaveis = list(("x", "y", "z"))
    linhas = []
    for i in range(len(b)):
        termos = []
        for j in range(len(variaveis)):
            val = float(A[i][j])
            var = variaveis[j]

            if val == 0 and len(termos) > 0:
                continue

            if val == 1:
                coef = "" if j == 0 else "+ "
            elif val == -1:
                coef = "-" if j == 0 else "- "
            elif val > 0:
                coef = f"{val:g}" if j == 0 else f"+ {val:g}"
            else:
                coef = f"{val:g}" if j == 0 else f"- {abs(val):g}"

            termos.append(f"{coef}{var}")

        equacao_esq = " ".join(termos) if termos else "0"
        linhas.append(f"  {equacao_esq} = {float(b[i]):g}")
    return "\n".join(linhas)


def analisar_criterios_convergencia(A):
    A = np.array(A, dtype=float)
    n = len(A)

    # 1. Critério das Linhas (Diagonal Estritamente Dominante)
    dominante = True
    for i in range(n):
        diag = abs(A[i][i])
        soma_outros = sum(abs(A[i][j]) for j in range(n) if j != i)
        if diag <= soma_outros:
            dominante = False
            break

    # 2. Critério de Sassenfeld (Convergência garantida para Gauss-Seidel)
    betas = np.zeros(n)
    for i in range(n):
        if A[i][i] == 0:
            return dominante, False, float("inf")
        soma1 = sum(abs(A[i][j]) * betas[j] for j in range(i))
        soma2 = sum(abs(A[i][j]) for j in range(i + 1, n))
        betas[i] = (soma1 + soma2) / abs(A[i][i])

    beta_max = float(np.max(betas))
    sassenfeld_ok = beta_max < 1.0
    return dominante, sassenfeld_ok, beta_max


def diagnosticar_matriz(A):
    """Retorna um dicionário detalhado com determinante, condicionamento e critérios."""
    A = np.array(A, dtype=float)
    det = float(np.linalg.det(A))
    singular = abs(det) < 1e-12
    dominante, sassenfeld_ok, beta_max = analisar_criterios_convergencia(A)

    return {
        "determinante": det,
        "singular": singular,
        "diagonal_dominante": dominante,
        "sassenfeld_ok": sassenfeld_ok,
        "beta_max": beta_max
    }

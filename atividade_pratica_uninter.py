import numpy as np
import time


def executar_jacobi(A, b, tol=1e-4, max_iter=100):
    n = len(b)
    x = np.zeros(n, dtype=float)
    historico = []
    inicio = time.perf_counter()

    for k in range(1, max_iter + 1):
        x_novo = np.zeros(n, dtype=float)
        for i in range(n):
            soma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_novo[i] = (b[i] - soma) / A[i][i]

        erro = np.max(np.abs(x_novo - x))
        historico.append((k, x_novo.copy(), erro))
        x = x_novo

        if np.isnan(erro) or erro > 1e10:
            tempo_ms = (time.perf_counter() - inicio) * 1000
            return x, k, erro, tempo_ms, historico, False

        if erro < tol:
            tempo_ms = (time.perf_counter() - inicio) * 1000
            return x, k, erro, tempo_ms, historico, True

    tempo_ms = (time.perf_counter() - inicio) * 1000
    return x, max_iter, erro, tempo_ms, historico, False


def executar_gauss_seidel(A, b, tol=1e-4, max_iter=100):
    n = len(b)
    x = np.zeros(n, dtype=float)
    historico = []
    inicio = time.perf_counter()

    for k in range(1, max_iter + 1):
        x_ant = x.copy()
        for i in range(n):
            soma1 = sum(A[i][j] * x[j] for j in range(i))
            soma2 = sum(A[i][j] * x_ant[j] for j in range(i + 1, n))
            x[i] = (b[i] - soma1 - soma2) / A[i][i]

        erro = np.max(np.abs(x - x_ant))
        historico.append((k, x.copy(), erro))

        if np.isnan(erro) or erro > 1e6:
            tempo_ms = (time.perf_counter() - inicio) * 1000
            return x, k, erro, tempo_ms, historico, False

        if erro < tol:
            tempo_ms = (time.perf_counter() - inicio) * 1000
            return x, k, erro, tempo_ms, historico, True

    tempo_ms = (time.perf_counter() - inicio) * 1000
    return x, max_iter, erro, tempo_ms, historico, False


def main():
    print("=" * 75)
    print("ATIVIDADE PRÁTICA LOCORREGIONAL - UNINTER")
    print("DISCIPLINA: Métodos Computacionais para Sistemas Lineares")
    print("=" * 75)

    # 1 e 2. Definição das matrizes A e b para o sistema linear do enunciado:
    #  x +  y + z = 1
    # 4x + 4y + 2z = 2
    # 2x +  y - z = 0
    A = np.array([
        [1.0, 1.0, 1.0],
        [4.0, 4.0, 2.0],
        [2.0, 1.0, -1.0]
    ])
    b = np.array([1.0, 2.0, 0.0])

    print("\n1. REPRESENTAÇÃO MATRICIAL (Ax = b):")
    print(f"Matriz A:\n{A}\n")
    print(f"Vetor b: {b}\n")

    # Solução analítica exata via NumPy apenas para referência de erro
    x_exato = np.linalg.solve(A, b)
    print(f"Solução Exata de Referência: x = {x_exato[0]:.4f}, y = {x_exato[1]:.4f}, z = {x_exato[2]:.4f}")

    # Execução do Método de Jacobi
    sol_jac, it_jac, err_jac, tempo_jac, hist_jac, conv_jac = executar_jacobi(A, b)

    print("\n" + "-" * 75)
    print("2A. EXECUÇÃO DO MÉTODO DE JACOBI (Primeiras 5 iterações):")
    print("-" * 75)
    for k, vals, err in hist_jac[:5]:
        print(f"Iteração {k:02d} | x = {vals[0]:10.4f} | y = {vals[1]:10.4f} | z = {vals[2]:10.4f} | Erro = {err:.6f}")

    # Execução do Método de Gauss-Seidel
    sol_gs, it_gs, err_gs, tempo_gs, hist_gs, conv_gs = executar_gauss_seidel(A, b)

    print("\n" + "-" * 75)
    print("2B. EXECUÇÃO DO MÉTODO DE GAUSS-SEIDEL (Primeiras 5 iterações):")
    print("-" * 75)
    for k, vals, err in hist_gs[:5]:
        print(f"Iteração {k:02d} | x = {vals[0]:10.4f} | y = {vals[1]:10.4f} | z = {vals[2]:10.4f} | Erro = {err:.6f}")

    # 3. Comparação de Velocidade e Erro
    print("\n" + "=" * 75)
    print("3. COMPARAÇÃO DE VELOCIDADE E ERRO (JACOBI vs GAUSS-SEIDEL)")
    print("=" * 75)
    print(f"{'MÉTODO':<15} | {'STATUS':<12} | {'ITERAÇÕES':<10} | {'TEMPO (ms)':<12} | {'ERRO FINAL':<15}")
    print("-" * 75)
    print(f"{'Jacobi':<15} | {'Convergiu' if conv_jac else 'Divergiu':<12} | {it_jac:<10} | {tempo_jac:<12.4f} | {err_jac:<15.4e}")
    print(f"{'Gauss-Seidel':<15} | {'Convergiu' if conv_gs else 'Divergiu':<12} | {it_gs:<10} | {tempo_gs:<12.4f} | {err_gs:<15.4e}")
    print("-" * 75)
    print("CONCLUSÃO TÉCNICA:")
    print("- Diferença Algorítmica: Jacobi usa apenas valores da iteração anterior (k),")
    print("  enquanto Gauss-Seidel usa imediatamente os valores atualizados na mesma iteração.")
    print("- Convergência: Como a matriz A original não é diagonalmente dominante (não atende")
    print("  ao Critério das Linhas nem ao Critério de Sassenfeld), ambos os métodos divergem")
    print("  para este sistema específico, embora o erro de Gauss-Seidel cresça mais devagar.")
    print("=" * 75)


if __name__ == "__main__":
    main()

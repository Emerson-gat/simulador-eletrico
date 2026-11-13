import tkinter as tk
import numpy as np
import time
from estado_sistema import obter_sistema, formatar_equacoes, analisar_criterios_convergencia


def executar_jacobi(A, b, tol=1e-4, max_iter=100):
    n = len(b)
    x = np.zeros(n, dtype=float)
    historico = []
    inicio = time.perf_counter()

    # Proteção contra divisão por zero na diagonal
    for i in range(n):
        if A[i][i] == 0:
            tempo_ms = (time.perf_counter() - inicio) * 1000
            return x, 0, float("inf"), tempo_ms, historico, False

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


def abrir_modulo_jacobi():
    janela = tk.Toplevel()
    janela.title("Método de Jacobi")
    janela.geometry("1000x700")

    topo = tk.Frame(janela)
    topo.pack(fill="x", padx=10, pady=5)

    texto = tk.Text(janela, font=("Consolas", 11))
    texto.pack(fill="both", expand=True, padx=10, pady=10)

    def atualizar_tela():
        texto.delete("1.0", tk.END)

        # Puxa as matrizes A e b sincronizadas da tela de Sistemas Lineares
        A, b, tol, max_iter, nome = obter_sistema()
        dominante, _, _ = analisar_criterios_convergencia(A)

        solucao, iteracoes, erro_final, tempo_ms, historico, convergiu = executar_jacobi(
            A, b, tol=tol, max_iter=max_iter
        )

        saida = []
        saida.append("==========================================================")
        saida.append(f"MÉTODO ITERATIVO DE JACOBI | {nome.upper()}")
        saida.append("==========================================================")
        saida.append("Sistema Linear:")
        saida.append(formatar_equacoes(A, b) + "\n")
        saida.append(f"Matriz A:\n{A}\n")
        saida.append(f"Vetor b: {b}")
        saida.append(f"Diagonal Dominante: {'SIM (Convergência garantida)' if dominante else 'NÃO (Risco de divergência)'}\n")
        saida.append("----------------------------------------------------------")
        saida.append(f"HISTÓRICO DE ITERAÇÕES (Tolerância = {tol}):")
        saida.append("----------------------------------------------------------")

        for k, vals, err in historico:
            saida.append(
                f"Iteração {k:02d} | x = {vals[0]:10.4f} | y = {vals[1]:10.4f} | z = {vals[2]:10.4f} | Erro = {err:.6f}"
            )

        saida.append("\n==========================================================")
        saida.append("RESULTADO FINAL - JACOBI")
        saida.append("==========================================================")
        saida.append(f"Status       : {'Convergiu' if convergiu else 'Não convergiu'}")
        saida.append(f"Solução      : x = {solucao[0]:.4f}, y = {solucao[1]:.4f}, z = {solucao[2]:.4f}")
        saida.append(f"Iterações    : {iteracoes}")
        saida.append(f"Erro Final   : {erro_final:.6f}")
        saida.append(f"Velocidade   : {tempo_ms:.4f} ms")

        texto.insert(tk.END, "\n".join(saida))

    tk.Button(
        topo,
        text="🔄 Atualizar com Sistema Atual",
        command=atualizar_tela,
        bg="#00C853",
        fg="white",
        font=("Arial", 10, "bold")
    ).pack(side="right")

    atualizar_tela()

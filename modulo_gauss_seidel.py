import tkinter as tk
import numpy as np
import time
from estado_sistema import obter_sistema, formatar_equacoes, analisar_criterios_convergencia


def executar_gauss_seidel(A, b, tol=1e-4, max_iter=100):
    n = len(b)
    x = np.zeros(n, dtype=float)
    historico = []
    inicio = time.perf_counter()

    # Proteção contra divisão por zero na diagonal principal
    for i in range(n):
        if A[i][i] == 0:
            tempo_ms = (time.perf_counter() - inicio) * 1000
            return x, 0, float("inf"), tempo_ms, historico, False

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


def abrir_modulo_gauss_seidel():
    janela = tk.Toplevel()
    janela.title("Método de Gauss-Seidel")
    janela.geometry("1000x700")

    topo = tk.Frame(janela)
    topo.pack(fill="x", padx=10, pady=5)

    texto = tk.Text(janela, font=("Consolas", 11))
    texto.pack(fill="both", expand=True, padx=10, pady=10)

    def atualizar_tela():
        texto.delete("1.0", tk.END)

        # Puxa as matrizes A e b sincronizadas da tela de Sistemas Lineares
        A, b, tol, max_iter, nome = obter_sistema()
        dominante, sassenfeld_ok, beta_max = analisar_criterios_convergencia(A)

        solucao, iteracoes, erro_final, tempo_ms, historico, convergiu = executar_gauss_seidel(
            A, b, tol=tol, max_iter=max_iter
        )

        saida = []
        saida.append("==========================================================")
        saida.append(f"MÉTODO ITERATIVO DE GAUSS-SEIDEL | {nome.upper()}")
        saida.append("==========================================================")
        saida.append("Sistema Linear:")
        saida.append(formatar_equacoes(A, b) + "\n")
        saida.append(f"Matriz A:\n{A}\n")
        saida.append(f"Vetor b: {b}")
        saida.append(f"Critério de Sassenfeld (β_max < 1): β_max = {beta_max:.4f} -> {'ATENDE' if sassenfeld_ok else 'NÃO ATENDE'}\n")
        saida.append("----------------------------------------------------------")
        saida.append(f"HISTÓRICO DE ITERAÇÕES (Tolerância = {tol}):")
        saida.append("----------------------------------------------------------")

        for k, vals, err in historico[:15]:
            saida.append(
                f"Iteração {k:02d} | x = {vals.item(0):10.4f} | y = {vals.item(1):10.4f} | z = {vals.item(2):10.4f} | Erro = {err:.4f}"
            )

        if len(historico) > 15:
            saida.append(f"... ({len(historico) - 15} iterações seguintes omitidas devido ao excesso de iterações/erro)")

        saida.append("\n==========================================================")
        saida.append("RESULTADO FINAL - GAUSS-SEIDEL")
        saida.append("==========================================================")
        saida.append(f"Status       : {'Convergiu' if convergiu else 'DIVERGIU (Erro crescente)'}")
        saida.append(f"Solução      : x = {solucao.item(0):.4f}, y = {solucao.item(1):.4f}, z = {solucao.item(2):.4f}")
        saida.append(f"Iterações    : {iteracoes}")
        saida.append(f"Erro Final   : {erro_final:.4e}")
        saida.append(f"Velocidade   : {tempo_ms:.4f} ms")
        saida.append("\nOBSERVAÇÃO TÉCNICA:")
        if convergiu:
            saida.append("O sistema atendeu aos critérios de convergência e atingiu")
            saida.append("a tolerância usando os valores atualizados na própria iteração.")
        else:
            saida.append("A matriz A atual não atende aos critérios de dominância diagonal")
            saida.append("nem ao Critério de Sassenfeld, fazendo o erro crescer a cada passo.")

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

import tkinter as tk
from tkinter import messagebox
import numpy as np
import time
from modulo_jacobi import executar_jacobi
from modulo_gauss_seidel import executar_gauss_seidel
from estado_sistema import obter_sistema, atualizar_sistema, analisar_criterios_convergencia


def abrir_modulo_sistemas_lineares():
    janela = tk.Toplevel()
    janela.title("Sistemas Lineares - Comparação Jacobi vs Gauss-Seidel")
    janela.geometry("1000x720")

    tk.Label(
        janela,
        text="📐 Sistemas Lineares: Jacobi vs Gauss-Seidel",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    entradas = []
    frame = tk.Frame(janela)
    frame.pack(pady=5)

    headers = list(("x", "y", "z", "b"))
    for col, titulo in enumerate(headers):
        tk.Label(frame, text=titulo, font=("Arial", 10, "bold")).grid(row=0, column=col)

    for linha in range(3):
        linha_entries = []
        for coluna in range(4):
            e = tk.Entry(frame, width=10, justify="center")
            e.grid(row=linha + 1, column=coluna, padx=4, pady=4)
            linha_entries.append(e)
        entradas.append(linha_entries)

    botoes_frame = tk.Frame(janela)
    botoes_frame.pack(pady=8)

    resultado = tk.Text(janela, height=26, width=110, font=("Consolas", 10))
    resultado.pack(pady=8, padx=10, fill="both", expand=True)

    nome_sistema = tk.StringVar(value="Sistema Padrão")

    def preencher_grid(valores, nome="Sistema Personalizado"):
        nome_sistema.set(nome)
        for i in range(3):
            for j in range(4):
                entradas[i][j].delete(0, tk.END)
                entradas[i][j].insert(0, f"{valores[i][j]:g}")

    def exemplo_pdf():
        valores = list((
            list((1, 1, 1, 1)),
            list((4, 4, 2, 2)),
            list((2, 1, -1, 0))
        ))
        preencher_grid(valores, "Sistema Padrão (3x3)")
        resolver()

    def exemplo_convergente():
        valores = list((
            list((4, -1, 1, 7)),
            list((1, 5, 1, -8)),
            list((2, 3, 10, 6))
        ))
        preencher_grid(valores, "Sistema Diagonalmente Dominante")
        resolver()

    def otimizar_linhas():
        try:
            matriz = []
            for i in range(3):
                matriz.append([float(entradas[i][j].get()) for j in range(4)])

            for col in range(3):
                melhor = max(range(col, 3), key=lambda r: abs(matriz[r][col]))
                matriz[col], matriz[melhor] = matriz[melhor], matriz[col]

            preencher_grid(matriz, f"{nome_sistema.get()} (Reordenado)")
            resolver()
        except Exception as erro:
            messagebox.showerror("Erro ao reordenar", str(erro))

    def resolver():
        try:
            A = np.array([
                [
                    float(entradas[i][0].get()),
                    float(entradas[i][1].get()),
                    float(entradas[i][2].get())
                ]
                for i in range(3)
            ])
            b = np.array([float(entradas[i][3].get()) for i in range(3)])

            # Alimenta automaticamente o estado global para todas as outras telas
            atualizar_sistema(A, b, nome=nome_sistema.get())

            # Analisa critérios matemáticos de convergência
            dominante, sassenfeld_ok, beta_max = analisar_criterios_convergencia(A)

            # 1. Solução Exata (Referência)
            t0 = time.perf_counter()
            x_exato = np.linalg.solve(A, b)
            tempo_exato = (time.perf_counter() - t0) * 1000

            # 2. Método de Jacobi
            x_jac, it_jac, err_jac, tempo_jac, _, conv_jac = executar_jacobi(A, b)
            erro_real_jac = np.max(np.abs(x_jac - x_exato)) if conv_jac else float("inf")

            # 3. Método de Gauss-Seidel
            x_gs, it_gs, err_gs, tempo_gs, _, conv_gs = executar_gauss_seidel(A, b)
            erro_real_gs = np.max(np.abs(x_gs - x_exato)) if conv_gs else float("inf")

            if conv_jac and conv_gs:
                texto_convergencia = (
                    f"Como a matriz atende aos critérios de convergência, ambos atingiram a solução exata.\n"
                    f"   Gauss-Seidel convergiu em {it_gs} iterações contra {it_jac} de Jacobi."
                )
            else:
                texto_convergencia = (
                    "Na ordem atual, a matriz A não é diagonalmente dominante (e não atende ao Critério\n"
                    "   de Sassenfeld), fazendo com que os métodos iterativos divirjam."
                )

            resultado.delete("1.0", tk.END)
            relatorio = f"""================================================================================
COMPARAÇÃO DE MÉTODOS COMPUTACIONAIS | {nome_sistema.get().upper()}
================================================================================
Matriz A:
{A}

Vetor b: {b}
Diagnóstico: Diagonal Dominante = {'SIM' if dominante else 'NÃO'} | Sassenfeld (β={beta_max:.3f}) = {'SIM' if sassenfeld_ok else 'NÃO'}

Solução Exata (Referência): x = {x_exato.item(0):.4f} | y = {x_exato.item(1):.4f} | z = {x_exato.item(2):.4f}
--------------------------------------------------------------------------------
MÉTODO          | STATUS      | ITERAÇÕES | TEMPO (ms) | ERRO ITERATIVO | ERRO REAL
--------------------------------------------------------------------------------
Jacobi          | {'Convergiu' if conv_jac else 'Divergiu':<11} | {it_jac:<9} | {tempo_jac:<10.4f} | {err_jac:<14.6f} | {erro_real_jac:.6f}
Gauss-Seidel    | {'Convergiu' if conv_gs else 'Divergiu':<11} | {it_gs:<9} | {tempo_gs:<10.4f} | {err_gs:<14.6f} | {erro_real_gs:.6f}
Exato (NumPy)   | Direto      | -         | {tempo_exato:<10.4f} | 0.000000       | 0.000000
--------------------------------------------------------------------------------
RESULTADOS OBTIDOS:
• Jacobi       : x = {x_jac.item(0):.4f}, y = {x_jac.item(1):.4f}, z = {x_jac.item(2):.4f}
• Gauss-Seidel : x = {x_gs.item(0):.4f}, y = {x_gs.item(1):.4f}, z = {x_gs.item(2):.4f}

ANÁLISE COMPARATIVA (VELOCIDADE E ERRO):
1. Diferença Algorítmica: O Método de Jacobi utiliza apenas os valores da iteração
   anterior (k) para calcular toda a nova iteração (k+1). Já o Método de Gauss-Seidel
   atualiza cada variável imediatamente e já usa os valores recém-calculados dentro
   da própria iteração.
2. Velocidade e Convergência: {texto_convergencia}
   (Nota: Os dados deste sistema já foram sincronizados com as janelas de Jacobi e Gauss-Seidel).
================================================================================
"""
            resultado.insert(tk.END, relatorio)

        except Exception as erro:
            messagebox.showerror("Erro ao calcular", f"Verifique os valores inseridos.\nDetalhe: {erro}")

    tk.Button(botoes_frame, text="Carregar Sistema Padrão", command=exemplo_pdf).pack(side="left", padx=5)
    tk.Button(botoes_frame, text="Carregar Exemplo Dominante", command=exemplo_convergente).pack(side="left", padx=5)
    tk.Button(botoes_frame, text="Reordenar Linhas", command=otimizar_linhas).pack(side="left", padx=5)
    tk.Button(botoes_frame, text="Resolver e Comparar", command=resolver, bg="#d0e8ff").pack(side="left", padx=5)

    # Inicia carregando o estado atual compartilhado
    A_init, b_init, _, _, nome_init = obter_sistema()
    grid_init = [[A_init[i][0], A_init[i][1], A_init[i][2], b_init[i]] for i in range(3)]
    preencher_grid(grid_init, nome_init)
    resolver()

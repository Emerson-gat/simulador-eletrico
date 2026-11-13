import tkinter as tk
from tkinter import ttk
import numpy as np

from modulo_lei_ohm import abrir_modulo_lei_ohm
from modulo_potencia import abrir_modulo_potencia
from modulo_consumo import abrir_modulo_consumo
from modulo_sistemas_lineares import abrir_modulo_sistemas_lineares
from modulo_jacobi import abrir_modulo_jacobi, executar_jacobi
from modulo_gauss_seidel import abrir_modulo_gauss_seidel, executar_gauss_seidel
from modo_professor import abrir_modo_professor
from estado_sistema import obter_sistema, formatar_equacoes, analisar_criterios_convergencia


def abrir_tela_academica():
    janela = tk.Toplevel()
    janela.title("Laboratório Acadêmico")
    janela.state("zoomed")
    janela.configure(bg="#081421")

    # CABEÇALHO
    tk.Label(
        janela,
        text="🎓 LABORATÓRIO ACADÊMICO",
        bg="#081421",
        fg="white",
        font=("Arial", 24, "bold")
    ).pack(pady=15)

    tk.Label(
        janela,
        text="Matemática • Eletrotécnica • Métodos Computacionais • Ensino",
        bg="#081421",
        fg="#00FF88",
        font=("Arial", 12, "bold")
    ).pack(pady=5)

    tk.Button(
        janela,
        text="⬅ Voltar ao Simulador",
        bg="#FF9800",
        fg="white",
        font=("Arial", 11, "bold"),
        command=janela.destroy
    ).pack(pady=10)

    # CONTAINER PRINCIPAL
    principal = tk.Frame(janela, bg="#081421")
    principal.pack(fill="both", expand=True, padx=10, pady=10)

    # MENU ESQUERDO
    menu = tk.Frame(principal, bg="#112233", width=300)
    menu.pack(side="left", fill="y", padx=10)
    menu.pack_propagate(False)

    tk.Label(
        menu,
        text="MÓDULOS",
        bg="#112233",
        fg="white",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    botoes = [
        "⚡ Lei de Ohm",
        "🔥 Potência Elétrica",
        "🏠 Consumo de Energia",
        "🔗 Resistores em Série",
        "🔀 Resistores em Paralelo",
        "📈 Função Afim",
        "🧮 Matrizes",
        "📐 Sistemas Lineares",
        "🔄 Método de Jacobi",
        "🔄 Método Gauss-Seidel",
        "📊 Relatório de Convergência",
        "🎯 Desafios",
        "👨‍🏫 Modo Professor",
        "👨‍🎓 Modo Aluno"
    ]

    # ÁREA CENTRAL
    centro = tk.Frame(principal, bg="#0B1826")
    centro.pack(side="left", fill="both", expand=True)

    texto = tk.Text(
        centro,
        bg="#000000",
        fg="#00FF88",
        insertbackground="white",
        font=("Consolas", 12)
    )

    scrollbar = tk.Scrollbar(centro, command=texto.yview)
    texto.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    texto.pack(fill="both", expand=True)

    def gerar_relatorio_sincronizado():
        A, b, tol, max_iter, nome = obter_sistema()
        dominante, sassenfeld_ok, beta_max = analisar_criterios_convergencia(A)
        x_exato = np.linalg.solve(A, b)

        sol_jac, it_jac, err_jac, tempo_jac, hist_jac, conv_jac = executar_jacobi(
            A, b, tol=tol, max_iter=max_iter
        )
        sol_gs, it_gs, err_gs, tempo_gs, hist_gs, conv_gs = executar_gauss_seidel(
            A, b, tol=tol, max_iter=max_iter
        )

        linhas = [
            "=" * 75,
            f"ANÁLISE COMPUTACIONAL DE SISTEMAS LINEARES | {nome.upper()}",
            "=" * 75,
            "\n1. REPRESENTAÇÃO MATRICIAL (Ax = b):",
            formatar_equacoes(A, b),
            f"\nMatriz A:\n{A}\n",
            f"Vetor b: {b}",
            f"Solução Exata: x = {x_exato.item(0):.4f}, y = {x_exato.item(1):.4f}, z = {x_exato.item(2):.4f}",
            f"Diagonal Dominante: {'SIM' if dominante else 'NÃO'} | Sassenfeld (β={beta_max:.4f}): {'ATENDE' if sassenfeld_ok else 'NÃO ATENDE'}",
            "\n" + "-" * 75,
            "2A. MÉTODO DE JACOBI (Primeiras 5 iterações):",
            "-" * 75
        ]

        for k, vals, err in hist_jac[:5]:
            linhas.append(
                f"Iteração {k:02d} | x = {vals.item(0):10.4f} | y = {vals.item(1):10.4f} | z = {vals.item(2):10.4f} | Erro = {err:.6f}"
            )

        linhas.extend([
            "\n" + "-" * 75,
            "2B. MÉTODO DE GAUSS-SEIDEL (Primeiras 5 iterações):",
            "-" * 75
        ])

        for k, vals, err in hist_gs[:5]:
            linhas.append(
                f"Iteração {k:02d} | x = {vals.item(0):10.4f} | y = {vals.item(1):10.4f} | z = {vals.item(2):10.4f} | Erro = {err:.6f}"
            )

        linhas.extend([
            "\n" + "=" * 75,
            "3. COMPARAÇÃO DE VELOCIDADE E ERRO (JACOBI vs GAUSS-SEIDEL)",
            "=" * 75,
            f"{'MÉTODO':<15} | {'STATUS':<12} | {'ITERAÇÕES':<10} | {'TEMPO (ms)':<12} | {'ERRO FINAL':<15}",
            "-" * 75,
            f"{'Jacobi':<15} | {'Convergiu' if conv_jac else 'Divergiu':<12} | {it_jac:<10} | {tempo_jac:<12.4f} | {err_jac:<15.4e}",
            f"{'Gauss-Seidel':<15} | {'Convergiu' if conv_gs else 'Divergiu':<12} | {it_gs:<10} | {tempo_gs:<12.4f} | {err_gs:<15.4e}",
            "-" * 75,
            "CONCLUSÃO TÉCNICA:",
            "- Diferença Algorítmica: Jacobi usa apenas valores da iteração anterior (k),",
            "  enquanto Gauss-Seidel usa imediatamente os valores atualizados na mesma iteração."
        ])

        if conv_jac and conv_gs:
            linhas.append("- Convergência: Ambos convergiram para a solução exata, com Gauss-Seidel")
            linhas.append("  exigindo menos iterações graças ao reaproveitamento imediato das variáveis.")
        else:
            linhas.append("- Convergência: Como a matriz A não atende aos critérios de dominância diagonal")
            linhas.append("  nem ao Critério de Sassenfeld, os métodos iterativos divergem nesta ordem.")

        linhas.append("=" * 75)
        return "\n".join(linhas)

    def abrir_modulo(nome):
        if nome == "⚡ Lei de Ohm":
            abrir_modulo_lei_ohm()
            return
        if nome == "🔥 Potência Elétrica":
            abrir_modulo_potencia()
            return
        if nome == "🏠 Consumo de Energia":
            abrir_modulo_consumo()
            return
        if nome == "📐 Sistemas Lineares":
            abrir_modulo_sistemas_lineares()
            return
        if nome == "🔄 Método de Jacobi":
            abrir_modulo_jacobi()
            return
        if nome == "🔄 Método Gauss-Seidel":
            abrir_modulo_gauss_seidel()
            return
        if nome == "👨‍🏫 Modo Professor":
            abrir_modo_professor()
            return

        texto.delete("1.0", tk.END)

        if nome == "🧮 Matrizes":
            A, b, _, _, nome_sis = obter_sistema()
            painel_matriz = (
                "======================================\n"
                "MATRIZES (FORMA Ax = b)\n"
                "======================================\n"
                f"Sistema Ativo: {nome_sis}\n\n"
                f"Equações:\n{formatar_equacoes(A, b)}\n\n"
                f"Matriz A:\n{A}\n\n"
                f"Vetor b:\n{b}\n"
            )
            texto.insert(tk.END, painel_matriz)
            return

        if nome == "📊 Relatório de Convergência":
            texto.insert(tk.END, gerar_relatorio_sincronizado())
            return

        conteudo = {
            "📈 Função Afim": "======================================\nFUNÇÃO AFIM\n======================================\nf(x) = ax + b\nExemplo: f(x) = 2x + 3 -> f(5) = 13\n",
            "🎯 Desafios": "======================================\nDESAFIOS\n======================================\n1. Calcular corrente de chuveiro 5500W.\n2. Escolher disjuntor e bitola.\n3. Simular instalação.\n",
            "👨‍🎓 Modo Aluno": "======================================\nMODO ALUNO\n======================================\n✓ Resolver atividades\n✓ Ganhar pontuação\n✓ Acompanhar evolução\n"
        }

        texto.insert(tk.END, conteudo.get(nome, f"Módulo {nome} em construção."))

    # CRIAR BOTÕES
    for nome in botoes:
        tk.Button(
            menu,
            text=nome,
            command=lambda n=nome: abrir_modulo(n),
            bg="#00C853",
            fg="white",
            font=("Arial", 11, "bold"),
            width=25
        ).pack(pady=3)

    abrir_modulo("📊 Relatório de Convergência")

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sys

sys.path.append(r"C:\simulador_eletrico")

from constantes import *
from calculos import calcular_corrente, calcular_potencia
from simulador_canvas import desenhar_circuito
from cenarios_reais import DESAFIOS
from biblioteca_equipamentos import equipamentos
from instalacoes_reais import relatorio_instalacao
from explicacoes_didaticas import gerar_aula
from tela_academica import abrir_tela_academica


def abrir_interface():
    janela = tk.Tk()
    janela.title("⚡ Simulador Elétrico Didático")
    janela.state("zoomed")
    janela.resizable(True, True)
    janela.configure(bg=COR_FUNDO)

    # =====================================
    # CABEÇALHO COMPACTO
    # =====================================
    topo = tk.Frame(janela, bg=COR_FUNDO)
    topo.pack(fill="x", pady=(10, 5))

    tk.Label(
        topo,
        text="⚡ Simulador Elétrico",
        bg=COR_FUNDO,
        fg="white",
        font=("Arial", 22, "bold")
    ).pack()

    cenario_label = tk.Label(
        topo,
        text="",
        bg=COR_FUNDO,
        fg="yellow",
        font=("Arial", 10, "bold")
    )
    cenario_label.pack(pady=2)

    # =====================================
    # PAINEL DE ENTRADAS HORIZONTAL
    # =====================================
    painel = tk.Frame(janela, bg=COR_CARD, pady=10, padx=15)
    painel.pack(pady=5, padx=20, fill="x")

    entradas_box = tk.Frame(painel, bg=COR_CARD)
    entradas_box.pack()

    # Coluna 1: Equipamento
    col1 = tk.Frame(entradas_box, bg=COR_CARD)
    col1.pack(side="left", padx=15)
    tk.Label(col1, text="Equipamento Real", bg=COR_CARD, fg="cyan", font=("Arial", 10, "bold")).pack()
    lista_equipamentos = ttk.Combobox(col1, values=list(equipamentos.keys()), width=35)
    lista_equipamentos.pack(pady=4)

    # Coluna 2: Tensão
    col2 = tk.Frame(entradas_box, bg=COR_CARD)
    col2.pack(side="left", padx=15)
    tk.Label(col2, text="Tensão (V)", bg=COR_CARD, fg="white", font=("Arial", 10, "bold")).pack()
    entrada_tensao = tk.Entry(col2, width=18, justify="center", font=("Consolas", 11))
    entrada_tensao.pack(pady=4)

    # Coluna 3: Resistência
    col3 = tk.Frame(entradas_box, bg=COR_CARD)
    col3.pack(side="left", padx=15)
    tk.Label(col3, text="Resistência (Ω)", bg=COR_CARD, fg="white", font=("Arial", 10, "bold")).pack()
    entrada_resistencia = tk.Entry(col3, width=18, justify="center", font=("Consolas", 11))
    entrada_resistencia.pack(pady=4)

    # =====================================
    # BARRA DE BOTÕES FIXA
    # =====================================
    barra_botoes = tk.Frame(janela, bg=COR_FUNDO)
    barra_botoes.pack(pady=8)

    def carregar_equipamento(event=None):
        nome = lista_equipamentos.get()
        if nome not in equipamentos:
            return
        equipamento = equipamentos[nome]
        tensao = equipamento["tensao"]
        potencia = equipamento["potencia"]
        resistencia = (tensao ** 2) / potencia

        entrada_tensao.delete(0, tk.END)
        entrada_tensao.insert(0, str(tensao))

        entrada_resistencia.delete(0, tk.END)
        entrada_resistencia.insert(0, f"{resistencia:.2f}")

    lista_equipamentos.bind("<<ComboboxSelected>>", carregar_equipamento)

    indice_desafio = 0

    def carregar_desafio():
        desafio = DESAFIOS[indice_desafio]
        cenario_label.config(
            text=f"DESAFIO: {desafio['titulo']} — {desafio['objetivo']}"
        )

    carregar_desafio()

    # Controle de escala do desenho usando dicionário (seguro contra cortes)
    estado_zoom = {"escala": 1.0}

    def aplicar_zoom(fator, x=290, y=160):
        nova_escala = estado_zoom["escala"] * fator
        if 0.4 <= nova_escala <= 3.0:
            canvas.scale("all", x, y, fator, fator)
            estado_zoom["escala"] = nova_escala
            lbl_zoom.config(text=f"Zoom: {int(round(nova_escala * 100))}%")

    def resetar_zoom():
        if canvas.find_all():
            simular()

    def limpar_tela():
        lista_equipamentos.set("")
        entrada_tensao.delete(0, tk.END)
        entrada_resistencia.delete(0, tk.END)
        canvas.delete("all")
        estado_zoom["escala"] = 1.0
        lbl_zoom.config(text="Zoom: 100%")
        texto_resultado.config(state="normal")
        texto_resultado.delete("1.0", tk.END)
        texto_resultado.insert(tk.END, "Tela limpa. Escolha um equipamento ou digite os valores acima e clique em SIMULAR.")
        texto_resultado.config(state="disabled")

    def simular(event=None):
        try:
            v_str = entrada_tensao.get().replace(",", ".").strip()
            r_str = entrada_resistencia.get().replace(",", ".").strip()

            if not v_str or not r_str:
                messagebox.showwarning("Atenção", "Preencha a Tensão (V) e a Resistência (Ω).")
                return

            tensao = float(v_str)
            resistencia = float(r_str)

            if resistencia == 0:
                messagebox.showerror("Erro", "A resistência não pode ser zero!")
                return

            corrente = calcular_corrente(tensao, resistencia)
            potencia = calcular_potencia(tensao, corrente)
            relatorio = relatorio_instalacao(tensao, corrente, potencia)
            equipamento_nome = lista_equipamentos.get()
            explicacao = gerar_aula(equipamento_nome, tensao, resistencia, corrente, potencia)

            saida = (
                f"⚡ Corrente: {relatorio['corrente']} A\n"
                f"🔥 Potência: {relatorio['potencia']} W\n\n"
                f"🔌 Disjuntor: {relatorio['disjuntor']}\n"
                f"🧵 Bitola: {relatorio['bitola']}\n"
                f"📊 Risco: {relatorio['risco']}\n\n"
                f"⚙ {relatorio['mensagem']}\n\n"
                f"🏠 Consumo/Hora: {relatorio['consumo_hora']} kWh\n"
                f"📅 Consumo/Mês: {relatorio['consumo_mensal']} kWh\n"
                f"💰 Custo Estimado: R$ {relatorio['custo_estimado']}\n\n"
                f"{explicacao}"
            )

            texto_resultado.config(state="normal")
            texto_resultado.delete("1.0", tk.END)
            texto_resultado.insert(tk.END, saida)
            texto_resultado.config(state="disabled")

            # Redesenha e ajusta a posição inicial do canvas
            canvas.xview_moveto(0)
            canvas.yview_moveto(0)
            desenhar_circuito(canvas, corrente)
            estado_zoom["escala"] = 1.0

            # Auto-ajuste para evitar que a borda direita fique cortada
            bbox = canvas.bbox("all")
            if bbox:
                x1, y1, x2, y2 = bbox
                largura = x2 - x1
                if largura > 550:
                    fator_fit = 540.0 / largura
                    canvas.scale("all", 10, 10, fator_fit, fator_fit)
                    estado_zoom["escala"] = fator_fit

            lbl_zoom.config(text=f"Zoom: {int(round(estado_zoom['escala'] * 100))}%")

        except Exception as erro:
            messagebox.showerror("Erro", f"Verifique os valores digitados.\nDetalhe: {erro}")

    janela.bind("<Return>", simular)

    tk.Button(
        barra_botoes,
        text="⚡ SIMULAR",
        bg=COR_BOTAO,
        fg="white",
        font=("Arial", 12, "bold"),
        padx=18,
        pady=6,
        cursor="hand2",
        command=simular
    ).pack(side="left", padx=8)

    tk.Button(
        barra_botoes,
        text="🔄 LIMPAR / VOLTAR",
        bg="#FF9800",
        fg="white",
        font=("Arial", 11, "bold"),
        padx=14,
        pady=6,
        cursor="hand2",
        command=limpar_tela
    ).pack(side="left", padx=8)

    tk.Button(
        barra_botoes,
        text="📚 LABORATÓRIO ACADÊMICO",
        bg="#2962FF",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=18,
        pady=6,
        cursor="hand2",
        command=abrir_tela_academica
    ).pack(side="left", padx=8)

    # =====================================
    # ÁREA INFERIOR DIVIDIDA (CIRCUITO COM ZOOM + RELATÓRIO)
    # =====================================
    area_inferior = tk.Frame(janela, bg=COR_FUNDO)
    area_inferior.pack(fill="both", expand=True, padx=20, pady=(5, 15))

    # Lado Esquerdo: Circuito + Barra de Zoom
    frame_canvas = tk.Frame(area_inferior, bg=COR_FUNDO)
    frame_canvas.pack(side="left", fill="y", padx=(0, 15))

    barra_zoom = tk.Frame(frame_canvas, bg=COR_FUNDO)
    barra_zoom.pack(fill="x", pady=(0, 5))

    tk.Label(
        barra_zoom,
        text="Visualização do Circuito",
        bg=COR_FUNDO,
        fg="white",
        font=("Arial", 11, "bold")
    ).pack(side="left")

    tk.Button(
        barra_zoom,
        text="➕",
        command=lambda: aplicar_zoom(1.15),
        bg="#1F3A52",
        fg="#00FF88",
        font=("Arial", 9, "bold"),
        width=3,
        cursor="hand2"
    ).pack(side="right", padx=2)

    tk.Button(
        barra_zoom,
        text="Reset",
        command=resetar_zoom,
        bg="#1F3A52",
        fg="white",
        font=("Arial", 8, "bold"),
        padx=6,
        cursor="hand2"
    ).pack(side="right", padx=2)

    tk.Button(
        barra_zoom,
        text="➖",
        command=lambda: aplicar_zoom(0.85),
        bg="#1F3A52",
        fg="#00FF88",
        font=("Arial", 9, "bold"),
        width=3,
        cursor="hand2"
    ).pack(side="right", padx=2)

    lbl_zoom = tk.Label(
        barra_zoom,
        text="Zoom: 100%",
        bg=COR_FUNDO,
        fg="#00FF88",
        font=("Consolas", 9, "bold")
    )
    lbl_zoom.pack(side="right", padx=8)

    canvas = tk.Canvas(
        frame_canvas,
        width=580,
        height=320,
        bg="black",
        highlightthickness=1,
        highlightbackground="#334455",
        cursor="fleur"
    )
    canvas.pack()

    tk.Label(
        frame_canvas,
                text="💡 Dica: Use a roda do mouse para dar zoom ou clique e arraste para mover o desenho.",
        bg=COR_FUNDO,
        fg="#8899AA",
        font=("Arial", 8, "italic")
    ).pack(pady=(4, 0))

    # Eventos de Zoom (Roda do Mouse) e Arraste (Clique e Mova)
    canvas.bind("<MouseWheel>", lambda e: aplicar_zoom(1.1 if e.delta > 0 else 0.9, e.x, e.y))
    canvas.bind("<ButtonPress-1>", lambda e: canvas.scan_mark(e.x, e.y))
    canvas.bind("<B1-Motion>", lambda e: canvas.scan_dragto(e.x, e.y, gain=1))

    # Lado Direito: Relatório com Barra de Rolagem
    frame_texto = tk.Frame(area_inferior, bg=COR_FUNDO)
    frame_texto.pack(side="left", fill="both", expand=True)

    tk.Label(frame_texto, text="Diagnóstico Técnico e Didático", bg=COR_FUNDO, fg="white", font=("Arial", 11, "bold")).pack(pady=(0, 5))

    box_scroll = tk.Frame(frame_texto, bg=COR_CARD)
    box_scroll.pack(fill="both", expand=True)

    scrollbar = tk.Scrollbar(box_scroll)
    scrollbar.pack(side="right", fill="y")

    texto_resultado = tk.Text(
        box_scroll,
        bg=COR_CARD,
        fg=COR_RESULTADO,
        font=("Consolas", 12, "bold"),
        wrap="word",
        padx=12,
        pady=12,
        yscrollcommand=scrollbar.set
    )
    texto_resultado.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=texto_resultado.yview)

    texto_resultado.insert(tk.END, "Selecione um equipamento acima e clique em ⚡ SIMULAR para ver o diagnóstico.")
    texto_resultado.config(state="disabled")

    janela.mainloop()


if __name__ == "__main__":
    abrir_interface()


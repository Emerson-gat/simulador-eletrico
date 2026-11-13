import streamlit as st
import numpy as np
import requests
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from calculos import calcular_corrente, calcular_potencia
from biblioteca_equipamentos import equipamentos
from instalacoes_reais import relatorio_instalacao
from explicacoes_didaticas import gerar_aula
from atividade_pratica_uninter import executar_jacobi
from atividade_pratica_uninter import executar_gauss_seidel
from estado_sistema import formatar_equacoes, analisar_criterios_convergencia

st.set_page_config(
    page_title="Simulador Eletrico & Laboratorio Academico",
    page_icon="⚡",
    layout="wide"
)


def autenticar_firebase(email, senha, api_key, modo="login"):
    endpoint = "signInWithPassword" if modo == "login" else "signUp"
    base_auth = "https://googleapis.com"
    url = f"{base_auth}:{endpoint}?key={api_key}"
    payload = {"email": email, "password": senha, "returnSecureToken": True}
    resp = requests.post(url, json=payload, timeout=10)
    return resp.status_code == 200, resp.json()


def salvar_log_firestore(project_id, id_token, usuario, dados_simulacao):
    if not project_id or not id_token:
        return False
    base_db = "https://googleapis.com"
    url = f"{base_db}/{project_id}/databases/(default)/documents/simulacoes"
    headers = {"Authorization": f"Bearer {id_token}"}
    doc = {
        "fields": {
            "usuario": {"stringValue": usuario},
            "equipamento": {"stringValue": str(dados_simulacao.get("equipamento", ""))},
            "corrente": {"doubleValue": float(dados_simulacao.get("corrente", 0))},
            "potencia": {"doubleValue": float(dados_simulacao.get("potencia", 0))}
        }
    }
    try:
        r = requests.post(url, json=doc, headers=headers, timeout=5)
        return r.status_code in (200, 201)
    except Exception:
        return False


if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.usuario = ""
    st.session_state.id_token = ""
    st.session_state.project_id = ""
    st.session_state.modo_demo = False

if not st.session_state.logado:
    col_esq, col_centro, col_dir = st.columns((1, 1.4, 1))
    with col_centro:
        st.markdown("<h1 style='text-align: center;'>⚡ Simulador Elétrico Didático</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #00FF88;'>Acesso ao Ambiente Computacional e Laboratório Acadêmico</p>", unsafe_allow_html=True)

        with st.container(border=True):
            aba_login, aba_cadastro, aba_config = st.tabs(("🔐 Entrar", "📝 Criar Conta", "⚙️ Config Firebase"))

            with aba_config:
                st.info("Cole os dados do seu projeto Firebase para ativar login e Firestore.")
                default_key = st.secrets["FIREBASE_API_KEY"] if "FIREBASE_API_KEY" in st.secrets else ""
                default_proj = st.secrets["FIREBASE_PROJECT_ID"] if "FIREBASE_PROJECT_ID" in st.secrets else ""
                api_key_input = st.text_input("Firebase Web API Key", value=default_key, type="password")
                project_id_input = st.text_input("Firebase Project ID (para Firestore)", value=default_proj)

            with aba_login:
                email_login = st.text_input("E-mail", key="email_l")
                senha_login = st.text_input("Senha", type="password", key="senha_l")

                if st.button("Entrar com Firebase", type="primary", use_container_width=True):
                    if not api_key_input:
                        st.warning("Informe a Web API Key na aba 'Config Firebase' ou use o Acesso Rápido abaixo.")
                    elif not email_login or not senha_login:
                        st.warning("Preencha e-mail e senha.")
                    else:
                        ok, dados = autenticar_firebase(email_login, senha_login, api_key_input, modo="login")
                        if ok:
                            st.session_state.logado = True
                            st.session_state.usuario = dados.get("email", email_login)
                            st.session_state.id_token = dados.get("idToken", "")
                            st.session_state.project_id = project_id_input
                            st.rerun()
                        else:
                            erro_msg = dados.get("error", {}).get("message", "Falha na autenticação.")
                            st.error(f"Erro Firebase: {erro_msg}")

            with aba_cadastro:
                email_cad = st.text_input("Novo E-mail", key="email_c")
                senha_cad = st.text_input("Nova Senha (mín. 6 caracteres)", type="password", key="senha_c")
                if st.button("Cadastrar no Firebase", use_container_width=True):
                    if not api_key_input:
                        st.warning("Informe a Web API Key na aba 'Config Firebase'.")
                    else:
                        ok, dados = autenticar_firebase(email_cad, senha_cad, api_key_input, modo="signup")
                        if ok:
                            st.success("Conta criada! Faça login na aba Entrar.")
                        else:
                            erro_msg = dados.get("error", {}).get("message", "Erro ao cadastrar.")
                            st.error(f"Erro Firebase: {erro_msg}")

            st.divider()
            if st.button("🚀 Entrar em Modo Apresentação (Sem Firebase)", use_container_width=True):
                st.session_state.logado = True
                st.session_state.usuario = "Apresentação Acadêmica"
                st.session_state.modo_demo = True
                st.rerun()
    st.stop()

with st.sidebar:
    st.markdown("## ⚡ Painel do Usuário")
    st.success(f"Conectado: **{st.session_state.usuario}**")
    if st.session_state.project_id:
        st.caption(f"Firestore Ativo: `{st.session_state.project_id}`")

    pagina = st.radio(
        "Navegação:",
        ("🔌 Simulador Elétrico", "🎓 Laboratório Acadêmico (Sistemas Lineares)")
    )

    st.divider()
    if st.button("⬅ Sair / Trocar Conta", use_container_width=True):
        st.session_state.logado = False
        st.session_state.id_token = ""
        st.rerun()

if pagina == "🔌 Simulador Elétrico":
    st.title("⚡ Simulador Elétrico Didático")
    st.caption("Análise de circuitos, dimensionamento de disjuntores, bitolas e consumo.")

    col1, col2, col3 = st.columns((2, 1, 1))
    with col1:
        lista_nomes = list(("-- Personalizado --",)) + list(equipamentos.keys())
        equip_escolhido = st.selectbox("Equipamento Real:", lista_nomes)

    tensao_padrao = 127.0
    resistencia_padrao = 53.76
    if equip_escolhido != "-- Personalizado --":
        eq = equipamentos.get(equip_escolhido)
        tensao_padrao = float(eq.get("tensao"))
        resistencia_padrao = round((tensao_padrao ** 2) / float(eq.get("potencia")), 2)

    with col2:
        tensao = st.number_input("Tensão (V):", min_value=1.0, value=tensao_padrao, step=1.0)
    with col3:
        resistencia = st.number_input("Resistência (Ω):", min_value=0.01, value=resistencia_padrao, step=0.5)

    if st.button("⚡ SIMULAR CIRCUITO", type="primary", use_container_width=True):
        corrente = calcular_corrente(tensao, resistencia)
        potencia = calcular_potencia(tensao, corrente)
        rel = relatorio_instalacao(tensao, corrente, potencia)
        aula = gerar_aula(equip_escolhido, tensao, resistencia, corrente, potencia)

        if not st.session_state.modo_demo and st.session_state.project_id:
            salvou = salvar_log_firestore(
                st.session_state.project_id,
                st.session_state.id_token,
                st.session_state.usuario,
                {"equipamento": equip_escolhido, "corrente": corrente, "potencia": potencia}
            )
            if salvou:
                st.toast("Simulação salva no Firestore!", icon="☁️")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Corrente (I)", f"{rel.get('corrente')} A")
        m2.metric("Potência (P)", f"{rel.get('potencia')} W")
        m3.metric("Disjuntor / Bitola", f"{rel.get('disjuntor')} | {rel.get('bitola')}")
        m4.metric("Custo Mensal Est.", f"R$ {rel.get('custo_estimado')}")

        st.divider()
        c_esq, c_dir = st.columns((1.1, 1))

        with c_esq:
            st.subheader("Visualização do Circuito")
            cor_fluxo = "#00FF88" if corrente < 10 else ("#FFAA00" if corrente < 20 else "#FF3333")
            svg_circuito = f"""
            <div style="background-color:#000000; padding:20px; border-radius:10px; border:1px solid #334455; text-align:center;">
                <h4 style="color:white; margin-bottom:15px;">SIMULAÇÃO ELÉTRICA</h4>
                <svg width="100%" height="220" viewBox="0 0 560 220">
                    <polyline points="90,70 210,70" fill="none" stroke="{cor_fluxo}" stroke-width="4"/>
                    <polyline points="330,70 460,70" fill="none" stroke="{cor_fluxo}" stroke-width="4"/>
                    <polyline points="485,95 485,170 65,170 65,95" fill="none" stroke="{cor_fluxo}" stroke-width="4"/>
                    <text x="65" y="67" fill="white" font-size="11" text-anchor="middle" font-weight="bold">FONTE</text>
                    <text x="65" y="84" fill="#00FF88" font-size="12" text-anchor="middle" font-weight="bold">{tensao:g} V</text>
                    <text x="270" y="75" fill="white" font-size="13" text-anchor="middle" font-weight="bold">CARGA ({resistencia:g}Ω)</text>
                    <text x="485" y="68" fill="white" font-size="13" text-anchor="middle" font-weight="bold">A</text>
                    <text x="485" y="84" fill="{cor_fluxo}" font-size="11" text-anchor="middle" font-weight="bold">{corrente:.2f}A</text>
                    <text x="280" y="205" fill="{cor_fluxo}" font-size="15" text-anchor="middle" font-weight="bold">
                                            {corrente:.2f} A — RISCO {rel.get('risco')}
                    </text>
                </svg>
            </div>
            """
            st.markdown(svg_circuito, unsafe_allow_html=True)

        with c_dir:
            st.subheader("Diagnóstico Técnico e Didático")
            st.info(f"**Status do Circuito:** {rel.get('mensagem')}")
            st.code(
                f"Equipamento : {equip_escolhido}\n"
                f"Consumo/Hora: {rel.get('consumo_hora')} kWh\n"
                f"Consumo/Mês : {rel.get('consumo_mensal')} kWh\n\n"
                f"{aula}",
                language="text"
            )

elif pagina == "🎓 Laboratório Acadêmico (Sistemas Lineares)":
    st.title("🎓 Laboratório Acadêmico: Sistemas Lineares")
    st.caption("Comparação computacional entre o Método de Jacobi e o Método de Gauss-Seidel (Ax = b).")

    preset = st.selectbox(
        "Carregar Sistema Predefinido:",
        ("Sistema Padrão (Atividade Prática)", "Sistema Diagonalmente Dominante (Convergente)", "Malhas Elétricas (3 Malhas)")
    )

    if preset == "Sistema Padrão (Atividade Prática)":
        mat_default = ((1.0, 1.0, 1.0, 1.0), (4.0, 4.0, 2.0, 2.0), (2.0, 1.0, -1.0, 0.0))
    elif preset == "Sistema Diagonalmente Dominante (Convergente)":
        mat_default = ((4.0, -1.0, 1.0, 7.0), (1.0, 5.0, 1.0, -8.0), (2.0, 3.0, 10.0, 6.0))
    else:
        mat_default = ((10.0, -2.0, -3.0, 12.0), (-2.0, 8.0, -1.0, 0.0), (-3.0, -1.0, 9.0, 5.0))

    st.markdown("#### Matriz Aumentada $[A | b]$:")
    entradas_grid = []
    cols_header = st.columns(4)
    for idx, h in enumerate(("x", "y", "z", "b")):
        cols_header.pop(0).markdown(f"**{h}**")

    for i in range(3):
        cols = st.columns(4)
        linha_vals = []
        linha_padrao = mat_default[i]
        for j in range(4):
            val = cols.pop(0).number_input(f"m_{i}_{j}", value=float(linha_padrao[j]), label_visibility="collapsed", key=f"cell_{preset}_{i}_{j}")
            linha_vals.append(val)
        entradas_grid.append(linha_vals)

    c_p1, c_p2 = st.columns(2)
    tol_web = c_p1.number_input("Tolerância de Erro:", value=0.0001, format="%.6f")
    max_iter_web = c_p2.number_input("Máximo de Iterações:", min_value=5, max_value=500, value=100)

    if st.button("🔄 Resolver e Comparar Métodos", type="primary", use_container_width=True):
        A = np.array([linha[:3] for linha in entradas_grid], dtype=float)
        b = np.array([linha for linha in entradas_grid], dtype=float)

        try:
            t0 = time.perf_counter()
            x_exato = np.linalg.solve(A, b)
            tempo_exato = (time.perf_counter() - t0) * 1000

            dominante, sassenfeld_ok, beta_max = analisar_criterios_convergencia(A)
            x_jac, it_jac, err_jac, tempo_jac, hist_jac, conv_jac = executar_jacobi(A, b, tol=tol_web, max_iter=int(max_iter_web))
            x_gs, it_gs, err_gs, tempo_gs, hist_gs, conv_gs = executar_gauss_seidel(A, b, tol=tol_web, max_iter=int(max_iter_web))

            st.subheader("1. Diagnóstico Prévio e Solução Analítica")
            d1, d2, d3 = st.columns(3)
            d1.metric("Diagonal Dominante", "SIM" if dominante else "NÃO")
            d2.metric("Critério de Sassenfeld", f"{'ATENDE' if sassenfeld_ok else 'NÃO ATENDE'} (β={beta_max:.2f})")
            d3.metric("Solução Exata (NumPy)", f"x={x_exato.item(0):.2f}, y={x_exato.item(1):.2f}, z={x_exato.item(2):.2f}")

            st.subheader("2. Comparativo de Velocidade e Erro")
            tabela_comp = {
                "Método": ("Jacobi", "Gauss-Seidel", "Exato (NumPy)"),
                "Status": ("Convergiu" if conv_jac else "Divergiu", "Convergiu" if conv_gs else "Divergiu", "Direto"),
                "Iterações": (str(it_jac), str(it_gs), "-"),
                "Tempo (ms)": (f"{tempo_jac:.4f}", f"{tempo_gs:.4f}", f"{tempo_exato:.4f}"),
                "Erro Final": (f"{err_jac:.4e}", f"{err_gs:.4e}", "0.000000"),
                "Resultado (x, y, z)": (
                    f"({x_jac.item(0):.4f}, {x_jac.item(1):.4f}, {x_jac.item(2):.4f})",
                    f"({x_gs.item(0):.4f}, {x_gs.item(1):.4f}, {x_gs.item(2):.4f})",
                    f"({x_exato.item(0):.4f}, {x_exato.item(1):.4f}, {x_exato.item(2):.4f})"
                )
            }
            st.table(tabela_comp)

            tab_j, tab_g = st.tabs(("📜 Histórico Jacobi", "📜 Histórico Gauss-Seidel"))
            with tab_j:
                for k, vals, err in hist_jac[:20]:
                    st.text(f"Iteração {k:02d} | x = {vals.item(0):10.4f} | y = {vals.item(1):10.4f} | z = {vals.item(2):10.4f} | Erro = {err:.6f}")
            with tab_g:
                for k, vals, err in hist_gs[:20]:
                    st.text(f"Iteração {k:02d} | x = {vals.item(0):10.4f} | y = {vals.item(1):10.4f} | z = {vals.item(2):10.4f} | Erro = {err:.6f}")

        except np.linalg.LinAlgError:
            st.error("A matriz A informada é singular (determinante zero) e não possui solução única.")


# ⚡ Simulador Elétrico Didático & Laboratório de Métodos Computacionais

![Python](https://shields.io)
![Streamlit](https://shields.io)
![Firebase](https://shields.io)
![NumPy](https://shields.io)

> **Aplicação Híbrida (Desktop + Web) que conecta a Engenharia Elétrica à Álgebra Linear e aos Métodos Numéricos Iterativos.**

🔗 **Acesse a Aplicação Online:** [simulador-eletrico-cgusrk75mbyzr3zpqdg6rc.streamlit.app](https://simulador-eletrico-cgusrk75mbyzr3zpqdg6rc.streamlit.app)

---

## 🎯 Sobre o Projeto

Este projeto nasceu da proposta de tornar o estudo de **Matrizes e Sistemas Lineares** visual, intuitivo e conectado à prática da **Eletrotécnica**. Em vez de tratar equações de forma puramente abstrata, a plataforma permite simular circuitos elétricos reais e analisar o comportamento matemático de algoritmos numéricos utilizados na resolução de malhas elétricas e sistemas complexos.

### Principais Funcionalidades

* **🔌 Simulador Elétrico Interativo:**
  * Cálculo de corrente (I), potência (P), consumo energético (kWh) e estimativa de custo mensal.
  * Dimensionamento automático de disjuntores, bitola de condutores e classificação de risco elétrico.
  * Diagrama esquemático dinâmico (Canvas com Zoom/Pan no Desktop e SVG responsivo na Web).
* **🎓 Laboratório Acadêmico (Sistemas Lineares Ax = b):**
  * Implementação completa dos métodos iterativos de **Jacobi** e **Gauss-Seidel**.
  * Diagnóstico prévio automático pelo **Critério das Linhas** (Diagonal Estritamente Dominante) e **Critério de Sassenfeld** (β).
  * Tabela comparativa em tempo real de velocidade (ms), número de iterações, erro iterativo e erro absoluto em relação à solução analítica.
* **🔐 Autenticação e Nuvem (Firebase):**
  * Sistema de login e cadastro de usuários integrado ao **Firebase Authentication**.
  * Registro automático de histórico de simulações no **Cloud Firestore**.

---

## 🏗️ Arquitetura do Sistema

```text
Simulador_Eletrico/
├── app_web.py                  # Interface Web (Streamlit + Firebase Auth/Firestore)
├── main.py                     # Ponto de entrada da versão Desktop
├── interface.py                # Interface Desktop principal com controles de Zoom/Pan
├── tela_academica.py           # Laboratório Acadêmico integrado (Desktop)
├── estado_sistema.py           # Gerenciador de estado sincronizado e critérios de convergência
├── calculos.py                 # Motor de cálculos elétricos (Lei de Ohm e Potência)
├── instalacoes_reais.py        # Regras de dimensionamento (disjuntores, cabos e custos)
├── modulo_jacobi.py            # Algoritmo iterativo de Jacobi (Desktop)
├── modulo_gauss_seidel.py      # Algoritmo iterativo de Gauss-Seidel (Desktop)
└── requirements.txt            # Dependências para deploy em nuvem
```

---

## 🚀 Como Executar Localmente

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Emerson-gat/simulador-eletrico.git
   cd simulador-eletrico
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a versão desejada:**
   * **Versão Web:** `streamlit run app_web.py`
   * **Versão Desktop:** `python main.py`

---

## 👨‍💻 Autor

Desenvolvido por **Emerson Silva** — Unindo eletricidade, computação científica e desenvolvimento de software.
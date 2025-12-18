import streamlit as st

# Configuração da página principal
st.set_page_config(
    page_title="Sonic Py-tagoras: Acústica Musical",
    page_icon="🎵",
    layout="wide"
)

# --- Cabeçalho com Imagem (Opcional, se quiser adicionar depois) ---
# st.image("https://placeholder.com/banner.jpg", use_column_width=True)

st.title("🎵 Sonic Py-tagoras")
st.subheader("Uma investigação interativa sobre a física, a matemática e as 'mentiras' da música.")

# --- Introdução ---
st.markdown("""
### Bem-vindo ao Laboratório de Acústica

Você sabia que o piano moderno é, por definição, um instrumento desafinado?

Este projeto nasceu de uma dúvida fundamental: por que a matemática da música parece simples (dobrar frequências, triplicar frequências), mas quando tentamos aplicar isso na prática, os números não fecham?

A música ocidental é construída sobre um "bug" matemático conhecido como **Coma Pitagórico**. Durante séculos, músicos, físicos e matemáticos brigaram sobre como lidar com esse erro. A solução que adotamos hoje (o Temperamento Igual) é um compromisso brilhante de engenharia, mas tem um custo sonoro.

Use o menu à esquerda para explorar as ferramentas que desenvolvemos para visualizar e ouvir esse fenômeno.
""")

st.divider()

# --- Guia das Ferramentas (Cards usando colunas) ---
st.header("🗺️ Guia das Ferramentas")

col1, col2 = st.columns(2)

with col1:
    st.info("### 1. 🎻 O Coma Pitagórico")
    st.markdown("""
    **O Problema Fundamental.**
    Entenda por que o famoso "Círculo das Quintas" é, na verdade, uma espiral que nunca se fecha.
    * **O que você vai ver:** Um gráfico mostrando como subir por quintas (x1.5) não chega no mesmo lugar que subir por oitavas (x2).
    * **O que você vai ouvir:** A dissonância (batimento) exata desse erro matemático.
    """)

    st.info("### 2. 🎹 Laboratório de Acordes")
    st.markdown("""
    **A Beleza vs. A Praticidade.**
    Compare o som puro da física (Just Intonation) com o som do piano moderno (Temperado).
    * **O que você vai ver:** O quanto a "Terça Maior" do piano moderno é "esticada" e desafinada em relação à física pura.
    * **O que você vai ouvir:** A diferença de textura entre um acorde que soa "liso" (puro) e um que soa "agitado" (temperado).
    """)

with col2:
    st.info("### 3. 🎸 Visualizador de Braço")
    st.markdown("""
    **A Geometria do Erro.**
    Se um luthier construísse um violão usando apenas a matemática pura, onde ficariam os trastes?
    * **O que você vai ver:** Duas cordas paralelas comparando a posição física (em milímetros) dos trastes em cada sistema.
    * **O destaque:** Veja como algumas notas ficariam visivelmente em lugares diferentes no braço do instrumento.
    """)

    st.success("### 4. 🎹 Piano Comparativo (Novo!)")
    st.markdown("""
    **A Experiência Prática.**
    Toque e sinta a diferença em tempo real.
    * **O que é:** Dois pianos de duas oitavas empilhados. O de cima é afinado pela natureza, o de baixo pela engenharia moderna.
    * **Como usar:** Use o teclado do seu computador (Z-M para graves, Q-I para agudos) para tocar os dois simultaneamente e sentir as diferenças harmônicas.
    """)

st.divider()

# --- Rodapé ---
st.markdown("""
<div style="text-align: center; color: #888;">
    <small>Desenvolvido como ferramenta de estudo em Python e Streamlit. A matemática não mente, mas a música engana.</small>
</div>
""", unsafe_allow_html=True)

st.sidebar.success("👈 Selecione uma ferramenta no menu para começar.")
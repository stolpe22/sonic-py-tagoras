import streamlit as st

st.set_page_config(
    page_title="Sonic Py-tagoras",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- HEADER COM ESTILO ---
st.title("🎵 Sonic Py-tagoras")
st.subheader("Enciclopédia Interativa de Acústica e Musicologia")

st.markdown("""
> *"A música é o prazer que a mente humana experimenta ao contar sem perceber que está contando."* > — Gottfried Wilhelm Leibniz
""")

st.divider()

# --- INTRODUÇÃO ---
st.markdown("""
### 👋 Bem-vindo ao Laboratório
Este não é apenas um app sobre música. É uma jornada interativa pela **Matemática** e **Física** que tornam a música possível.
Navegue pelo menu lateral seguindo a numeração sugerida para entender a história completa, desde a vibração de uma única corda até a complexidade da afinação moderna.
""")

st.write("") # Espaçamento

# --- GUIA DE NAVEGAÇÃO (GRID) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🧬 1. A Física (O Som)")
    st.info("""
    Entenda a matéria-prima da música.
    
    * **1. Série Harmônica:** O DNA de um timbre e por que notas soam bem juntas.
    * **2. Geometria do Som:** Veja o som desenhando formas de Lissajous em tempo real.
    """)

with col2:
    st.markdown("### 📐 2. A Matemática (O Problema)")
    st.warning("""
    Descubra o "bug" impossível da música.
    
    * **3. Geometria Musical:** Por que o relógio tem 12 horas e a música 12 notas?
    * **4. O Coma Pitagórico:** O erro matemático que quebrou a cabeça dos gregos.
    * **5. Intervalo do Lobo:** Como a história tentou domar esse erro (e falhou).
    """)

with col3:
    st.markdown("### 🎻 3. A Aplicação (A Música)")
    st.success("""
    Da teoria para o seu ouvido.
    
    * **6. Piano Comparativo:** Teste seus ouvidos: Afinação Pura vs. Moderna.
    * **7. Lab. de Acordes:** A química das emoções (Maior, Menor, Diminuto).
    * **8. Luthieria Digital:** A matemática por trás dos trastes do violão.
    """)

# --- CALL TO ACTION FINAL ---
st.divider()
c_game, c_cred = st.columns([2, 1])

with c_game:
    st.markdown("### 🏆 Desafio Final")
    st.markdown("""
    Acha que tem um ouvido absoluto? Depois de estudar os módulos, vá para o **9. Treino Auditivo** e tente vencer a máquina no desafio de microtonalidade.
    """)

with c_cred:
    st.caption("Desenvolvido com Python & Streamlit")
    st.caption("Focado em visualização de dados musicais.")

# Dica visual para o sidebar
st.sidebar.info("👆 Comece pelo módulo 01 para seguir a ordem cronológica do aprendizado!")
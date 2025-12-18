import streamlit as st

st.set_page_config(page_title="Sonic Py-tagoras", page_icon="🎵", layout="wide")

st.title("🎵 Sonic Py-tagoras: Enciclopédia Acústica")
st.markdown("### A Matemática, a Física e a História por trás da Música")

st.info("👈 Navegue pelo menu lateral para acessar os laboratórios.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🟢 Fundamentos")
    st.markdown("""
    * **1. 🎻 O Coma Pitagórico:** O "bug" matemático original.
    * **2. 🎹 Laboratório de Acordes:** A física da consonância.
    * **3. 🎸 Visualizador de Braço:** A geometria dos instrumentos.
    * **4. 🎹 Piano Comparativo:** Toque e sinta a diferença.
    """)

with col2:
    st.markdown("#### 🔵 Tópicos Avançados (Novos!)")
    st.markdown("""
    * **5. 🌀 Geometria do Som (Lissajous):** Veja o som desenhando formas.
    * **6. 🧬 Série Harmônica:** O DNA de um timbre.
    * **7. 🐺 Intervalo do Lobo:** A história das afinações antigas.
    * **8. 👂 Treino Auditivo:** Teste seus ouvidos contra a física.
    * **9. 👽 Microtonalidade:** Músicas de outros mundos (além das 12 notas).
    """)

st.divider()
st.caption("Um projeto educacional interativo.")
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title="Coma Pitagórico", page_icon="🎻", layout="wide")

st.title("🎻 O Coma Pitagórico: O Espiral Infinito")

# --- Teoria ---
with st.expander("📚 Aula Teórica: Por que isso acontece?", expanded=True):
    st.markdown("""
    ### O Mito do Círculo das Quintas
    Na escola de música, aprendemos o "Círculo das Quintas", onde se você subir de Quinta em Quinta (Dó -> Sol -> Ré...), eventualmente você volta ao Dó.
    
    **Na física, isso é mentira.** É um Espiral, não um círculo.
    
    1.  **A Matemática da Oitava (x2):** É perfeita. Dobre a frequência, você tem a mesma nota, mais aguda. $2, 4, 8, 16...$
    2.  **A Matemática da Quinta (x1.5):** É a base da harmonia. Multiplique por 1.5.
    
    O problema é: **Não existe** nenhum número inteiro de vezes que você possa multiplicar 1.5 para chegar num resultado que seja uma potência perfeita de 2.
    
    $$ (1.5)^{12} \\approx 129.74 $$
    $$ 2^7 = 128.00 $$
    
    Essa sobra de **1.74** é o **Coma Pitagórico**. É a "sujeira" que sobra quando tentamos fechar o ciclo.
    """)

# --- Funções de Áudio ---
def gerar_som(frequencia, duracao, sample_rate=44100, tipo="Piano"):
    t = np.linspace(0, duracao, int(sample_rate * duracao), endpoint=False)
    if tipo == "Seno Puro":
        onda = np.sin(2 * np.pi * frequencia * t)
    else:
        # Harmônicos para soar mais natural
        onda = 1.0 * np.sin(2 * np.pi * frequencia * t)
        onda += 0.5 * np.sin(2 * np.pi * (frequencia * 2) * t)
        decaimento = np.exp(-3 * t)
        onda = onda * decaimento
    return onda / np.max(np.abs(onda)) if np.max(np.abs(onda)) > 0 else onda

# --- Interface ---
st.divider()
st.subheader("🛠️ Simulador")

col_params, col_vis = st.columns([1, 2])

with col_params:
    st.markdown("**Parâmetros**")
    frequencia_base = st.number_input("Freq. Base (Hz)", value=100.0, help="Frequência inicial da corda.")
    num_passos = st.slider("Ciclos de Quintas", 1, 12, 12, help="Quantas vezes vamos multiplicar por 1.5")
    timbre = st.selectbox("Timbre", ["Piano", "Seno Puro"])

    # Cálculos
    freq_quintas = frequencia_base * (1.5 ** num_passos)
    num_oitavas = int(np.round(np.log2(freq_quintas / frequencia_base)))
    freq_oitavas = frequencia_base * (2 ** num_oitavas)
    diferenca = freq_quintas - freq_oitavas
    cents = 1200 * np.log2(freq_quintas / freq_oitavas)

with col_vis:
    # Gráfico
    data = pd.DataFrame({
        'Sistema': ['Oitavas Perfeitas (x2)', 'Ciclo de Quintas (x1.5)'],
        'Hz': [freq_oitavas, freq_quintas],
        'Cor': ['#3498db', '#e74c3c']
    })
    
    # Zoom dinâmico
    min_val = min(freq_oitavas, freq_quintas) * 0.99
    max_val = max(freq_oitavas, freq_quintas) * 1.01
    
    chart = alt.Chart(data).mark_bar(size=40).encode(
        x=alt.X('Hz', scale=alt.Scale(domain=[min_val, max_val]), title='Frequência (Hz)'),
        y='Sistema',
        color=alt.Color('Cor', scale=None),
        tooltip=['Sistema', 'Hz']
    ).properties(height=200)
    
    st.altair_chart(chart, use_container_width=True)

# --- Resultados e Áudio ---
col1, col2, col3 = st.columns(3)
col1.metric("Matemática (Quintas)", f"{freq_quintas:.2f} Hz")
col2.metric("Física (Oitavas)", f"{freq_oitavas:.2f} Hz")
col3.metric("Erro (Coma)", f"{diferenca:.2f} Hz", delta=f"{cents:.2f} Cents", delta_color="inverse")

st.write("---")
st.subheader("🔊 Experiência Auditiva")
st.markdown("Se tocarmos essas duas frequências juntas, elas estão próximas demais para serem duas notas diferentes, mas longe demais para serem a mesma nota. O resultado é o **Batimento**.")

if st.button("Tocar a Dissonância (O Som do Coma)"):
    som1 = gerar_som(freq_oitavas, 3, tipo=timbre)
    som2 = gerar_som(freq_quintas, 3, tipo=timbre)
    mix = (som1 + som2) * 0.5
    st.audio(mix, sample_rate=44100)
    st.caption("Ouça a oscilação de volume 'uau-uau-uau'. Isso é a interferência das ondas.")
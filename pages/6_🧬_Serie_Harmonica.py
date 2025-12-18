import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title="Série Harmônica", page_icon="🧬", layout="wide")
st.title("🧬 A Série Harmônica: O DNA do Som")

st.markdown("""
Uma corda nunca vibra sozinha. Ela vibra em partes inteiras (1/2, 1/3, 1/4...).
Essas subdivisões criam notas "fantasmas" chamadas **Harmônicos**.
""")

fundamental = st.number_input("Frequência Fundamental (Hz)", value=65.41, help="C2 (Dó Grave)")

# Gerar harmônicos
harmonicos = []
for i in range(1, 17):
    freq = fundamental * i
    nome_nota = ""
    # Aproximação grosseira da nota
    if i == 1: nome_nota = "Tônica (8va)"
    elif i == 2: nome_nota = "Oitava"
    elif i == 3: nome_nota = "Quinta"
    elif i == 4: nome_nota = "Oitava"
    elif i == 5: nome_nota = "Terça Maior"
    elif i == 7: nome_nota = "Sétima Menor (Pura)"
    
    harmonicos.append({"Ordem": i, "Hz": freq, "Intervalo": nome_nota, "Amplitude": 1/i})

df = pd.DataFrame(harmonicos)

# Gráfico de Espectro
chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('Hz', title='Frequência (Hz)'),
    y=alt.Y('Amplitude', title='Energia Relativa'),
    color=alt.Color('Ordem', legend=None),
    tooltip=['Ordem', 'Hz', 'Intervalo']
).properties(height=300)

st.altair_chart(chart, use_container_width=True)

st.info("💡 Perceba: O acorde Maior (Tônica, Terça, Quinta) aparece naturalmente nos harmônicos 4, 5 e 6.")

# Sintetizador Aditivo
st.subheader("🎹 Sintetizador Aditivo")
st.write("Ligue/Desligue harmônicos para criar timbres.")

col_checks = st.columns(8)
ativos = []
for i in range(16):
    with col_checks[i % 8]:
        if st.checkbox(f"H{i+1}", value=(i < 4)):
            ativos.append(i+1)

if st.button("Tocar Som Resultante"):
    sr = 44100
    t = np.linspace(0, 2.0, int(sr*2.0), endpoint=False)
    wave = np.zeros_like(t)
    for h in ativos:
        # Amplitude cai com a ordem (1/h) para soar natural
        wave += (1/h) * np.sin(2 * np.pi * (fundamental * h) * t)
    
    wave = wave / np.max(np.abs(wave))
    st.audio(wave, sample_rate=sr)
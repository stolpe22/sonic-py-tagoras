import streamlit as st
import numpy as np

st.set_page_config(page_title="Intervalo do Lobo", page_icon="🐺")
st.title("🐺 Arqueologia Musical: O Intervalo do Lobo")

st.markdown("""
Antes de 1700, os instrumentos eram afinados para soar perfeitos em Dó Maior.
Mas se você tentasse tocar em teclas distantes (como Fá#), encontrava o **Lobo**: um intervalo tão desafinado que parecia um uivo.
""")

sistema = st.selectbox("Escolha o Sistema de Afinação:", 
             ["Pitagórico (Antiguidade)", "Mesotônico 1/4 Coma (Renascença)", "Temperamento Igual (Moderno)"])

f_base = 261.63 # C4

if sistema == "Pitagórico (Antiguidade)":
    # Baseado em Quintas 3/2 puras. A Terça maior é horrível (81/64)
    freqs = [1, 256/243, 9/8, 32/27, 81/64, 4/3, 729/512, 3/2, 128/81, 27/16, 16/9, 243/128, 2]
    msg = "As Quintas são perfeitas. As Terças são muito esticadas e brilhantes. O Lobo está entre G# e Eb."
    wolf_pair = (415.30, 622.25) # Exemplo aproximado do lobo G#-Eb
elif sistema == "Mesotônico 1/4 Coma (Renascença)":
    # Terças Maiores (5/4) são puras. As Quintas são encurtadas.
    # O lobo é TERRÍVEL.
    msg = "As Terças são doces e puras (melhor que o piano moderno). Mas tente tocar o Lobo..."
    wolf_pair = (409.0, 638.0) # G# muito grave, Eb muito agudo
else:
    # Moderno
    msg = "Tudo é igualmente 'meio' desafinado. Não há lobos, mas também não há pureza perfeita."
    wolf_pair = (415.30, 622.25) # G# para D# temperado (neutro)

st.info(msg)

col1, col2 = st.columns(2)
with col1:
    st.subheader("🎵 O Acorde 'Bom'")
    st.write("Dó Maior (C-E-G) neste sistema:")
    if st.button("Tocar Dó Maior"):
        # Simplificação para demonstração
        t = np.linspace(0, 2, 44100*2)
        if "Pitagórico" in sistema:
            s = np.sin(2*np.pi*f_base*t) + np.sin(2*np.pi*f_base*1.265*t) + np.sin(2*np.pi*f_base*1.5*t)
        elif "Mesotônico" in sistema:
            s = np.sin(2*np.pi*f_base*t) + np.sin(2*np.pi*f_base*1.25*t) + np.sin(2*np.pi*f_base*1.495*t)
        else:
            s = np.sin(2*np.pi*f_base*t) + np.sin(2*np.pi*f_base*1.2599*t) + np.sin(2*np.pi*f_base*1.498*t)
        st.audio(s/3, sample_rate=44100)

with col2:
    st.subheader("🐺 O Acorde do Lobo")
    st.write("G# para Eb (A 'quinta' proibida):")
    if st.button("Soltar o Lobo"):
        t = np.linspace(0, 3, 44100*3)
        # Tocar as duas frequências do par lobo
        s = np.sin(2*np.pi*wolf_pair[0]*t) + np.sin(2*np.pi*wolf_pair[1]*t)
        st.audio(s/2, sample_rate=44100)
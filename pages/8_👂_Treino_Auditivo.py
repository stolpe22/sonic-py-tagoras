import streamlit as st
import numpy as np
import random

st.set_page_config(page_title="Treino Auditivo", page_icon="👂")
st.title("👂 Desafio: O Afinador Humano")

st.markdown("Você consegue adivinhar a diferença de frequência (Hz) apenas ouvindo o batimento?")

if 'target_diff' not in st.session_state:
    st.session_state.target_diff = random.choice([1, 2, 3, 4, 5, 10])
    st.session_state.base_freq = 440

def play_quiz():
    diff = st.session_state.target_diff
    f1 = st.session_state.base_freq
    f2 = f1 + diff
    
    t = np.linspace(0, 3, 44100*3)
    s = np.sin(2*np.pi*f1*t) + np.sin(2*np.pi*f2*t)
    return s/2

st.write("🔊 Ouça o som abaixo:")
st.audio(play_quiz(), sample_rate=44100)

guess = st.slider("Quantos batimentos por segundo (Hz)?", 0, 15, 0)

if st.button("Verificar Resposta"):
    real = st.session_state.target_diff
    if guess == real:
        st.balloons()
        st.success(f"Correto! A diferença era de {real} Hz.")
    else:
        st.error(f"Errou! A diferença era de {real} Hz. Você chutou {guess}.")
    
    if st.button("Próximo Desafio"):
        st.session_state.target_diff = random.choice([1, 2, 3, 4, 5, 8, 10, 15])
        st.rerun()
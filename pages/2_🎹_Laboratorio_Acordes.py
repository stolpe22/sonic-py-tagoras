import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title="Laboratório de Acordes", page_icon="🎹", layout="wide")
st.title("🎹 Laboratório: A Busca pela Terça Perfeita")

# --- Teoria ---
with st.expander("📚 Aula Teórica: O que é Consonância?", expanded=False):
    st.markdown("""
    ### Por que gostamos de Acordes?
    Quando uma corda vibra, ela não vibra apenas inteira. Ela vibra em metades, terços, quartos, quintos... Esses são os **Harmônicos**.
    
    Um acorde soa "limpo" (consonante) quando as ondas das notas se alinham perfeitamente com esses harmônicos.
    
    * **Acorde Maior Natural (Puro):** Baseado na proporção 4:5:6. As ondas se encontram a cada poucos ciclos. É paz pura.
    * **Acorde Maior Temperado (Piano Moderno):** Para podermos tocar em todos os tons, "esticamos" a Terça Maior. Ela é muito aguda (Sharp).
    
    O Piano moderno é um instrumento **levemente desafinado por design**. Nós nos acostumamos com essa tensão, mas a física não mente.
    """)

# --- Funções ---
def gerar_onda(freq, duracao, sample_rate=44100):
    t = np.linspace(0, duracao, int(sample_rate * duracao), endpoint=False)
    # Onda rica com harmônicos pares e ímpares
    onda = 1.0 * np.sin(2 * np.pi * freq * t) 
    onda += 0.5 * np.sin(2 * np.pi * (freq * 2) * t)
    onda += 0.25 * np.sin(2 * np.pi * (freq * 3) * t)
    return onda * np.exp(-3 * t)

def mixar(freqs):
    mix = np.sum([gerar_onda(f, 2.5) for f in freqs], axis=0)
    return mix / np.max(np.abs(mix))

# --- Controles ---
st.sidebar.header("Configuração")
tipo = st.sidebar.radio("Tipo de Acorde", ["Maior (Major)", "Menor (Minor)"])
root = st.sidebar.number_input("Tônica (Hz)", value=261.63, help="C4 (Dó Central)")

# --- Cálculos ---
if tipo == "Maior (Major)":
    ratios = [1.0, 5/4, 3/2] # Ptolomeu
    semitons = [0, 4, 7]     # 12-TET
    nome_terca = "Terça Maior"
else:
    ratios = [1.0, 6/5, 3/2] # Zarlino
    semitons = [0, 3, 7]     # 12-TET
    nome_terca = "Terça Menor"

freqs_nat = [root * r for r in ratios]
freqs_temp = [root * (2**(s/12)) for s in semitons]

# --- Visualização e Comparação ---
st.divider()
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🔍 Análise Espectral")
    # Calcular Cents da Terça
    terca_nat = freqs_nat[1]
    terca_temp = freqs_temp[1]
    diff_cents = 1200 * np.log2(terca_temp / terca_nat)
    
    st.write(f"Comparando a **{nome_terca}**:")
    
    metric_col_a, metric_col_b = st.columns(2)
    metric_col_a.metric("Frequência Pura", f"{terca_nat:.2f} Hz")
    metric_col_b.metric("Frequência Piano", f"{terca_temp:.2f} Hz", delta=f"{diff_cents:.2f} cents", delta_color="inverse")
    
    if abs(diff_cents) > 10:
        st.warning(f"⚠️ A diferença é de {abs(diff_cents):.1f} cents. O ouvido humano treinado percebe desafinação a partir de 5 cents.")
    else:
        st.success("A diferença é sutil neste intervalo.")

with col2:
    st.subheader("🎧 Teste Cego")
    st.write("Consegue ouvir o 'tremor' no som temperado?")
    
    if st.button("🎵 Tocar: Afinação Pura (Natural)"):
        st.audio(mixar(freqs_nat), sample_rate=44100)
    
    if st.button("🎹 Tocar: Afinação Temperada (Moderna)"):
        st.audio(mixar(freqs_temp), sample_rate=44100)
        
    st.markdown("---")
    if st.button("🔁 Comparação Direta (Puro -> Temperado)"):
        silencio = np.zeros(15000)
        st.audio(np.concatenate([mixar(freqs_nat), silencio, mixar(freqs_temp)]), sample_rate=44100)
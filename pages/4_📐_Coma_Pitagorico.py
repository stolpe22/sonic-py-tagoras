import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="O Coma Pitagórico", page_icon="📐", layout="wide")

# --- CSS (Mesmo estilo da Geometria Musical) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .story-box {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FFC107; /* Amarelo Estilo História */
        margin-bottom: 20px;
    }
    .math-box {
        font-family: 'Courier New', monospace;
        background-color: #111;
        padding: 15px;
        border: 1px solid #333;
        border-radius: 5px;
        color: #4CAF50;
        text-align: center;
    }
    .result-box {
        background-color: #262730;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #444;
        margin-top: 10px;
    }
    .highlight-red { color: #e74c3c; font-weight: bold; }
    .highlight-green { color: #4CAF50; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("📐 O Coma Pitagórico: O Erro Matemático")

# --- INTRODUÇÃO ---
with st.expander("📚 O Paradoxo das Réguas (Contexto)", expanded=True):
    st.markdown("""
    Na página anterior, vimos que a música usa matemática. Mas existe um "bug" no sistema.
    
    Imagine duas réguas para medir o som:
    1.  **Régua Verde (Oitavas):** Multiplica por **2** (Dobro).
    2.  **Régua Azul (Quintas):** Multiplica por **1.5** (Metade mais um pouco).
    
    **O Problema:** Se você tentar alinhar essas duas réguas, elas **nunca** terminam juntas.
    Sempre sobra um pedacinho. Esse pedacinho é o **Coma Pitagórico**.
    """)

st.divider()

# --- INTERFACE PRINCIPAL ---
col_ctrl, col_vis = st.columns([1, 1.5])

with col_ctrl:
    st.subheader("🛠️ O Experimento")
    st.write("Vamos empilhar Quintas e ver se conseguimos chegar num Dó perfeito.")
    
    passos = st.slider("Número de Quintas (Passos):", 1, 12, 12)
    
    # --- CÁLCULOS ---
    freq_base = 100.0
    
    # 1. Caminho das Quintas (Natural / Pitagórico)
    # Fórmula: f * 1.5^n
    freq_natural = freq_base * (1.5 ** passos)
    
    # 2. Caminho Temperado (Moderno)
    # No sistema moderno, "trapaceamos" mudando 1.5 para 1.498 (raiz 12 de 2 ^ 7)
    # 2^(7/12) é a quinta temperada
    freq_temperada = freq_base * ((2**(7/12)) ** passos)

    # 3. Normalização (Trazer para a oitava 100-200Hz para comparar)
    # Natural
    val_nat = freq_natural
    divs_nat = 0
    while val_nat >= freq_base * 2:
        val_nat /= 2
        divs_nat += 1
        
    # Temperada
    val_temp = freq_temperada
    while val_temp >= freq_base * 2:
        val_temp /= 2
    
    # Cálculo do Erro (Cents)
    import math
    cents_error = 1200 * math.log2(val_nat / freq_base) if val_nat > 0 else 0
    
    # EXIBIÇÃO DOS DADOS
    st.markdown("#### 📊 Resultados Matemáticos")
    
    st.markdown(f"""
    <div class="result-box">
        <p><b>1. O Alvo (Dó Perfeito):</b> <br><span class="highlight-green">{freq_base:.2f} Hz</span></p>
        <hr>
        <p><b>2. Sistema Natural (Pitagórico):</b><br>
        Após {passos} passos e {divs_nat} oitavas:<br>
        <span class="highlight-red">{val_nat:.2f} Hz</span> (Erro: +{cents_error:.1f}¢)</p>
        <hr>
        <p><b>3. Sistema Temperado (Moderno):</b><br>
        Após {passos} passos:<br>
        <span class="highlight-green">{val_temp:.2f} Hz</span> (Erro: 0.0¢)</p>
    </div>
    """, unsafe_allow_html=True)
    
    if passos == 12:
        st.error("🚨 ALERTA: No sistema Natural, a conta não fecha! Sobra 1.36 Hz.")
    else:
        st.info("Continue subindo até 12 para ver o problema.")

with col_vis:
    st.subheader("🌀 Visualização do Erro")
    
    # Gráfico Polar (Estilo Radar)
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    
    # Ângulo de uma Quinta Justa (Pura)
    # log2(1.5) da oitava. Em radianos: log2(1.5) * 2pi
    quinta_pura_rad = np.log2(1.5) * 2 * np.pi
    
    # Ângulo de uma Quinta Temperada (Moderna)
    # 7 semitons de 12. Em radianos: (7/12) * 2pi
    quinta_temp_rad = (7/12) * 2 * np.pi
    
    angles_nat = [0]
    radii_nat = [1.5]
    
    angles_temp = [0]
    radii_temp = [1.5] # Um pouco mais para fora para diferenciar
    
    for i in range(passos):
        angles_nat.append(angles_nat[-1] + quinta_pura_rad)
        radii_nat.append(1.5 + (i * 0.1))
        
        angles_temp.append(angles_temp[-1] + quinta_temp_rad)
        # Temperado fica no mesmo raio para comparação visual
    
    # 1. Alvo (Verde) - Sempre no topo
    ax.plot([0, 0], [0, radii_nat[-1]+0.5], color='#4CAF50', linestyle='--', linewidth=2, label='Alvo (Oitava Perfeita)')
    ax.text(0, radii_nat[-1]+0.6, "DÓ\n(Puro)", color='#4CAF50', ha='center', fontweight='bold')
    
    # 2. Caminho Natural (Vermelho/Azul)
    ax.plot(angles_nat, radii_nat, color='#e74c3c', marker='o', linewidth=1.5, label='Pitagórico (Natural)')
    
    # 3. Caminho Temperado (Branco/Cinza - Pontilhado)
    # Só desenha se tivermos mais de 1 passo, para não poluir
    if passos > 1:
        # Plotamos apenas o ponto final para mostrar que ele "certa"
        final_temp_angle = angles_temp[-1] % (2*np.pi)
        # ax.scatter([final_temp_angle], [radii_nat[-1]], color='white', s=100, marker='x', label='Temperado (Moderno)', zorder=10)

    # Lógica de Fechamento
    if passos > 0:
        final_angle_nat = angles_nat[-1] % (2*np.pi)
        
        # Linha Vermelha (Onde chegamos no natural)
        ax.plot([0, final_angle_nat], [0, radii_nat[-1]], color='#e74c3c', linewidth=3)
        
        if passos == 12:
            # Preenche o ERRO
            theta = np.linspace(0, final_angle_nat, 50)
            ax.fill_between(theta, 0, radii_nat[-1], color='#e74c3c', alpha=0.3)
            ax.text(final_angle_nat, radii_nat[-1]+0.2, f"COMA\n(O Excesso)", color='#e74c3c', fontweight='bold')
            
            # Marca o acerto do temperado
            ax.text(0.1, radii_nat[-1]-0.5, "Temperado\nfecha aqui!", color='white', fontsize=8, alpha=0.7)

    ax.set_rticks([])
    ax.set_xticks([])
    ax.grid(False)
    ax.legend(loc='lower right', facecolor='#222', labelcolor='white')
    st.pyplot(fig)

# --- ÁUDIO COMPARATIVO ---
st.divider()
st.subheader("🎹 Comparação Auditiva")
st.write("Ouça a diferença entre a matemática pura (que dá erro) e a moderna (que corrige).")

col_snd1, col_snd2, col_snd3 = st.columns(3)

def gen_tone(f):
    sr = 44100
    t = np.linspace(0, 3, int(sr*3), endpoint=False)
    # Som rico (Dente de Serra suave)
    return 0.5 * (np.sin(2*np.pi*f*t) + 0.25*np.sin(4*np.pi*f*t))

with col_snd1:
    st.markdown("**1. Dó Puro (Alvo)**")
    st.caption("Frequência: 100.00 Hz")
    if st.button("▶️ Tocar Puro"):
        st.audio(gen_tone(100.0), sample_rate=44100)

with col_snd2:
    st.markdown("**2. Dó Pitagórico (Natural)**")
    st.caption(f"Frequência: {val_nat:.2f} Hz (Desafinado)")
    if st.button("▶️ Tocar Pitagórico"):
        st.audio(gen_tone(val_nat), sample_rate=44100)

with col_snd3:
    st.markdown("**3. Dó Temperado (Moderno)**")
    st.caption(f"Frequência: {val_temp:.2f} Hz (Corrigido)")
    if st.button("▶️ Tocar Temperado"):
        st.audio(gen_tone(val_temp), sample_rate=44100)

# --- CAIXA FINAL ---
st.divider()
if st.button("💀 Tocar Puro + Pitagórico (Ouvir o Erro)"):
    mix = gen_tone(100.0) + gen_tone(val_nat)
    st.audio(mix, sample_rate=44100)
    st.error("Ouviu o 'Waw-waw'? Esse é o som do Coma Pitagórico.")
    
if st.button("✅ Tocar Puro + Temperado (Ouvir a Solução)"):
    # Nota: No temperado ideal, seria 100 com 100, sem batimento.
    # Mas na prática, o temperamento muda todas as OUTRAS notas para que a oitava bata.
    # Aqui, a oitava temperada bate perfeitamente com a pura.
    mix = gen_tone(100.0) + gen_tone(val_temp)
    st.audio(mix, sample_rate=44100)
    st.success("Som liso! Sem batimento. A matemática foi 'domada'.")
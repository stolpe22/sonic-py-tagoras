import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="O Coma Pitagórico", page_icon="📐", layout="wide")

# --- CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .concept-card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3498db;
        margin-bottom: 20px;
    }
    .math-comparison {
        background-color: #111;
        padding: 15px;
        border-radius: 8px;
        font-family: monospace;
        color: #eee;
    }
    .highlight-octave { color: #4CAF50; font-weight: bold; } /* Verde */
    .highlight-fifth { color: #3498db; font-weight: bold; } /* Azul */
    .highlight-error { color: #ff4b4b; font-weight: bold; } /* Vermelho */
</style>
""", unsafe_allow_html=True)

st.title("📐 A Falha na Matrix: O Coma Pitagórico")

# --- 1. CONCEITO BÁSICO ---
st.markdown("""
<div class="concept-card">
    <h3>🔍 O Problema das Duas Réguas</h3>
    <p>Imagine que temos duas réguas para medir a música:</p>
    <ul>
        <li><b>Régua das Oitavas (Verde):</b> Multiplica a frequência por <b>2</b>. (Ex: 100 → 200 → 400)</li>
        <li><b>Régua das Quintas (Azul):</b> Multiplica a frequência por <b>1.5</b>. (Ex: 100 → 150 → 225)</li>
    </ul>
    <p><b>A Teoria:</b> Se usarmos a Régua das Quintas 12 vezes, deveríamos chegar no mesmo lugar que a Régua das Oitavas usada 7 vezes.</p>
    <p><b>A Realidade:</b> Veja abaixo o que acontece na prática.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# --- 2. A CORRIDA MATEMÁTICA ---
col_race, col_visual = st.columns([1.5, 1])

with col_race:
    st.subheader("🏃‍♂️ A Corrida das Frequências")
    
    # Slider
    steps = st.slider("Avance as Quintas (Passos):", 0, 12, 12)
    
    freq_base = 100.0
    
    # Caminho das Oitavas (Referência Perfeita)
    # 7 oitavas é o ponto de encontro teórico
    freq_octave_final = freq_base * (2**7) # 12800 Hz
    
    # Caminho das Quintas (Ouvido Humano)
    freq_fifth_current = freq_base * (1.5**steps)
    
    # Dataframe para visualizar a "Subida"
    st.markdown("#### Comparando a Subida Absoluta")
    st.write("Se não fizermos nenhum ajuste, as frequências sobem astronomicamente:")
    
    race_data = {
        "Passos": ["Início", "Meta (Final Teórico)"],
        "Régua Oitavas (x2)": [f"{freq_base:.1f} Hz", f"{freq_octave_final:.1f} Hz"],
        "Régua Quintas (x1.5)": [f"{freq_base:.1f} Hz", f"???" if steps < 12 else f"{freq_fifth_current:.1f} Hz"]
    }
    st.table(pd.DataFrame(race_data))

    if steps == 12:
        diff_abs = freq_fifth_current - freq_octave_final
        st.markdown(f"""
        <div class="math-comparison">
            🏁 <b>RESULTADO FINAL:</b><br>
            Alvo (7 Oitavas): <span class="highlight-octave">{freq_octave_final:.2f} Hz</span><br>
            Você (12 Quintas): <span class="highlight-fifth">{freq_fifth_current:.2f} Hz</span><br>
            <hr>
            Diferença: <span class="highlight-error">+{diff_abs:.2f} Hz</span> (Passou do ponto!)
        </div>
        """, unsafe_allow_html=True)

    # --- 3. A NORMALIZAÇÃO (O "ELEVADOR") ---
    st.markdown("### 📉 Trazendo de volta para comparar")
    st.write("Como 12.000 Hz é muito agudo, vamos dividir o resultado das Quintas por 2 (descer oitavas) até ele voltar para perto do 100 Hz inicial.")
    
    # Lógica de trazer de volta
    val = freq_fifth_current
    divisions = 0
    while val >= freq_base * 2:
        val /= 2
        divisions += 1
        
    st.markdown(f"""
    <div class="math-comparison">
        Frequência lá no alto: {freq_fifth_current:.2f} Hz<br>
        Dividido por 2 ({divisions} vezes): <b>{val:.2f} Hz</b><br>
        <br>
        Comparação na Oitava Inicial:<br>
        Dó Perfeito: <span class="highlight-octave">{freq_base:.2f} Hz</span><br>
        Dó das Quintas: <span class="highlight-error">{val:.2f} Hz</span>
    </div>
    """, unsafe_allow_html=True)
    
    import math
    cents = 1200 * math.log2(val/freq_base) if val > 0 else 0
    if steps == 12:
        st.error(f"O erro é de {cents:.2f} cents. Isso é o Coma Pitagórico.")

with col_visual:
    st.subheader("🌀 Visualização do Erro")
    # Gráfico Polar
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    
    # Lógica Visual
    # Círculo completo = 1 Oitava
    # Quinta = 7/12 do círculo (aprox)
    
    quinta_rad = np.log2(1.5) * 2 * np.pi # O valor exato em radianos dentro de uma oitava
    
    angles = [0]
    radii = [1.5]
    
    for i in range(steps):
        angles.append(angles[-1] + quinta_rad)
        radii.append(1.5 + (i*0.1))
        
    # 1. Alvo (Verde) - Sempre no topo (0 radianos)
    ax.plot([0, 0], [0, radii[-1]+0.5], color='#4CAF50', linestyle='--', linewidth=2, label='Alvo (Oitava Pura)')
    ax.text(0, radii[-1]+0.8, "DÓ\n(Puro)", color='#4CAF50', ha='center', fontweight='bold')
    
    # 2. Caminho (Azul)
    ax.plot(angles, radii, color='#3498db', marker='o', linewidth=1.5, label='Caminho das Quintas')
    
    # 3. Erro (Vermelho)
    if steps > 0:
        # Ângulo normalizado (onde caiu no relógio)
        final_angle = angles[-1] % (2*np.pi)
        
        ax.plot([0, final_angle], [0, radii[-1]], color='#e74c3c', linewidth=2, label='Sua Posição')
        
        if steps == 12:
            # Highlight do Coma
            # 
            theta = np.linspace(0, final_angle, 50)
            ax.fill_between(theta, 0, radii[-1], color='#e74c3c', alpha=0.3)
            ax.text(final_angle, radii[-1]+0.3, f"ERRO\n(+{cents:.1f}¢)", color='#e74c3c', fontweight='bold')

    ax.set_rticks([])
    ax.set_xticks([])
    ax.grid(False)
    ax.legend(loc='lower right', facecolor='#222', labelcolor='white')
    st.pyplot(fig)
    
    st.caption("O gráfico mostra as 'voltas' dadas. Note que a 12ª volta (linha vermelha) passa um pouco da linha verde.")

# --- 4. SONIFICAÇÃO ---
st.divider()
st.subheader("🔊 A Prova Auditiva")
st.write("Abaixo, geramos as duas notas resultantes dessa matemática.")

c1, c2, c3 = st.columns(3)

def gen_tone(f):
    t = np.linspace(0, 3, int(44100*3), endpoint=False)
    return 0.5 * (np.sin(2*np.pi*f*t) + 0.2*np.sin(4*np.pi*f*t))

with c1:
    st.markdown("**1. O Dó Matemático (100 Hz)**")
    if st.button("▶️ Tocar Dó Puro"):
        st.audio(gen_tone(100.0), sample_rate=44100)

with c2:
    st.markdown(f"**2. O Dó das Quintas ({val:.2f} Hz)**")
    if st.button("▶️ Tocar Dó Pitagórico"):
        st.audio(gen_tone(val), sample_rate=44100)

with c3:
    st.markdown("**3. O Batimento (A Diferença)**")
    if st.button("▶️ Tocar Juntos"):
        mix = gen_tone(100.0) + gen_tone(val)
        st.audio(mix, sample_rate=44100)
        st.error("Esse som pulsante ('waw-waw') é o Coma Pitagórico acontecendo fisicamente no ar.")
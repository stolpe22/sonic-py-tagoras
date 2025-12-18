import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Treino Auditivo Pro", page_icon="👂", layout="wide")

# --- CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .game-box {
        background-color: #222;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #444;
        text-align: center;
        margin-bottom: 20px;
    }
    .result-box {
        margin-top: 20px;
        padding: 15px;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
    }
    .difficulty-selector {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border-left: 5px solid #FFC107;
    }
</style>
""", unsafe_allow_html=True)

st.title("👂 Desafio do Afinador: Timbres Musicais")

# --- NOVO MOTOR DE SÍNTESE (Sons Confortáveis) ---
def generate_wave(freq, duration, wave_type="flute", sr=44100):
    t = np.linspace(0, duration, int(sr*duration), endpoint=False)
    
    if wave_type == "flute": 
        # TIPO 1: FLAUTA (Seno Puro)
        # Extremamente suave, sem harmônicos.
        return 0.4 * np.sin(2 * np.pi * freq * t)
    
    elif wave_type == "electric_piano":
        # TIPO 2: PIANO ELÉTRICO (Tipo Rhodes)
        # Em vez de onda quadrada estridente, somamos harmônicos suaves.
        # Fundamental + 2º Harmônico (fraco) + 4º Harmônico (fraco)
        w = 0.4 * np.sin(2 * np.pi * freq * t)
        w += 0.2 * np.sin(2 * np.pi * (freq * 2) * t)
        w += 0.1 * np.sin(2 * np.pi * (freq * 4) * t)
        return w
    
    elif wave_type == "soft_string":
        # TIPO 3: CORDA SUAVE (Onda Triangular)
        # A triangular é rica como a dente de serra, mas muito menos "abelhuda".
        # Fórmula da Triangular: 
        return 0.4 * (2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1)
    
    return np.zeros_like(t)

# --- ESTADO DO JOGO ---
if 'target_freq' not in st.session_state:
    st.session_state.target_freq = np.random.randint(430, 450)
if 'show_result' not in st.session_state:
    st.session_state.show_result = False

# --- CONFIGURAÇÃO DE DIFICULDADE (Mudamos os nomes) ---
with st.expander("⚙️ Configuração de Timbres", expanded=True):
    col_dif, col_desc = st.columns([1, 2])
    
    with col_dif:
        difficulty = st.radio(
            "Escolha os Instrumentos:",
            ["Nível 1: Flauta x Flauta", "Nível 2: Corda x Flauta", "Nível 3: Piano Elétrico x Corda"]
        )
    
    with col_desc:
        if "Nível 1" in difficulty:
            st.info("🟢 **Iniciante (Sons Puros)**\n\nVocê vai afinar dois sons de **Flauta** (senoides). O batimento é muito límpido e fácil de ouvir.")
            target_instr = "flute"
            user_instr = "flute"
        elif "Nível 2" in difficulty:
            st.warning("🟡 **Intermediário (Realista)**\n\nVocê tem um **Diapasão (Flauta)** e precisa afinar um **Violino (Corda)**. A textura da corda torna o desafio mais interessante, mas ainda agradável.")
            target_instr = "soft_string" 
            user_instr = "flute"     
        else:
            st.error("🔴 **Avançado (Harmônico)**\n\nDois instrumentos ricos: **Piano Elétrico** vs **Violino**. Muitos harmônicos se cruzam. Exige ouvido treinado para achar a fundamental.")
            target_instr = "electric_piano"
            user_instr = "soft_string"

st.divider()

# --- O JOGO ---
col_game, col_spoiler = st.columns([1, 1])

with col_game:
    st.markdown('<div class="game-box">', unsafe_allow_html=True)
    st.subheader("🎛️ Mesa de Afinação")
    
    # 1. Slider
    user_freq = st.slider("Ajuste a frequência (Hz):", 420.0, 460.0, 440.0, 0.5)
    
    st.markdown("---")

    # 2. Botão de Ouvir
    if st.button("🔊 Tocar Mistura (Som Suave)", type="primary"):
        sr = 44100
        # Gerar as duas ondas
        w_target = generate_wave(st.session_state.target_freq, 3.0, target_instr, sr)
        w_user = generate_wave(user_freq, 3.0, user_instr, sr)
        
        # Mixagem
        mix = w_target + w_user
        
        # Envelope suave (Fade In/Out para não dar estalo)
        env = np.concatenate([np.linspace(0, 1, 2000), np.ones(len(mix)-4000), np.linspace(1, 0, 2000)])
        
        # Normalização para garantir volume confortável
        max_val = np.max(np.abs(mix))
        if max_val > 0:
            mix = mix / max_val * 0.5 # 50% do volume máximo para segurança
            
        st.audio(mix * env, sample_rate=sr)

    st.caption(f"Referência: {target_instr.replace('_', ' ').title()} | Você: {user_instr.replace('_', ' ').title()}")
    st.markdown("---")

    # 3. Confirmação
    if st.button("✅ Confirmar Resposta"):
        st.session_state.show_result = True
    
    # 4. Resultado
    if st.session_state.show_result:
        diff = abs(user_freq - st.session_state.target_freq)
        
        if diff == 0:
            st.balloons()
            st.markdown(f'<div class="result-box" style="background:#1c4a25; color:#cfc;">🎉 PERFEITO!</div>', unsafe_allow_html=True)
        elif diff <= 1.0:
            st.balloons()
            st.markdown(f'<div class="result-box" style="background:#1c4a25; color:#cfc;">🏆 EXCELENTE! Erro: {diff:.1f} Hz.</div>', unsafe_allow_html=True)
        elif diff <= 3.0:
            st.markdown(f'<div class="result-box" style="background:#5e5a00; color:#ff9;">⚠️ QUASE... Erro: {diff:.1f} Hz.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result-box" style="background:#4a1c1c; color:#fcc;">❌ TENTE DE NOVO. Erro: {diff:.1f} Hz.</div>', unsafe_allow_html=True)
        
        st.markdown(f"**Alvo:** {st.session_state.target_freq} Hz | **Você:** {user_freq} Hz")
        
        if st.button("🔄 Novo Desafio"):
            st.session_state.target_freq = np.random.randint(430, 450)
            st.session_state.show_result = False
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

with col_spoiler:
    st.info("💡 **Dica:** Tente fechar os olhos. O som 'liso' é como uma linha reta. O som desafinado tem 'caroços'.")
    
    with st.expander("👀 Ver Spoiler Visual", expanded=False):
        st.subheader("Osciloscópio")
        
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('#0e1117')
        ax.set_facecolor('#0e1117')
        
        # Zoom de 20ms para ver o formato da onda
        t_vis = np.linspace(0, 0.02, 1000) 
        
        wt = generate_wave(st.session_state.target_freq, 0.02, target_instr, 50000)
        wu = generate_wave(user_freq, 0.02, user_instr, 50000)
        
        # Plota ondas individuais
        ax.plot(t_vis, wt, color='#4CAF50', alpha=0.3, label='Alvo')
        ax.plot(t_vis, wu, color='#FFC107', alpha=0.3, label='Você')
        
        # Plota mix
        ax.plot(t_vis, wt+wu, color='white', lw=1.5, label='Mix')
        
        ax.legend(facecolor='#222', labelcolor='white')
        ax.axis('off')
        st.pyplot(fig)
        
        envelope_freq = abs(user_freq - st.session_state.target_freq)
        st.caption(f"Batimento: {envelope_freq:.1f} Hz")

# --- MODO QUIZ ---
st.divider()
st.subheader("🧠 Nível 2: Ouvido Absoluto (Velocidade)")

if 'quiz_diff' not in st.session_state:
    st.session_state.quiz_diff = np.random.choice([1, 2, 4, 8])

col_q1, col_q2 = st.columns([1, 2])

with col_q1:
    st.write("Ouça o batimento. Qual a velocidade?")
    if st.button("🔊 Tocar Desafio"):
        f_base = 440
        f_desafio = f_base + st.session_state.quiz_diff
        sr = 44100
        # Usando os sons suaves aqui também
        w1 = generate_wave(f_base, 4.0, "soft_string", sr)
        w2 = generate_wave(f_desafio, 4.0, "flute", sr)
        
        # Normalização de segurança
        mix = (w1+w2) * 0.5
        st.audio(mix, sample_rate=sr)

with col_q2:
    cols = st.columns(4)
    if cols[0].button("1 Hz (Lento)"):
        if st.session_state.quiz_diff == 1: st.success("Correto!"); st.balloons()
        else: st.error("Errou.")
        
    if cols[1].button("2 Hz (Médio)"):
        if st.session_state.quiz_diff == 2: st.success("Correto!"); st.balloons()
        else: st.error("Errou.")

    if cols[2].button("4 Hz (Rápido)"):
        if st.session_state.quiz_diff == 4: st.success("Correto!"); st.balloons()
        else: st.error("Errou.")
        
    if cols[3].button("8 Hz (Motor)"):
        if st.session_state.quiz_diff == 8: st.success("Correto!"); st.balloons()
        else: st.error("Errou.")
    
    if st.button("Próximo Quiz ➡️"):
        st.session_state.quiz_diff = np.random.choice([1, 2, 4, 8])
        st.rerun()
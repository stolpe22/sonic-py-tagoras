import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="O Intervalo do Lobo", page_icon="🐺", layout="wide")

# --- CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .history-box {
        background-color: #262730;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #3498db;
        margin-bottom: 15px;
    }
    .wolf-alert {
        background-color: #4a1c1c;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #e74c3c;
        color: #ffcccc;
    }
    .sweet-spot {
        background-color: #1c4a25;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #4CAF50;
        color: #ccffcc;
    }
    h3 { border-bottom: 1px solid #444; padding-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

st.title("🐺 Arqueologia Musical: A Saga das Afinações")
st.markdown("### Por que seu piano nunca está 100% afinado?")

# --- INTRODUÇÃO (WIKI) ---
with st.expander("📚 O Problema Matemático (O Cobertor Curto)", expanded=False):
    st.markdown("""
    A música é baseada em proporções simples:
    * **Oitava:** 2/1 (Dobro)
    * **Quinta:** 3/2 (1.5x)
    * **Terça Maior:** 5/4 (1.25x)
    
    **O Drama:** É matematicamente impossível fazer esses três números se encaixarem perfeitamente num ciclo de 12 notas.
    Se você afina as Quintas perfeitas, as Terças ficam horríveis (Pitagórico).
    Se você afina as Terças perfeitas, as Quintas ficam curtas (Mesotônico).
    Se você divide o erro por igual, nada fica perfeito, mas nada fica horrível (Temperado Moderno).
    """)

st.divider()

# --- SELETOR DE ERA ---
col_sel, col_info = st.columns([1, 2])

with col_sel:
    st.subheader("⏳ Máquina do Tempo")
    era = st.radio(
        "Escolha o Sistema:",
        ["1. Pitagórico (Idade Média)", "2. Mesotônico (Renascença)", "3. Temperado (Moderno)"],
        captions=[
            "Quintas Puras, Terças ásperas.",
            "Terças Puras (Doces), Quintas curtas.",
            "Tudo igual, nada puro."
        ]
    )

with col_info:
    if "Pitagórico" in era:
        st.markdown("""
        <div class="history-box">
            <h4>🏰 Era Pitagórica (1400s)</h4>
            <p><b>Foco:</b> Quintas Perfeitas (3:2) para cantos gregorianos e harmonias abertas.</p>
            <p><b>O Problema:</b> A Terça Maior (Dó-Mi) ficava muito "esticada" e brilhante, quase desafinada.</p>
            <p><b>O Lobo:</b> Escondido entre G# e Eb. Soava terrível.</p>
        </div>
        """, unsafe_allow_html=True)
    elif "Mesotônico" in era:
        st.markdown("""
        <div class="history-box" style="border-left-color: #f1c40f;">
            <h4>🎨 Era Mesotônica (1600s)</h4>
            <p><b>Foco:</b> A Terça Maior Pura (5:4). Na Renascença, a música ficou mais emotiva e precisava de terças doces e calmas.</p>
            <p><b>O Preço:</b> Para consertar a Terça, eles tiveram que "encurtar" as Quintas. O som é melancólico e lindo.</p>
            <p><b>O Lobo:</b> Ficou AINDA MAIOR. Tocar na tonalidade errada era insuportável.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="history-box" style="border-left-color: #4CAF50;">
            <h4>🎹 Era Temperada (Hoje)</h4>
            <p><b>Foco:</b> Liberdade total. Queremos tocar em qualquer tom (Dó, Fá#, Si...).</p>
            <p><b>A Solução:</b> Pegamos o "Lobo" e o cortamos em 12 pedacinhos minúsculos, espalhando um pouquinho de desafinação em cada tecla.</p>
            <p><b>Resultado:</b> Nada é puramente físico (natural), mas nada dói no ouvido.</p>
        </div>
        """, unsafe_allow_html=True)

# --- FUNÇÕES DE ÁUDIO E CÁLCULO ---
def get_freqs(root, system):
    # Frequências baseadas em C4 = 261.63
    # Retorna: [Freq Fundamental, Freq Terça, Freq Quinta]
    
    if "Pitagórico" in system:
        # Quinta = 1.5 (Pura)
        # Terça = 1.2656 (81/64 - O Ditono Pitagórico, muito brilhante/áspero)
        # Lobo (se for a tecla G#)
        if root > 400: # Simulando G#
            return [root, root * 1.2656, root * 1.479] # Quinta do lobo encurtada
        return [root, root * 1.2656, root * 1.5]

    elif "Mesotônico" in system:
        # Quinta = 1.4953 (Encurtada propositalmente para consertar a terça)
        # Terça = 1.25 (Pura/Natural 5:4 - O "Doce" da Renascença)
        if root > 400: # Simulando G# (O Lobo Mesotônico é feroz)
            return [root, root * 1.25, root * 1.531] # Quinta do lobo muito larga!
        return [root, root * 1.25, root * 1.4953]

    else: # Temperado
        # Quinta = 1.4983 (Quase pura)
        # Terça = 1.2599 (Um meio termo aceitável)
        return [root, root * 1.2599, root * 1.4983]

def play_system(is_wolf, system_name):
    base = 415.30 if is_wolf else 261.63 # G# (Lobo) ou C (Puro)
    freqs = get_freqs(base, system_name)
    
    sr = 44100
    t = np.linspace(0, 3, sr*3, endpoint=False)
    wave = np.zeros_like(t)
    
    # Sintetizar Acorde
    for f in freqs:
        wave += 0.3 * np.sin(2 * np.pi * f * t)
        
    # Envelope
    env = np.concatenate([np.linspace(0, 1, 2000), np.ones(len(wave)-4000), np.linspace(1, 0, 2000)])
    return wave * env

# --- FUNÇÃO DE DESENHO DO PIANO ---
def draw_piano(system_name):
    fig, ax = plt.subplots(figsize=(10, 3))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')

    # Teclas Brancas
    for i in range(8):
        rect = patches.Rectangle((i, 0), 1, 1, facecolor='white', edgecolor='black')
        ax.add_patch(rect)
        ax.text(i+0.5, 0.1, "CDEFGABC"[i], ha='center')

    # Teclas Pretas e Destaques
    black_pos = [1, 2, 4, 5, 6] # C#, D#, F#, G#, A#
    labels = ["C#", "D#/Eb", "F#", "G#", "A#"]
    
    for i, pos in enumerate(black_pos):
        color = 'black'
        lbl = labels[i]
        
        # Lógica de Cores por Sistema
        if "Temperado" not in system_name:
            if lbl == "G#" or "D#" in lbl:
                color = '#800000' # Vermelho escuro (Perigo)
        
        rect = patches.Rectangle((pos-0.3, 0.4), 0.6, 0.6, facecolor=color, edgecolor='black', zorder=2)
        ax.add_patch(rect)
        
        # Ícones
        if "Temperado" not in system_name and (lbl == "G#" or "D#" in lbl):
            ax.text(pos, 0.5, "🐺", ha='center', va='center', fontsize=12, zorder=3)
            
    # Conexão do Lobo
    if "Temperado" not in system_name:
        ax.annotate("", xy=(2, 0.9), xytext=(5, 0.9), arrowprops=dict(arrowstyle="<->", color='red', lw=2))
        ax.text(3.5, 0.95, "INTERVALO DO LOBO\n(G# a Eb)", ha='center', color='red', fontweight='bold', backgroundcolor='#0e1117')

    ax.set_xlim(0, 8); ax.set_ylim(0, 1.3); ax.axis('off')
    return fig

# --- LABORATÓRIO INTERATIVO ---
st.divider()
st.header("🎹 Laboratório Comparativo")

col_piano, col_buttons = st.columns([3, 2])

with col_piano:
    st.pyplot(draw_piano(era))

with col_buttons:
    st.markdown("### Ouça a Diferença")
    
    # Botão 1: Acorde Bom
    st.markdown("#### 1. Tocar em Dó Maior (Seguro)")
    if st.button("🎵 Tocar Dó Maior (C-E-G)"):
        st.audio(play_system(False, era), sample_rate=44100)
    
    if "Mesotônico" in era:
        st.caption("✅ Note como este acorde é calmo e 'doce'. A Terça é pura!")
    elif "Pitagórico" in era:
        st.caption("✅ Note como é brilhante, mas a Terça vibra um pouco rápido.")
        
    st.markdown("---")
    
    # Botão 2: O Lobo
    st.markdown("#### 2. Tocar no Lobo (Proibido)")
    if st.button("🐺 Tocar G# Maior (O Acorde Quebrado)"):
        st.audio(play_system(True, era), sample_rate=44100)
        
    if "Temperado" in era:
        st.success("Tudo certo! Soa igual ao Dó Maior. O Lobo foi domesticado.")
    elif "Mesotônico" in era:
        st.error("⚠️ ESCUTE! Parece desafinado e 'uivando'. A Quinta é larga demais.")
    else:
        st.error("⚠️ Batimento forte e rápido. Inutilizável musicalmente.")

# --- TABELA COMPARATIVA ---
st.divider()
with st.expander("📊 Tabela Comparativa (Resumo Técnico)", expanded=True):
    data = {
        "Sistema": ["Pitagórico", "Mesotônico (1/4 Coma)", "Temperado Igual"],
        "A Quinta (G)": ["Pura (Perfeita)", "Encurtada (Desafinada)", "Quase Pura"],
        "A Terça (E)": ["Muito Aguda (Dissonante)", "Pura (Doce/Perfeita)", "Aguda (Aceitável)"],
        "O Lobo": ["Sim (Uiva)", "Sim (Feroz)", "Não (Distribuído)"],
        "Pode modular?": ["Não (Só tons simples)", "Não (Só tons centrais)", "Sim (Qualquer tom)"]
    }
    st.table(data)
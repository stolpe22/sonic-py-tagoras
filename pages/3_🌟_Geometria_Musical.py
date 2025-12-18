import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Geometria Musical", page_icon="🌟", layout="wide")

# --- CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .story-box {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FFC107;
        margin-bottom: 20px;
    }
    .math-box {
        font-family: 'Courier New', monospace;
        background-color: #111;
        padding: 15px;
        border: 1px solid #333;
        border-radius: 5px;
        color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌟 A Geometria da Música: Por que 12 notas?")

# --- INTRODUÇÃO ---
with st.expander("📚 O Resumo da Ópera (Leia Primeiro)", expanded=True):
    st.markdown("""
    Como o vídeo explicou, a música não é aleatória.
    1.  **Física:** Uma corda vibra em harmônicos (visto na página "Série Harmônica").
    2.  **Matemática:** Para criar notas novas que combinam, usamos a **Quinta Justa** (multiplicar a frequência por 1.5).
    3.  **Geometria:** Se organizarmos essas notas num círculo, as escalas que soam bem formam **desenhos simétricos (Estrelas)**.
    
    Vamos testar essa teoria agora! 👇
    """)

st.divider()

# --- INTERFACE PRINCIPAL ---
col_ctrl, col_vis = st.columns([1, 2])

with col_ctrl:
    st.subheader("🛠️ O Construtor de Escalas")
    st.write("Vamos empilhar Quintas (x1.5) e ver o desenho que forma.")
    
    # Controle de Passos (Quantas quintas?)
    passos = st.slider("Quantas notas gerar?", 1, 12, 1)
    
    # Explicação Dinâmica baseada no vídeo
    if passos == 1:
        st.info("🎵 1 Nota: Apenas a Tônica. Tédio total.")
    elif passos == 5:
        st.success("🌟 5 Notas: **Escala Pentatônica**! (Música Asiática/Blues). Forma uma forma simétrica simples.")
    elif passos == 7:
        st.success("🏛️ 7 Notas: **Escala Maior/Diatônica**! (Dó-Ré-Mi...). A base da música ocidental. Forma uma estrela complexa.")
    elif passos == 12:
        st.warning("🌈 12 Notas: **Escala Cromática**. O círculo completo (Piano). Simetria perfeita.")
    elif passos == 6:
        st.error("❌ 6 Notas: Não forma simetria bonita. (Escala de Tons Inteiros - soa estranho).")
    else:
        st.write(f"Gerando {passos} notas...")

    st.markdown("---")
    st.markdown("#### 🧮 A Matemática Moderna")
    st.markdown("Para fechar o círculo perfeitamente (sem o Lobo), usamos a fórmula do **Temperamento Igual**:")
    
    st.latex(r"f_n = f_0 \cdot 2^{\frac{n}{12}}")
    st.caption("Cada nota é exatamente a raiz 12ª de 2 maior que a anterior.")

with col_vis:
    st.subheader("🕸️ O Círculo das Quintas (Visual)")
    
    # Configuração do Gráfico Polar
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    
    # As 12 posições do relógio (Notas Cromáticas)
    # C=0, G=1, D=2... (Seguindo o Círculo das Quintas para visualização geométrica)
    # Mas para facilitar a visão de "Estrela", vamos plotar na ordem cromática e desenhar as linhas de conexão.
    
    # Notas Cromáticas (Posições fixas no círculo)
    chromatic_notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    angles = np.linspace(0, 2*np.pi, 12, endpoint=False)
    
    # Vamos rotacionar para C ficar no topo (pi/2)
    angles = np.roll(angles, 0) # Ajuste visual se precisar
    
    # Plota os pontos base (As 12 notas possíveis)
    ax.scatter(angles, [1]*12, color='#333', s=100, zorder=1)
    
    # Adiciona rótulos
    for ang, note in zip(angles, chromatic_notes):
        # Ajuste de rotação para leitura
        ax.text(ang, 1.15, note, color='white', ha='center', va='center', fontweight='bold', fontsize=12)

    # --- LÓGICA DE GERAÇÃO (A Mágica) ---
    # Começamos em C (Indice 0)
    # A cada passo, somamos 7 semitons (Uma Quinta Justa)
    
    current_idx = 0 # C
    visited_indices = [0]
    
    lines_x = []
    lines_y = []
    
    path_angles = [angles[0]]
    path_radii = [1.0]
    
    for _ in range(passos - 1):
        # Pula 7 semitons (A Quinta)
        next_idx = (current_idx + 7) % 12
        visited_indices.append(next_idx)
        
        # Guardar coordenadas para linha
        path_angles.append(angles[next_idx])
        path_radii.append(1.0)
        
        current_idx = next_idx

    # Desenhar as LINHAS de conexão (A Geometria)
    # Se passos > 1, desenhamos a teia
    if passos > 1:
        # Desenha a linha conectando na ordem de geração
        ax.plot(path_angles, path_radii, color='#FFC107', linewidth=2, linestyle='-', marker='o', markersize=8, zorder=10)
        
        # Se for 12, fecha o círculo visualmente
        if passos == 12:
            ax.plot([path_angles[-1], path_angles[0]], [1, 1], color='#FFC107', linewidth=2)

    # Destacar as notas ativas (tocadas)
    active_angles = [angles[i] for i in visited_indices]
    ax.scatter(active_angles, [1]*len(active_angles), color='#4CAF50', s=250, zorder=20, edgecolors='white')

    ax.set_ylim(0, 1.2)
    ax.axis('off')
    st.pyplot(fig)

# --- ÁUDIO GERADO ---
st.divider()
st.subheader("🎹 Ouça a Escala Gerada")

if st.button("🔊 Tocar Notas Selecionadas"):
    # Gerar som
    sr = 44100
    wave_total = np.array([])
    
    # Ordenar as frequências para tocar em escala (do grave pro agudo) e não na ordem de geração (quintas)
    # Isso faz soar "musical" (Dó, Ré, Mi...) em vez de "técnico" (Dó, Sol, Ré...)
    visited_indices.sort()
    
    for note_idx in visited_indices:
        # Fórmula do Temperamento Igual explicada no vídeo
        # f = f0 * (2^(n/12))
        freq = 261.63 * (2 ** (note_idx / 12))
        
        t = np.linspace(0, 0.4, int(sr*0.4), endpoint=False)
        # Som suave (Seno + Harmônico)
        tone = 0.5 * np.sin(2*np.pi*freq*t) + 0.2*np.sin(4*np.pi*freq*t)
        
        # Envelope curto
        tone *= np.concatenate([np.linspace(0,1,500), np.ones(len(tone)-1000), np.linspace(1,0,500)])
        
        wave_total = np.concatenate([wave_total, tone])
        
    st.audio(wave_total, sample_rate=sr)

# --- CONTEÚDO EDUCACIONAL EXTRA ---
with st.expander("🧠 Por que 5 e 7 funcionam e 6 não? (Simetria)"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **A Regra da Estrela:**
        O vídeo explica que escalas boas são aquelas que formam polígonos regulares ou quase regulares (Estrelas).
        
        * **5 Notas (Pentatônica):** Deixa "buracos" grandes no círculo, mas eles são bem distribuídos. É estável.
        * **7 Notas (Maior):** É a distribuição mais eficiente de pontos sem criar aglomerados (semitons) excessivos.
        """)
    with col2:
        st.markdown("""
        **O Fracasso do 6:**
        Se você fizer 6 quintas, você cai exatamente no lado oposto do círculo (Trítono).
        Isso cria uma simetria tão perfeita que se torna monótona e ambígua (Escala de Tons Inteiros).
        Não tem "centro" gravitacional (Tônica).
        """)
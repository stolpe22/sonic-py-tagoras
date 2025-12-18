import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(page_title="Série Harmônica", page_icon="🧬", layout="wide")

# --- CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .theory-box {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 20px;
    }
    .logic-box {
        background-color: #222;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #e74c3c;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .didactic-box {
        background-color: #262730;
        border: 1px solid #4CAF50;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧬 A Série Harmônica: A Matemática de Deus")

# --- LÓGICA DE PRESETS (MIXER) ---
def atualizar_presets():
    escolha = st.session_state.preset_combo
    new_vals = []
    if escolha == "Seno Puro": new_vals = [1.0] + [0.0]*7
    elif escolha == "Dente de Serra (Todos)": new_vals = [1.0/(i+1) for i in range(8)]
    elif escolha == "Clarinete (Ímpares)": new_vals = [(1.0/(i+1) if (i+1)%2!=0 else 0.0) for i in range(8)]
    elif escolha == "Órgão (Oitavas)": new_vals = [1.0, 0.0, 0.5, 0.0, 0.25, 0.0, 0.1, 0.0]
    
    if new_vals:
        for i, val in enumerate(new_vals):
            st.session_state[f"vol_{i}"] = val

# Inicialização segura do estado
for i in range(8):
    if f"vol_{i}" not in st.session_state:
        st.session_state[f"vol_{i}"] = 1.0 if i == 0 else 0.0

# --- TABS ---
tab_teoria, tab_violao, tab_mixer = st.tabs(["📊 Teoria Completa", "🎸 Física do Violão (Didático)", "🎛️ Mixer"])

# --- ABA 1: TEORIA COMPLETA ---
with tab_teoria:
    st.header("1. O Acorde da Natureza")
    
    col_chart, col_text = st.columns([2, 1])
    
    with col_chart:
        dados_harmonicos = []
        nomes = ["Tônica", "Oitava", "Quinta", "Oitava", "Terça Maior", "Quinta", "7ª Menor", "Oitava", "2ª Maior", "3ª Maior", "4ª Aum", "Quinta", "6ª Menor", "7ª Menor", "7ª Maior", "Oitava"]
        
        for i in range(1, 17):
            cor = "#3498db"
            if i in [4, 5, 6]: cor = "#4CAF50"
            if i == 7: cor = "#e74c3c"
            
            dados_harmonicos.append({
                "H": i,
                "Amplitude": 1/i,
                "Cor": cor,
                "Nota": nomes[i-1]
            })
            
        df = pd.DataFrame(dados_harmonicos)
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('H:O', title='Harmônico'),
            y=alt.Y('Amplitude', title='Energia'),
            color=alt.Color('Cor', scale=None),
            tooltip=['H', 'Nota']
        ).properties(height=350)
        
        text = chart.mark_text(dy=-10, color='white').encode(text='Nota')
        st.altair_chart(chart + text, use_container_width=True)

    with col_text:
        st.markdown("""
        <div class="theory-box">
            <h4>🌿 O Segredo Verde</h4>
            <p>Observe as barras <b style="color:#4CAF50">Verdes (4, 5, 6)</b>.</p>
            <p>Se você tocar essas três frequências juntas, você ouve um <b>Acorde Maior Perfeito</b>.</p>
            <p>A natureza "esconde" um acorde maior dentro de cada nota.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    
    st.header("2. Por que essa ordem?")
    col_logic, col_table = st.columns([1, 1])

    with col_logic:
        st.markdown("""
        <div class="logic-box">
            <h4>🧮 A Regra da Multiplicação</h4>
            <p>A série multiplica a vibração (x2, x3, x4...).</p>
            <ul>
                <li><b>H1 (x1):</b> Original.</li>
                <li><b>H2 (x2):</b> O dobro é a Oitava (mesma nota).</li>
                <li><b>H3 (x3):</b> O triplo cria a Quinta.</li>
                <li><b>H5 (x5):</b> O quíntuplo cria a Terça.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_table:
        df_logica = pd.DataFrame([
            ["1", "1x", "Dó", "Tônica"],
            ["2", "2x", "Dó", "Oitava"],
            ["3", "3x", "Sol", "Quinta"],
            ["4", "4x", "Dó", "Oitava"],
            ["5", "5x", "Mi", "Terça Maior"],
            ["6", "6x", "Sol", "Quinta"],
        ], columns=["H", "Mult", "Nota", "Intervalo"])
        st.table(df_logica)


# --- ABA 2: VIOLÃO (CORRIGIDA) ---
with tab_violao:
    st.header("🎸 O Mapa dos Harmônicos")
    st.markdown("Use o seletor abaixo para encontrar os pontos mágicos no braço do violão.")

    # Seletor de Casas Reais
    casas_opcoes = ["12ª Casa (Oitava)", "7ª Casa (Quinta)", "5ª Casa (2 Oitavas)", "9ª Casa (Terça/Repetida)", "4ª Casa (Terça)", "3ª Casa (Quinta Alta)"]
    escolha_casa = st.select_slider("Onde você vai encostar o dedo?", options=casas_opcoes, value="12ª Casa (Oitava)")
    
    # Lógica
    if "12ª" in escolha_casa:
        harm = 2; pos_dedo = 0.5; explicacao = "Metade exata da corda."
        msg_extra = "O som é a mesma nota da corda solta, só que mais aguda."
    elif "7ª" in escolha_casa:
        harm = 3; pos_dedo = 1/3; explicacao = "Divide a corda em 3 partes."
        msg_extra = "O som é uma Quinta (Ex: Corda Lá -> Som Mi)."
    elif "5ª" in escolha_casa:
        harm = 4; pos_dedo = 1/4; explicacao = "Divide a corda em 4 partes."
        msg_extra = "Som de Oitava (Duas oitavas acima da solta)."
    elif "4ª" in escolha_casa:
        harm = 5; pos_dedo = 1/5; explicacao = "Divide a corda em 5 partes."
        msg_extra = "Som de Terça Maior. (Ex: Corda Lá -> Som Dó#)."
    elif "9ª" in escolha_casa:
        harm = 5; pos_dedo = 0.4; explicacao = "Divide a corda em 5 partes (no 2º ponto)." 
        msg_extra = "💡 CURIOSIDADE: A 9ª casa gera o MESMO harmônico da 4ª casa!"
    elif "3ª" in escolha_casa:
        harm = 6; pos_dedo = 1/6; explicacao = "Divide a corda em 6 partes."
        msg_extra = "Som de Quinta (muito aguda)."

    col_vis, col_info = st.columns([3, 1])
    
    with col_vis:
        # DPI alto para evitar serrilhado
        fig, ax = plt.subplots(figsize=(10, 3), dpi=100)
        fig.patch.set_facecolor('#222')
        ax.set_facecolor('#222')
        
        x = np.linspace(0, 1, 600)
        y = np.sin(harm * np.pi * x)
        
        # 1. DESENHAR OS TRASTES DE REFERÊNCIA (Sólidos e fixos)
        trastes_reais = {
            0.5: "12ª", 
            0.333: "7ª", 
            0.25: "5ª", 
            0.2: "4ª", 
            0.4: "9ª",
            0.166: "3ª"
        }
        
        # Desenha TODAS as linhas de referência primeiro
        for pos, nome in trastes_reais.items():
            # Linha Sólida (sem pontilhado) e cinza claro
            ax.axvline(pos, color='#666', linestyle='-', linewidth=1.5, zorder=1)
            # Texto da casa
            ax.text(pos, -1.25, nome, color='#aaa', ha='center', fontsize=9, fontweight='bold')

        # 2. DESENHAR A CORDA (Onda)
        ax.plot(x, y, color='#00ff00', lw=2.5, label='Vibração', zorder=2)
        ax.plot(x, -y, color='#00ff00', lw=2.5, alpha=0.3, ls='-', zorder=2) # Fantasma sólido também
        ax.axhline(0, color='#888', lw=1, zorder=1) # Linha central
        
        # 3. DESENHAR O DEDO DO USUÁRIO (Bolinha Branca)
        # Z-order alto para ficar em cima das linhas
        ax.scatter([pos_dedo], [0], s=250, color='white', edgecolor='red', linewidth=2, zorder=10)
        ax.text(pos_dedo, 0.7, "👇 Dedo aqui", color='white', ha='center', fontsize=12, fontweight='bold', zorder=10)

        # Se for a 9ª casa, mostra a referência fantasma da 4ª
        if "9ª" in escolha_casa:
            other_node = 0.2
            ax.scatter([other_node], [0], s=80, color='gray', alpha=0.6, zorder=5)
            ax.text(other_node, 0.3, "(Mesmo Nó)", color='gray', ha='center', fontsize=8)

        ax.axis('off')
        ax.set_ylim(-1.4, 1.4)
        st.pyplot(fig)

    with col_info:
        st.markdown(f"""
        <div class="didactic-box">
            <h3>🎵 Harmônico {harm}</h3>
            <p style="font-size: 1.1em; color: #4CAF50;">{msg_extra}</p>
            <hr>
            <p><b>A Física:</b> {explicacao}</p>
            <p>As linhas cinzas verticais são os trastes fixos do violão.</p>
        </div>
        """, unsafe_allow_html=True)


# --- ABA 3: MIXER ---
with tab_mixer:
    st.header("🎛️ Mixer de Harmônicos")
    st.selectbox(
        "Presets:", 
        ["Manual", "Seno Puro", "Dente de Serra (Todos)", "Clarinete (Ímpares)", "Órgão (Oitavas)"],
        key="preset_combo",
        on_change=atualizar_presets
    )
    st.write("---")
    cols = st.columns(8)
    for i in range(8):
        with cols[i]:
            st.slider(f"H{i+1}", 0.0, 1.0, key=f"vol_{i}")

    if st.button("🔊 Tocar Som", type="primary"):
        sr = 44100; t = np.linspace(0, 2.0, int(sr*2.0), endpoint=False); wave = np.zeros_like(t); base_freq = 110.0
        for i in range(8):
            vol = st.session_state[f"vol_{i}"]
            if vol > 0: wave += vol * np.sin(2 * np.pi * (base_freq * (i+1)) * t)
        env = np.concatenate([np.linspace(0, 1, 1000), np.ones(len(wave)-2000), np.linspace(1, 0, 1000)])
        st.audio((wave * env) / (np.max(np.abs(wave)) + 0.001), sample_rate=sr)
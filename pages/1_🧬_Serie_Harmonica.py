import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import streamlit.components.v1 as components # Importante para a animação lisa
import json

st.set_page_config(page_title="Série Harmônica Viva", page_icon="🎻", layout="wide")

# --- CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .theory-card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #9b59b6;
        margin-bottom: 20px;
    }
    .nature-chord-box {
        background-color: #1c2e26;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin-top: 20px;
    }
    /* Esconde o botão de fullscreen do iframe para ficar mais limpo */
    iframe { width: 100%; border: none; }
</style>
""", unsafe_allow_html=True)

st.title("🎻 Série Harmônica: A Física da Música")

# --- ESTADO GLOBAL ---
if 'amplitudes' not in st.session_state:
    st.session_state.amplitudes = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

# --- NAVEGAÇÃO ---
menu = st.radio(
    "Navegação",
    ["📚 Aula Teórica", "🎻 Corda Viva (Visualizador)", "🎸 No Violão"],
    horizontal=True,
    label_visibility="collapsed"
)

# --- FUNÇÕES ---
def apply_preset(name):
    new_vals = []
    if name == "Flauta": new_vals = [1.0, 0.1, 0.05, 0.0, 0.0, 0.0]
    elif name == "Clarinete": new_vals = [1.0, 0.0, 0.6, 0.0, 0.3, 0.0]
    elif name == "Violino": new_vals = [1.0, 0.5, 0.33, 0.25, 0.2, 0.16]
    elif name == "Sino": new_vals = [1.0, 0.0, 0.0, 0.0, 0.8, 0.0]
    
    for i, val in enumerate(new_vals):
        st.session_state.amplitudes[i] = val
        # Atualiza os sliders se existirem na sessão
        if f"sl_{i}" in st.session_state:
            st.session_state[f"sl_{i}"] = val

# =========================================
# CONTEÚDO 1: TEORIA
# =========================================
if menu == "📚 Aula Teórica":
    st.header("📚 Fundamentos da Acústica")
    st.subheader("1. Como a corda se divide?")
    
    fig_theory, axs = plt.subplots(4, 1, figsize=(10, 8))
    fig_theory.patch.set_facecolor('#0e1117')
    plt.subplots_adjust(hspace=0.6)
    
    for i in range(4):
        h = i + 1
        x_t = np.linspace(0, 1, 400)
        y_t = np.sin(h * np.pi * x_t)
        
        ax = axs[i]
        ax.set_facecolor('#0e1117')
        ax.set_title(f"H{h} (Frequência = {h}x) - Divide a corda em {h} partes", color='white', fontsize=12, pad=10)
        ax.plot(x_t, y_t, color='#4CAF50', lw=2)
        ax.plot(x_t, -y_t, color='#4CAF50', lw=2, alpha=0.3, ls='--')
        ax.axis('off')
        
        nodes = np.linspace(0, 1, h+1)
        ax.scatter(nodes, np.zeros_like(nodes), color='white', s=30, zorder=5)

    st.pyplot(fig_theory)
    
    st.divider()
    
    st.subheader("2. A Matemática das Frequências")
    col_text, col_chart = st.columns([1, 1.5])
    
    with col_text:
        st.markdown("""
        <div class="theory-card">
            <h4>📐 A Regra de Ouro</h4>
        """, unsafe_allow_html=True)
        
        st.latex(r"f_n = n \cdot f_1")
        
        st.markdown("""
            <p style="margin-top: 10px;">Se a nota fundamental é <b>Lá (110 Hz)</b>:</p>
            <ul>
                <li><b>H1 (1x):</b> 110 Hz</li>
                <li><b>H2 (2x):</b> 220 Hz</li>
                <li><b>H3 (3x):</b> 330 Hz</li>
                <li><b>H4 (4x):</b> 440 Hz</li>
                <li><b>H5 (5x):</b> 550 Hz</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_chart:
        st.markdown("#### 🎹 O 'DNA' do Som")
        dados_harmonicos = []
        nomes_notas = ["Tônica (1x)", "Oitava (2x)", "Quinta (3x)", "Oitava (4x)", "Terça Maior (5x)", "Quinta (6x)", "7ª Menor (7x)", "Oitava (8x)"]
        
        for i in range(1, 9):
            cor = "#3498db"
            if i in [4, 5, 6]: cor = "#4CAF50"
            if i == 7: cor = "#e74c3c"
            
            dados_harmonicos.append({
                "Harmônico": f"H{i}", 
                "Energia": 1/i, 
                "Cor": cor, 
                "Nota": nomes_notas[i-1], 
                "Frequência": f"{i}x"
            })
            
        df_chart = pd.DataFrame(dados_harmonicos)
        chart = alt.Chart(df_chart).mark_bar().encode(
            x=alt.X('Harmônico', sort=None), 
            y=alt.Y('Energia', axis=None), 
            color=alt.Color('Cor', scale=None), 
            tooltip=['Harmônico', 'Nota', 'Frequência']
        ).properties(height=300)
        
        text = chart.mark_text(dy=-10, color='white').encode(text='Nota')
        st.altair_chart(chart + text, use_container_width=True)

        st.markdown("""
        <div class="nature-chord-box" style="margin-top: 10px; padding: 15px;">
            <h5 style="margin: 0; color: #fff;">🌿 A Natureza é "Maior"</h5>
            <hr style="margin: 5px 0; border-color: #4CAF50;">
            <p style="font-size: 0.95em;">
                Repare nas barras <b>Verdes (H4, H5 e H6)</b>. 
                Quando elas vibram juntas, formam a proporção matemática <b>4:5:6</b>.
            </p>
            <p style="font-size: 0.95em;">
                Essa proporção exata cria a <b>Tríade Maior</b> (Dó-Mi-Sol). 
                Isso prova que o acorde "alegre" não foi inventado por humanos; 
                ele é uma consequência inevitável da física das cordas!
            </p>
        </div>
        """, unsafe_allow_html=True)

# =========================================
# CONTEÚDO 2: ANIMAÇÃO (COM PAUSE E VELOCIDADE)
# =========================================
elif menu == "🎻 Corda Viva (Visualizador)":
    col_vis, col_mixer = st.columns([2, 1])

    with col_mixer:
        st.subheader("🎛️ Timbre")
        
        # Botões de Preset
        c1, c2 = st.columns(2)
        if c1.button("Flauta 🪈"): apply_preset("Flauta")
        if c2.button("Clarinete 🌭"): apply_preset("Clarinete")
        c3, c4 = st.columns(2)
        if c3.button("Violino 🎻"): apply_preset("Violino")
        if c4.button("Sino 🔔"): apply_preset("Sino")
        
        st.markdown("---")
        st.caption("Ajuste a energia de cada harmônico:")
        
        # Sliders de Harmônicos
        for i in range(6):
            val = st.slider(f"H{i+1}", 0.0, 1.0, value=st.session_state.amplitudes[i], key=f"sl_{i}", 
                          on_change=lambda i=i: st.session_state.amplitudes.__setitem__(i, st.session_state[f"sl_{i}"]))
            st.session_state.amplitudes[i] = val
            
        st.markdown("---")
        st.subheader("⚙️ Controles")

        # --- CONTROLE DE VELOCIDADE (NOVO) ---
        # Default 0.05 (velocidade normal)
        speed = st.slider("Velocidade da Animação", 0.01, 0.20, 0.05, 0.01)
        
        # --- BOTÃO PAUSAR ---
        if 'animating' not in st.session_state:
            st.session_state.animating = True

        def toggle_anim():
            st.session_state.animating = not st.session_state.animating

        btn_label = "⏸️ Pausar" if st.session_state.animating else "▶️ Tocar"
        st.button(btn_label, on_click=toggle_anim, type="primary" if st.session_state.animating else "secondary")
        
        show_sum = st.checkbox("Mostrar Soma (Linha Branca)", value=True)

    with col_vis:
        st.subheader("Interferência em Tempo Real")
        
        # --- PREPARAÇÃO DOS DADOS PRO JAVASCRIPT ---
        # Enviamos agora o "speed" junto com o resto
        js_data = json.dumps({
            "amps": st.session_state.amplitudes[:6],
            "showSum": show_sum,
            "isPaused": not st.session_state.animating,
            "speed": speed # <--- O valor do slider vai aqui
        })

        # --- HTML/JS ---
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ margin: 0; background-color: #0e1117; overflow: hidden; }}
                canvas {{ width: 100%; height: 400px; border-radius: 8px; border: 1px solid #333; }}
            </style>
        </head>
        <body>
            <canvas id="waveCanvas"></canvas>
            <script>
                const canvas = document.getElementById('waveCanvas');
                const ctx = canvas.getContext('2d');
                
                const data = {js_data};
                
                const colors = ['#ff00ff', '#ffff00', '#00ff00', '#00ffff', '#ff9900', '#ff3333'];
                
                if (typeof window.time === 'undefined') window.time = 0;
                
                function resize() {{
                    canvas.width = window.innerWidth;
                    canvas.height = 400;
                }}
                window.addEventListener('resize', resize);
                resize();

                function draw() {{
                    const w = canvas.width;
                    const h = canvas.height;
                    const centerY = h / 2;
                    const scaleY = h / 5;
                    
                    ctx.clearRect(0, 0, w, h);
                    
                    // Eixo
                    ctx.beginPath(); ctx.strokeStyle = '#333'; ctx.lineWidth = 1;
                    ctx.moveTo(0, centerY); ctx.lineTo(w, centerY); ctx.stroke();

                    const numPoints = 300;
                    const sumY = new Float32Array(numPoints);
                    
                    for (let hIdx = 0; hIdx < 6; hIdx++) {{
                        const amp = data.amps[hIdx];
                        if (amp < 0.01) continue;
                        
                        const hNum = hIdx + 1;
                        const color = colors[hIdx];
                        
                        ctx.beginPath();
                        ctx.strokeStyle = color;
                        ctx.lineWidth = 1.5;
                        ctx.globalAlpha = 0.6;
                        
                        for (let i = 0; i < numPoints; i++) {{
                            const xNorm = i / (numPoints - 1);
                            const xPix = xNorm * w;
                            
                            // Usa window.time para animar
                            const yVal = amp * Math.sin(hNum * Math.PI * xNorm) * Math.cos(window.time * hNum);
                            
                            sumY[i] += yVal;
                            const yPix = centerY - (yVal * scaleY);
                            if (i === 0) ctx.moveTo(xPix, yPix); else ctx.lineTo(xPix, yPix);
                        }}
                        ctx.stroke();
                        
                        // Fantasma
                        ctx.beginPath();
                        ctx.setLineDash([2, 4]); ctx.lineWidth = 0.5; ctx.globalAlpha = 0.3;
                        for (let i = 0; i < numPoints; i++) {{
                            const xNorm = i / (numPoints - 1);
                            const xPix = xNorm * w;
                            const yVal = amp * Math.sin(hNum * Math.PI * xNorm);
                            const yPix = centerY - (yVal * scaleY);
                            if (i === 0) ctx.moveTo(xPix, yPix); else ctx.lineTo(xPix, yPix);
                        }}
                        ctx.stroke();
                        ctx.setLineDash([]);
                    }}

                    if (data.showSum) {{
                        ctx.beginPath(); ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 3; ctx.globalAlpha = 1.0;
                        for (let i = 0; i < numPoints; i++) {{
                            const xNorm = i / (numPoints - 1);
                            const xPix = xNorm * w;
                            const yPix = centerY - (sumY[i] * scaleY);
                            if (i === 0) ctx.moveTo(xPix, yPix); else ctx.lineTo(xPix, yPix);
                        }}
                        ctx.stroke();
                    }}
                    
                    // --- LÓGICA DE VELOCIDADE ---
                    if (!data.isPaused) {{
                        // Agora soma o valor vindo do Slider (data.speed)
                        window.time += data.speed;
                    }}
                    
                    requestAnimationFrame(draw);
                }}
                
                draw();
            </script>
        </body>
        </html>
        """
        components.html(html_code, height=410)
        
        # --- LEGENDA DE CORES ---
        st.markdown("""
        <div style="display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; background-color: #161b22; padding: 10px; border-radius: 8px; font-size: 0.8em; border: 1px solid #333; margin-top: -5px; margin-bottom: 15px;">
            <div style="display: flex; align-items: center;"><span style="background: #ff00ff; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; display:inline-block;"></span><b>H1</b> (Tônica)</div>
            <div style="display: flex; align-items: center;"><span style="background: #ffff00; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; display:inline-block;"></span><b>H2</b> (Oitava)</div>
            <div style="display: flex; align-items: center;"><span style="background: #00ff00; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; display:inline-block;"></span><b>H3</b> (Quinta)</div>
            <div style="display: flex; align-items: center;"><span style="background: #00ffff; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; display:inline-block;"></span><b>H4</b> (2ª Oitava)</div>
            <div style="display: flex; align-items: center;"><span style="background: #ff9900; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; display:inline-block;"></span><b>H5</b> (Terça Maior)</div>
            <div style="display: flex; align-items: center;"><span style="background: #ff3333; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; display:inline-block;"></span><b>H6</b> (Quinta Alta)</div>
            <div style="display: flex; align-items: center; margin-left: 10px; padding-left: 10px; border-left: 1px solid #555;"><span style="background: #ffffff; width: 15px; height: 4px; margin-right: 5px; display:inline-block;"></span><b>SOMA</b> (Resultado)</div>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.animating:
            st.warning("⏸️ Pausado")

# =========================================
# CONTEÚDO 3: VIOLÃO
# =========================================
elif menu == "🎸 No Violão":
    st.header("🎸 Harmônicos Naturais")
    st.markdown("Use o slider para encontrar os nós e veja como eles formam o Acorde Maior.")
    
    casas_opcoes = [
        "12ª (H2 - Oitava)", 
        "7ª (H3 - Quinta)", 
        "5ª (H4 - 2 Oitavas)", 
        "9ª (H5 - Terça Maior)", 
        "4ª (H5 - Terça Maior)",
        "3ª (H6 - Quinta Alta)"
    ]
    
    escolha = st.select_slider("Posição do Dedo:", options=casas_opcoes, value="12ª (H2 - Oitava)")
    
    harm_map = {"12ª":2, "7ª":3, "5ª":4, "9ª":5, "4ª":5, "3ª":6}
    node_pos_map = {"12ª":0.5, "7ª":0.333, "5ª":0.25, "9ª":0.4, "4ª":0.2, "3ª":0.166}
    
    selected_key = escolha.split(' ')[0]
    h_val = harm_map[selected_key]
    finger_pos = node_pos_map[selected_key]

    fig, ax = plt.subplots(figsize=(12, 3), dpi=100)
    fig.patch.set_facecolor('#222'); ax.set_facecolor('#222')
    
    x_v = np.linspace(0, 1, 800)
    y_v = np.sin(h_val * np.pi * x_v)
    
    ax.axhline(0, color='#666', lw=1)
    ax.plot(x_v, y_v, color='#00ff00', lw=2.5, label='Vibração')
    ax.plot(x_v, -y_v, color='#00ff00', lw=2.5, alpha=0.3, ls='--')
    
    for i in range(1, 13):
        fret_pos = 1 - (1 / (2 ** (i / 12)))
        ax.axvline(fret_pos, color='#444', lw=1.5, zorder=1)
        ax.text(fret_pos, -1.3, str(i), color='#888', ha='center', fontsize=9, fontweight='bold')
    ax.axvline(0, color='#888', lw=3)
    
    ax.scatter([finger_pos], [0], s=250, color='white', edgecolor='red', lw=2, zorder=10)
    ax.text(finger_pos, 0.7, "👇 Dedo aqui", color='white', ha='center', fontweight='bold', fontsize=10)
    
    ax.axis('off'); ax.set_ylim(-1.4, 1.4); ax.set_xlim(-0.02, 1.02)
    st.pyplot(fig)
    
    st.markdown("---")
    
    col_info, col_acorde = st.columns([1, 1])
    
    with col_info:
        st.info(f"📍 **Detalhe Técnico:**\nAo tocar na **{selected_key} casa**, você força a corda a se dividir em **{h_val} partes** iguais.")
        
    with col_acorde:
        msg_header = "🌿 O Segredo Verde"
        if h_val == 4:
            msg_body = "Você encontrou a **TÔNICA** (H4). A base do acorde."
        elif h_val == 5:
            msg_body = "Você encontrou a **TERÇA MAIOR** (H5). É ela que dá a alegria ao acorde!"
        elif h_val == 6:
            msg_body = "Você encontrou a **QUINTA** (H6). O fechamento do acorde."
        else:
            msg_body = "Continue explorando para achar as partes do acorde (4, 5 e 6)."

        st.markdown(f"""
        <div class="nature-chord-box">
            <h4>{msg_header}</h4>
            <p>{msg_body}</p>
            <p style="font-size:0.9em; opacity:0.8;">Lembre-se: H4, H5 e H6 juntos formam o Acorde Maior Perfeito.</p>
        </div>
        """, unsafe_allow_html=True)
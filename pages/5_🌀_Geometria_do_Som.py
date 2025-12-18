import streamlit as st
import json
import streamlit.components.v1 as components

st.set_page_config(page_title="Geometria de Lissajous (Animada)", page_icon="🌀", layout="wide")

st.title("🌀 Geometria do Som: Lissajous em Tempo Real")

# --- CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .main-wrapper { 
        background-color: #000; 
        border: 1px solid #333; 
        border-radius: 10px; 
        padding: 10px;
        text-align: center;
    }
    .mini-manual {
        font-size: 0.85em;
        color: #bbb;
        background: #1a1a1a;
        padding: 10px;
        border-radius: 5px;
        border-left: 3px solid #4CAF50;
        margin-bottom: 10px;
        margin-top: 10px;
    }
    .curiosity-box {
        background-color: #262730;
        border: 1px solid #FF4B4B;
        border-radius: 5px;
        padding: 15px;
        margin-top: 15px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- AULAS TEÓRICAS ---
with st.expander("📚 Aula 1: Como ler o desenho? (Decifrando a Geometria)", expanded=False):
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown("""
        **O Mecanismo:**
        Imagine uma caneta presa a dois motores:
        * O motor **X** empurra a caneta para Esquerda/Direita.
        * O motor **Y** empurra a caneta para Cima/Baixo.
        """)
    with col_b:
        st.markdown("""
        **A Regra das Pontas (Lombadas):**
        Conte quantas vezes a curva toca a borda do gráfico.
        * **1 : 1 (Uníssono):** Desenha um Círculo ou Linha.
        * **2 : 1 (Oitava):** Desenha uma Parábola (forma de U) ou um 8.
        * **3 : 2 (Quinta):** Desenha um Nó (3 pontas verticais, 2 horizontais).
        """)

with st.expander("📚 Aula 2: O que é a Defasagem (Fase)?", expanded=False):
    st.markdown("""
    ### O "Atraso" da Onda
    A **Fase** não muda a nota, muda o **ponto de partida**.
    * **0.0 π:** Começam juntos (Linha /).
    * **0.5 π:** Defasagem máxima (Círculo O).
    
    ### Por que o desenho gira sozinho?
    Se as frequências não forem perfeitamente exatas, o "atraso" muda a cada milissegundo. Essa mudança constante é o que vemos como **rotação 3D**.
    """)

st.divider()

# --- CONTROLES (Python) ---
col_setup, col_vis = st.columns([1, 2])

with col_setup:
    st.subheader("🎛️ Configuração Sonora")
    
    modo = st.radio("Entrada:", ["🎵 Notas Musicais", "🧮 Frequência Livre"], horizontal=True)
    
    freq_x, freq_y = 0.0, 0.0
    
    if modo == "🎵 Notas Musicais":
        sistema = st.selectbox("Afinação:", ["Natural (Just)", "Temperado (Equal)"])
        notas = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        ratios_justos = [1/1, 16/15, 9/8, 6/5, 5/4, 4/3, 45/32, 3/2, 8/5, 5/3, 9/5, 15/8]
        c4 = 261.63

        def get_freq(idx, oitava, sys):
            if sys.startswith("Natural"): return c4 * ratios_justos[idx] * (2 ** (oitava - 4))
            else: return c4 * (2 ** ((idx + ((oitava - 4) * 12)) / 12))

        c1, c2 = st.columns(2)
        with c1:
            nx = st.selectbox("Nota X", notas, index=0)
            ox = st.number_input("Oitava X", 1, 8, 4)
        with c2:
            ny = st.selectbox("Nota Y", notas, index=7) # G (Quinta)
            oy = st.number_input("Oitava Y", 1, 8, 4)
            
        freq_x = get_freq(notas.index(nx), ox, sistema)
        freq_y = get_freq(notas.index(ny), oy, sistema)

        # --- A NOVA EXPLICAÇÃO / CURIOSIDADE ---
        st.markdown("""
        <div class="curiosity-box">
            <h4>💡 Por que o desenho muda?</h4>
            <p>Faça o teste agora: alterne o seletor de <b>Afinação</b> acima.</p>
            <ul>
                <li><b>No Natural:</b> O desenho fica <b>PARADO</b>. <br>Isso acontece porque a proporção matemática é exata (ex: 3 para 2). As ondas se encaixam como engrenagens perfeitas.</li>
                <li><b>No Temperado:</b> O desenho fica <b>GIRANDO</b>. <br>Isso prova que a afinação moderna é "errada"! Como a proporção não é exata (é 1.498... e não 1.5), as ondas nunca se encontram no mesmo lugar, criando esse efeito de rotação eterna.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        c1, c2 = st.columns(2)
        with c1: freq_x = st.number_input("Freq X", 1.0, 1000.0, 200.0, 0.1)
        with c2: freq_y = st.number_input("Freq Y", 1.0, 1000.0, 300.0, 0.1)

    st.write("---")
    
    # --- MINI MANUAL ---
    st.markdown("""
    <div class="mini-manual">
    <b>📐 Controle Manual de Fase (π):</b><br>
    Use se quiser girar a figura manualmente.<br>
    • 0.0 π: Fechado (/) | 0.5 π: Aberto (O)
    </div>
    """, unsafe_allow_html=True)

    delta_pi = st.slider("Fase Manual", 0.0, 2.0, 0.5, 0.05)
    delta = delta_pi * 3.14159

    st.divider()
    
    # --- AJUSTES VISUAIS ---
    st.subheader("🎨 Estética")
    velocidade = st.slider("Velocidade", 0.0001, 0.02, 0.002, 0.0001, format="%.4f")
    espessura = st.slider("Espessura", 0.5, 5.0, 1.0, 0.5)
    brilho = st.slider("Brilho Neon", 0, 20, 0)
    rastro = st.slider("Rastro (Fade)", 0.01, 0.3, 0.05)

    # Análise Rápida
    ratio = freq_y / freq_x if freq_x else 0
    st.info(f"Ratio Matemático: {ratio:.5f}")

# --- JSON PARA O JAVASCRIPT ---
dados_json = json.dumps({
    "freqX": freq_x,
    "freqY": freq_y,
    "delta": delta,
    "speed": velocidade,
    "lineWidth": espessura,
    "glow": brilho,
    "fade": rastro
})

# --- VISUALIZADOR ANIMADO (JS) ---
with col_vis:
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ margin: 0; background: #000; overflow: hidden; color: white; font-family: sans-serif; }}
        .container {{ display: flex; flex-direction: column; align-items: center; justify-content: center; height: 500px; }}
        canvas {{ background: #000; border: 1px solid #333; border-radius: 8px; }}
        .btn {{
            margin-top: 15px; padding: 10px 25px; font-size: 16px; 
            background: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;
            transition: 0.2s; font-weight: bold;
        }}
        .btn:hover {{ background: #45a049; transform: scale(1.05); }}
    </style>
    </head>
    <body>
    <div class="container">
        <canvas id="canvas" width="600" height="400"></canvas>
        <button class="btn" id="playBtn" onclick="toggleAudio()">🔊 Tocar / Parar Som</button>
    </div>

    <script>
        const data = {dados_json};
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const btn = document.getElementById('playBtn');

        let audioCtx = null;
        let oscX = null;
        let oscY = null;
        let isPlaying = false;
        let gainNode = null;

        const width = canvas.width;
        const height = canvas.height;
        const centerX = width / 2;
        const centerY = height / 2;
        const scale = 150; 

        const trail = [];
        const maxTrail = 1000; 
        let time = 0;

        function draw() {{
            ctx.fillStyle = `rgba(0, 0, 0, ${{data.fade}})`; 
            ctx.fillRect(0, 0, width, height);

            time += data.speed;

            const x = centerX + Math.sin(data.freqX * time + data.delta) * scale;
            const y = centerY + Math.sin(data.freqY * time) * scale;

            trail.push({{x, y}});
            if (trail.length > maxTrail) trail.shift();

            ctx.beginPath();
            ctx.strokeStyle = '#00ff00';
            ctx.lineWidth = data.lineWidth;
            ctx.shadowBlur = data.glow; 
            ctx.shadowColor = '#00ff00';

            for (let i = 0; i < trail.length - 1; i++) {{
                ctx.moveTo(trail[i].x, trail[i].y);
                ctx.lineTo(trail[i+1].x, trail[i+1].y);
            }}
            ctx.stroke();

            ctx.beginPath();
            ctx.shadowBlur = 0; 
            ctx.fillStyle = '#fff';
            ctx.arc(x, y, data.lineWidth + 2, 0, Math.PI * 2);
            ctx.fill();

            requestAnimationFrame(draw);
        }}
        
        draw();

        function toggleAudio() {{
            if (!isPlaying) {{
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                gainNode = audioCtx.createGain();
                gainNode.gain.value = 0.1; 
                gainNode.connect(audioCtx.destination);

                oscX = audioCtx.createOscillator();
                oscX.type = 'sine';
                oscX.frequency.value = data.freqX;
                
                oscY = audioCtx.createOscillator();
                oscY.type = 'sine';
                oscY.frequency.value = data.freqY;

                oscX.connect(gainNode);
                oscY.connect(gainNode);

                oscX.start();
                oscY.start();
                
                isPlaying = true;
                btn.innerText = "🛑 Parar Som";
                btn.style.background = "#e74c3c";
            }} else {{
                if(oscX) oscX.stop();
                if(oscY) oscY.stop();
                isPlaying = false;
                btn.innerText = "🔊 Tocar / Parar Som";
                btn.style.background = "#4CAF50";
            }}
        }}
    </script>
    </body>
    </html>
    """
    components.html(html_code, height=550)
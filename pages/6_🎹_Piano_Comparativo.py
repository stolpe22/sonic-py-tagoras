import streamlit as st
import numpy as np
import json
import streamlit.components.v1 as components

st.set_page_config(page_title="Piano Comparativo + Spectrum", page_icon="🎹", layout="wide")

st.title("🎹 Piano Comparativo: Onda vs. Espectro")

# --- CSS para layout limpo ---
st.markdown("""
<style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    iframe { width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.header("🎛️ Configuração")
    frequencia_base = st.number_input("Frequência C3 (Hz)", value=130.81, step=1.0)
    st.divider()
    st.info("""
    **Legenda Visual:**
    
    🌊 **Modo Onda (Tempo):**
    Ótimo para ver o "batimento" (o som oscilando).
    
    📊 **Modo Barras (Frequência):**
    Mostra os picos de energia.
    * **Verde:** Natural
    * **Laranja:** Temperado
    """)

# --- Cálculos Matemáticos ---
base_ratios = [1/1, 16/15, 9/8, 6/5, 5/4, 4/3, 45/32, 3/2, 8/5, 5/3, 9/5, 15/8]
notas_nome_base = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
eh_preta_base = [False, True, False, True, False, False, True, False, True, False, True, False]

freqs_natural = []
freqs_temperada = []
notas_labels = []
notas_cores = []

num_oitavas = 2
for oitava in range(num_oitavas):
    for i in range(12):
        # Natural
        f_nat = frequencia_base * base_ratios[i] * (2 ** oitava)
        freqs_natural.append(f_nat)
        # Temperado
        semitom_global = i + (oitava * 12)
        f_temp = frequencia_base * (2 ** (semitom_global / 12))
        freqs_temperada.append(f_temp)
        # Labels
        notas_labels.append(f"{notas_nome_base[i]}{3+oitava}")
        notas_cores.append(eh_preta_base[i])

# C5 Final
freqs_natural.append(frequencia_base * 4)
freqs_temperada.append(frequencia_base * (2 ** (24 / 12)))
notas_labels.append(f"C{3+num_oitavas}")
notas_cores.append(False)

dados_json = json.dumps({
    "natural": freqs_natural,
    "temperado": freqs_temperada,
    "labels": notas_labels,
    "eh_preta": notas_cores
})

# --- Injeção HTML/JS ---
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: monospace; color: white; background-color: #0e1117; user-select: none; overflow: hidden; }}
    
    .main-wrapper {{
        display: flex; flex-direction: column; align-items: center; gap: 10px; width: 100%;
    }}

    .top-bar {{ 
        display: flex; gap: 20px; align-items: center; justify-content: center;
        background: #1f2937; padding: 10px; border-radius: 8px; width: 100%; max-width: 800px;
    }}
    
    .control-group {{ display: flex; flex-direction: column; align-items: center; }}
    .control-group label {{ font-size: 10px; color: #aaa; margin-bottom: 2px; text-transform: uppercase; }}

    select {{ padding: 5px; background: #333; color: white; border: 1px solid #555; border-radius: 4px; }}
    
    .toggle-container {{ display: flex; background: #111; border-radius: 4px; border: 1px solid #444; overflow: hidden; }}
    .toggle-btn {{ 
        padding: 5px 15px; cursor: pointer; font-size: 12px; background: #111; color: #888; border: none; transition: 0.2s;
    }}
    .toggle-btn:hover {{ color: white; }}
    .toggle-btn.active {{ background: #333; color: #4CAF50; font-weight: bold; }}

    /* CANVAS */
    .visualizer-container {{
        width: 100%; max-width: 800px; height: 140px;
        background: #000; border: 1px solid #444; border-radius: 5px; position: relative;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }}
    canvas {{ width: 100%; height: 100%; display: block; }}
    
    /* PIANO */
    .piano-group {{ display: flex; flex-direction: column; gap: 2px; position: relative; margin-top: 5px; }}
    .piano-label {{ font-size: 10px; color: #aaa; margin-left: 5px; }}
    .piano {{ position: relative; height: 130px; display: flex; justify-content: center; }}
    
    .key {{
        border: 1px solid #777; border-radius: 0 0 4px 4px; cursor: pointer;
        box-sizing: border-box; display: flex; flex-direction: column; 
        align-items: center; justify-content: flex-end;
        padding-bottom: 5px; position: relative;
    }}
    .white-key {{ width: 32px; height: 100%; background: white; color: black; z-index: 1; }}
    .white-key .kb {{ color: #d32f2f; font-weight: bold; font-size: 11px; margin-bottom: 2px; }}
    .white-key .note {{ font-size: 8px; opacity: 0.6; }}
    .white-key.active {{ background: #ccc; }}
    
    .black-key {{
        width: 22px; height: 60%; background: #111; color: white; 
        position: absolute; z-index: 2; border: 1px solid #000; border-top: none;
    }}
    .black-key .kb {{ color: #4fc3f7; font-weight: bold; font-size: 10px; margin-bottom: 2px; }}
    .black-key.active {{ background: #444; }}

    /* MONITOR DE FREQUÊNCIA */
    #monitor {{
        margin-top: 15px; font-size: 1.5em; font-weight: bold; color: #4CAF50;
        text-align: center; height: 30px; font-family: monospace;
        text-shadow: 0 0 10px rgba(76, 175, 80, 0.3);
    }}

</style>
</head>
<body>

<div class="main-wrapper">
    
    <div class="top-bar">
        <div class="control-group">
            <label>Controle do Teclado (PC)</label>
            <select id="mode-selector">
                <option value="both">Tocar Ambos</option>
                <option value="natural">Apenas Natural</option>
                <option value="temperado">Apenas Temperado</option>
            </select>
        </div>
        <div class="control-group">
            <label>Tipo de Gráfico</label>
            <div class="toggle-container">
                <button class="toggle-btn active" onclick="setVisMode('wave', this)">🌊 Onda</button>
                <button class="toggle-btn" onclick="setVisMode('bar', this)">📊 Barras</button>
            </div>
        </div>
    </div>

    <div class="visualizer-container">
        <canvas id="scope"></canvas>
    </div>

    <div class="piano-group">
        <div class="piano-label">Natural (Just Intonation)</div>
        <div class="piano" id="piano-nat"></div>
    </div>
    
    <div class="piano-group">
        <div class="piano-label">Temperado (Equal Temperament)</div>
        <div class="piano" id="piano-temp"></div>
    </div>

    <div id="monitor">Clique no piano para ativar...</div>

</div>

<script>
    const data = {dados_json};
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    const ctx = new AudioContext();
    
    const analyserNat = ctx.createAnalyser();
    const analyserTemp = ctx.createAnalyser();
    analyserNat.fftSize = 2048; 
    analyserTemp.fftSize = 2048;
    
    const masterGain = ctx.createGain();
    masterGain.gain.value = 0.4;
    masterGain.connect(ctx.destination);
    
    analyserNat.connect(masterGain);
    analyserTemp.connect(masterGain);

    const canvas = document.getElementById('scope');
    const cCtx = canvas.getContext('2d');
    let visualMode = 'wave';

    function setVisMode(mode, btn) {{
        visualMode = mode;
        document.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    }}

    function draw() {{
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
        const w = canvas.width;
        const h = canvas.height;
        const bufferLength = analyserNat.frequencyBinCount;
        cCtx.fillStyle = '#000';
        cCtx.fillRect(0, 0, w, h);

        if (visualMode === 'wave') {{
            const dataNat = new Uint8Array(bufferLength);
            const dataTemp = new Uint8Array(bufferLength);
            analyserNat.getByteTimeDomainData(dataNat);
            analyserTemp.getByteTimeDomainData(dataTemp);
            cCtx.lineWidth = 2;
            const drawWaveLine = (data, color) => {{
                cCtx.beginPath();
                cCtx.strokeStyle = color;
                const sliceWidth = w * 1.0 / bufferLength;
                let x = 0;
                for(let i = 0; i < bufferLength; i++) {{
                    const v = data[i] / 128.0;
                    const y = v * (h / 2);
                    if(i===0) cCtx.moveTo(x, y); else cCtx.lineTo(x, y);
                    x += sliceWidth;
                }}
                cCtx.stroke();
            }};
            cCtx.globalCompositeOperation = 'screen';
            drawWaveLine(dataTemp, '#ff9500');
            drawWaveLine(dataNat, '#00ff00');
        }} else {{
            const dataNat = new Uint8Array(bufferLength);
            const dataTemp = new Uint8Array(bufferLength);
            analyserNat.getByteFrequencyData(dataNat);
            analyserTemp.getByteFrequencyData(dataTemp);
            const barWidth = (w / bufferLength) * 2.5;
            let x = 0;
            cCtx.globalCompositeOperation = 'lighter';
            const limit = bufferLength / 2; 
            for(let i = 0; i < limit; i++) {{
                const barHeightNat = dataNat[i] / 2;
                cCtx.fillStyle = 'rgba(0, 255, 0, 0.6)';
                cCtx.fillRect(x, h - barHeightNat, barWidth, barHeightNat);
                const barHeightTemp = dataTemp[i] / 2;
                cCtx.fillStyle = 'rgba(255, 149, 0, 0.6)';
                cCtx.fillRect(x, h - barHeightTemp, barWidth, barHeightTemp);
                x += barWidth + 1;
            }}
        }}
        requestAnimationFrame(draw);
    }}
    draw();

    const keyMap = {{
        'z': 0, 's': 1, 'x': 2, 'd': 3, 'c': 4, 'v': 5, 'g': 6, 'b': 7, 'h': 8, 'n': 9, 'j': 10, 'm': 11,
        'q': 12, '2': 13, 'w': 14, '3': 15, 'e': 16, 'r': 17, '5': 18, 't': 19, '6': 20, 'y': 21, '7': 22, 'u': 23, 'i': 24
    }};
    const indexToChar = {{}};
    for (const [char, idx] of Object.entries(keyMap)) indexToChar[idx] = char.toUpperCase();

    function playSound(freq, type) {{
        if (ctx.state === 'suspended') ctx.resume();
        const osc = ctx.createOscillator(); 
        const gain = ctx.createGain();
        osc.type = 'triangle'; 
        osc.frequency.value = freq;
        const now = ctx.currentTime;
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(0.5, now + 0.05);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 2.0);
        osc.connect(gain);
        if (type === 'nat') gain.connect(analyserNat);
        else gain.connect(analyserTemp);
        osc.start(); osc.stop(now + 2.0);
    }}

    // Adicionado parâmetro 'fixedMode' para identificar se veio do mouse
    function createKeys(containerId, freqs, prefix, fixedMode) {{
        const container = document.getElementById(containerId);
        let leftPos = 0;
        const whiteWidth = 32; const blackWidth = 22;
        data.labels.forEach((label, i) => {{
            const isBlack = data.eh_preta[i];
            const bindChar = indexToChar[i] || "";
            const key = document.createElement('div');
            key.id = prefix + '-' + i;
            key.innerHTML = `<span class="kb">${{bindChar}}</span><span class="note">${{label}}</span>`;
            if (!isBlack) {{
                key.className = 'key white-key'; leftPos += whiteWidth;
            }} else {{
                key.className = 'key black-key';
                key.style.left = (leftPos - (blackWidth / 2)) + 'px'; 
            }}
            
            // Passa o modo fixo (natural ou temperado) no clique do mouse
            key.onmousedown = () => triggerNote(i, fixedMode);
            key.onmouseup = () => releaseNote(i);
            key.onmouseleave = () => releaseNote(i);
            container.appendChild(key);
        }});
        container.style.width = leftPos + 'px';
    }}

    // Atualizado para aceitar 'forcedMode'
    function triggerNote(index, forcedMode = null) {{
        const globalMode = document.getElementById('mode-selector').value;
        const monitor = document.getElementById('monitor');
        
        // Lógica de decisão
        let playNat = false;
        let playTemp = false;

        if (forcedMode) {{
            // Se veio do Mouse, obedece o clique independente do combobox
            if (forcedMode === 'natural') playNat = true;
            if (forcedMode === 'temperado') playTemp = true;
        }} else {{
            // Se veio do Teclado, obedece o combobox
            if (globalMode === 'both' || globalMode === 'natural') playNat = true;
            if (globalMode === 'both' || globalMode === 'temperado') playTemp = true;
        }}

        // Execução Visual e Sonora
        let txt = data.labels[index] + " | ";
        
        if (playNat) {{
            document.getElementById('k-nat-' + index)?.classList.add('active');
            playSound(data.natural[index], 'nat');
            txt += "Nat: " + data.natural[index].toFixed(1) + "Hz ";
        }}
        
        if (playTemp) {{
            document.getElementById('k-temp-' + index)?.classList.add('active');
            playSound(data.temperado[index], 'temp');
            txt += "Temp: " + data.temperado[index].toFixed(1) + "Hz";
        }}
        
        monitor.innerText = txt;
    }}

    function releaseNote(index) {{
        document.getElementById('k-nat-' + index)?.classList.remove('active');
        document.getElementById('k-temp-' + index)?.classList.remove('active');
    }}

    // Eventos de Teclado (chamam triggerNote SEM forcedMode)
    window.addEventListener('keydown', (e) => {{ if (!e.repeat && keyMap.hasOwnProperty(e.key.toLowerCase())) triggerNote(keyMap[e.key.toLowerCase()]); }});
    window.addEventListener('keyup', (e) => {{ if (keyMap.hasOwnProperty(e.key.toLowerCase())) releaseNote(keyMap[e.key.toLowerCase()]); }});
    
    // Criação das teclas passando o modo fixo do mouse
    createKeys('piano-nat', data.natural, 'k-nat', 'natural');
    createKeys('piano-temp', data.temperado, 'k-temp', 'temperado');

</script>
</body>
</html>
"""

components.html(html_code, height=600)
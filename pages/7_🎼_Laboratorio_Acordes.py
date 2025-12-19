import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Laboratório de Acordes", page_icon="🎼", layout="wide")

# --- CSS Customizado ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .chord-box {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #3498db;
        margin-bottom: 20px;
    }
    .happy { border-left-color: #4CAF50; } /* Maior */
    .sad { border-left-color: #3498db; }   /* Menor */
    .tense { border-left-color: #e74c3c; } /* Diminuto/Aumentado */
    .complex { border-left-color: #9b59b6; } /* Setimas */
    
    .metric-container {
        background-color: #111;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        border: 1px solid #333;
    }
    .big-note { font-size: 1.5em; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🎼 Laboratório de Acordes")
st.markdown("### A Química das Emoções Musicais")

# --- 1. CONTROLES (MESA DE MISTURA) ---
col_ctrl, col_info = st.columns([1, 2])

with col_ctrl:
    st.subheader("🎹 Monte seu Acorde")
    
    # Fundamental
    notas = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    root_note = st.selectbox("Nota Fundamental (Raiz):", notas, index=0)
    octave = st.number_input("Oitava:", 2, 5, 4)
    
    # Tipo de Acorde
    tipos_acorde = {
        "Maior (Feliz/Estável)": [0, 4, 7],
        "Menor (Triste/Melancólico)": [0, 3, 7],
        "Diminuto (Tenso/Assustador)": [0, 3, 6],
        "Aumentado (Misterioso/Onírico)": [0, 4, 8],
        "Sus4 (Suspenso/Aberto)": [0, 5, 7],
        "Maior com 7ª (Jazzy/Sofisticado)": [0, 4, 7, 11],
        "Menor com 7ª (Soul/Profundo)": [0, 3, 7, 10]
    }
    
    chord_type_name = st.selectbox("Qualidade do Acorde:", list(tipos_acorde.keys()))
    intervals = tipos_acorde[chord_type_name]
    
    # Determinar estilo visual baseada no nome
    style_class = "happy"
    if "Menor" in chord_type_name: style_class = "sad"
    if "Diminuto" in chord_type_name or "Aumentado" in chord_type_name: style_class = "tense"
    if "7ª" in chord_type_name: style_class = "complex"

# --- LÓGICA DE CÁLCULO ---
def get_freq(note_name, oct):
    # Dicionário de distancias a partir de C
    semitones_from_c = {n: i for i, n in enumerate(notas)}
    
    # --- CORREÇÃO AQUI ---
    # Antes estava usando semitones_from_c[root_note], o que travava tudo na raiz.
    # Agora usa semitones_from_c[note_name], que é a nota atual do loop.
    midi_note = semitones_from_c[note_name] + ((oct + 1) * 12)
    
    # Cálculo da frequência baseado no padrão MIDI (A4 = 69 = 440Hz)
    return 440.0 * (2 ** ((midi_note - 69) / 12))

# Calcular frequencias do acorde
chord_freqs = []
chord_notes_names = []

for interval in intervals:
    # Achar o nome da nota
    root_idx = notas.index(root_note)
    note_idx = (root_idx + interval) % 12
    note_name = notas[note_idx]
    
    # Calcular frequencia real (considerando virada de oitava)
    current_octave = octave + ((root_idx + interval) // 12)
    f = get_freq(note_name, current_octave)
    
    chord_freqs.append(f)
    chord_notes_names.append(f"{note_name}{current_octave}")

# --- 2. PAINEL INFORMATIVO ---
with col_info:
    # Texto Explicativo Dinâmico
    explanation = ""
    if "Maior" in chord_type_name and "7ª" not in chord_type_name:
        explanation = "O **Acorde Maior** é o pilar da música ocidental. A relação entre as notas (4:5:6 na Justa) é tão estável que nosso cérebro relaxa. É som de 'conclusão' e 'alegria'."
    elif "Menor" in chord_type_name and "7ª" not in chord_type_name:
        explanation = "O **Acorde Menor** tem a terça rebaixada (3 semitons em vez de 4). Essa pequena mudança cria uma 'fricção' suave que associamos à tristeza ou introspecção."
    elif "Diminuto" in chord_type_name:
        explanation = "O **Acorde Diminuto** é pura tensão! Ele tem o intervalo de 'Trítono' (o Diabo na música). Ele pede desesperadamente para ser resolvido em outro acorde."
    else:
        explanation = "Acordes complexos (7ª, Aumentados) adicionam camadas de cor e textura, muito usados em Jazz e MPB para criar atmosferas ricas."

    st.markdown(f"""
    <div class="chord-box {style_class}">
        <h3>{root_note} {chord_type_name.split(' ')[0]}</h3>
        <p>{explanation}</p>
        <hr>
        <p><b>Notas:</b> <span class="big-note">{' - '.join(chord_notes_names)}</span></p>
    </div>
    """, unsafe_allow_html=True)

# --- 3. VISUALIZAÇÃO E ÁUDIO ---
tab_wave, tab_math = st.tabs(["🌊 O Raio-X da Onda", "🧮 A Matemática dos Intervalos"])

with tab_wave:
    c_plot, c_audio = st.columns([3, 1])
    
    with c_plot:
        # Gerar Ondas
        duration = 0.04 # 40ms para ver o detalhe da forma de onda
        sr = 44100
        t = np.linspace(0, duration, int(sr*duration), endpoint=False)
        
        y_sum = np.zeros_like(t)
        
        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor('#0e1117')
        ax.set_facecolor('#0e1117')
        
        colors = ['#FFC107', '#03A9F4', '#4CAF50', '#E91E63']
        
        # Plotar ondas individuais (fantasmas)
        for i, f in enumerate(chord_freqs):
            wave = np.sin(2 * np.pi * f * t)
            y_sum += wave
            ax.plot(t, wave, alpha=0.3, linestyle='--', color=colors[i % len(colors)], label=f'{chord_notes_names[i]} ({f:.1f} Hz)')
            
        # Plotar a Soma (A "Forma" do Acorde)
        ax.plot(t, y_sum, color='white', linewidth=3, label='Soma Resultante')
        
        ax.set_title("Interferência das Ondas (Zoom de 40ms)", color='white')
        ax.axis('off')
        ax.legend(loc='upper right', facecolor='#222', labelcolor='white')
        st.pyplot(fig)
        
        st.caption("As linhas coloridas são as notas individuais. A linha grossa branca é o que seu ouvido recebe: uma onda complexa resultante da soma.")

    with c_audio:
        st.markdown("### 🔊 Ouça")
        
        # Gerar áudio mais longo para tocar
        dur_audio = 2.0
        t_audio = np.linspace(0, dur_audio, int(sr*dur_audio), endpoint=False)
        
        # Inicializa o array vazio
        final_wave = np.zeros_like(t_audio)
        
        # SINTESE: Soma todas as notas do acorde
        num_notas = len(chord_freqs)
        
        for f in chord_freqs:
            # Para cada nota do acorde, adicionamos a fundamental + um harmônico leve (timbre de orgão/piano)
            tone = 0.6 * np.sin(2 * np.pi * f * t_audio)          # Fundamental
            tone += 0.2 * np.sin(2 * np.pi * (f * 2) * t_audio)   # 2º Harmônico (Oitava)
            tone += 0.1 * np.sin(2 * np.pi * (f * 3) * t_audio)   # 3º Harmônico (Quinta)
            
            # Soma ao mix final
            final_wave += tone
        
        # Envelope ADSR Simples para não dar "pop" no começo nem no fim
        # Attack (100ms), Sustain (durante), Release (300ms)
        attack = int(sr * 0.1)
        release = int(sr * 0.3)
        
        env = np.ones_like(final_wave)
        env[:attack] = np.linspace(0, 1, attack)
        env[-release:] = np.linspace(1, 0, release)
        
        final_wave = final_wave * env
        
        # NORMALIZAÇÃO IMPORTANTE:
        # Divide pelo valor máximo absoluto para garantir que fique entre -1.0 e 1.0
        # Adiciona um pequeno epsilon para evitar divisão por zero se for silêncio
        max_val = np.max(np.abs(final_wave))
        if max_val > 0:
            final_wave = final_wave / max_val
            
        # Reduz um pouco o ganho final para evitar distorção nos alto-falantes
        final_wave = final_wave * 0.8
        
        st.audio(final_wave, sample_rate=sr)
        
        if "Maior" in chord_type_name and "7ª" not in chord_type_name:
            st.success("Sente a estabilidade?")
        elif "Diminuto" in chord_type_name:
            st.error("Sente a tensão pedindo socorro?")
        else:
            st.info("Percebe a cor desse som?")

with tab_math:
    st.markdown("### Por que essas notas?")
    st.write("Um acorde é definido pela distância (em semitons) a partir da nota raiz.")
    
    # Criar Tabela Explicativa
    data = []
    for i, interval in enumerate(intervals):
        tipo_intervalo = "Tônica (Raiz)"
        if interval == 3: tipo_intervalo = "3ª Menor (Triste)"
        elif interval == 4: tipo_intervalo = "3ª Maior (Alegre)"
        elif interval == 5: tipo_intervalo = "4ª Justa"
        elif interval == 6: tipo_intervalo = "5ª Diminuta (Tritono/Tensão)"
        elif interval == 7: tipo_intervalo = "5ª Justa (Estabilidade)"
        elif interval == 8: tipo_intervalo = "5ª Aumentada"
        elif interval == 10: tipo_intervalo = "7ª Menor"
        elif interval == 11: tipo_intervalo = "7ª Maior"
        
        data.append({
            "Nota": chord_notes_names[i],
            "Distância (Semitons)": interval,
            "Frequência (Hz)": f"{chord_freqs[i]:.2f}",
            "Função no Acorde": tipo_intervalo
        })
        
    df = pd.DataFrame(data)
    st.table(df)
    
    st.markdown("""
    > **Dica de Ouro:** A nota mais importante para definir se o acorde é "Feliz" ou "Triste" é a **Terça** (a segunda nota da lista).
    > * Se a distância for 4 semitons -> **Maior** (Alegre).
    > * Se a distância for 3 semitons -> **Menor** (Triste).
    """)
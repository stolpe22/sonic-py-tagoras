import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title="Visualizador de Braço", page_icon="🎸", layout="wide")

st.title("🎸 Luthieria: O Braço da Física vs. O Braço Real")

# --- Teoria ---
with st.expander("📚 Aula Teórica: Como se constrói um violão?", expanded=False):
    st.markdown("""
    ### A Regra do 18 (aprox 17.817)
    Para posicionar os trastes de um violão, os luthiers usam uma constante matemática derivada da Raiz de 12.
    
    O objetivo é dividir a oitava em 12 partes iguais (Temperamento Igual). Isso garante que você possa tocar um acorde de Dó Maior e um de Mi Maior e ambos soem "aceitáveis".
    
    **O Preço da Versatilidade:**
    Se afinássemos o violão pela física pura (Just Intonation), os acordes em Dó soariam angelicais, perfeitos. Mas se você tentasse tocar em Ré, soaria como um gato sendo estrangulado (o famoso "Wolf Interval").
    
    O gráfico abaixo mostra onde os trastes ficariam se fossem afinados puramente para a tônica da corda solta.
    """)

# --- Controles ---
st.sidebar.header("Oficina do Luthier")
comprimento_corda = st.sidebar.number_input("Escala (mm)", value=650, step=10, help="Padrão violão clássico: 650mm")
zoom_mode = st.sidebar.checkbox("Modo Microscópio (Zoom)", value=False, help="Foca nas diferenças pequenas")

# --- Lógica ---
# Ratios Justos
just_ratios = [1/1, 16/15, 9/8, 6/5, 5/4, 4/3, 45/32, 3/2, 8/5, 5/3, 9/5, 15/8, 2/1]
nomes = ["Tônica", "2ªm", "2ªM", "3ªm", "3ªM", "4ªJ", "Tri", "5ªJ", "6ªm", "6ªM", "7ªm", "7ªM", "Oitava"]

dados = []
for i in range(13):
    # Temperado (Fórmula de Luthier)
    pos_temp = comprimento_corda * (1 - (1 / (2 ** (i / 12))))
    
    # Justo (Fração Simples)
    pos_just = comprimento_corda * (1 - (1 / just_ratios[i]))
    
    dados.append({"Semitom": i, "Nome": nomes[i], "Sistema": "Temperado (Moderno)", "mm": pos_temp})
    dados.append({"Semitom": i, "Nome": nomes[i], "Sistema": "Natural (Justo)", "mm": pos_just})

df = pd.DataFrame(dados)

# --- Visualização ---
st.divider()

# Gráfico
domain_x = [0, comprimento_corda] if not zoom_mode else [0, 400]

base = alt.Chart(df).encode(
    x=alt.X('mm', scale=alt.Scale(domain=domain_x), title="Distância da Pestana (mm)"),
    y=alt.Y('Sistema', title=None),
    tooltip=['Nome', 'mm', 'Sistema']
)

corda = base.mark_rule(size=2, color="#555")
trastes = base.mark_tick(thickness=3, size=40).encode(
    color=alt.Color('Sistema', legend=None, scale=alt.Scale(range=['#e74c3c', '#3498db'])) # Azul Justo, Vermelho Temp
)
texto = base.mark_text(dy=-25, size=11).encode(text='Nome')

st.altair_chart((corda + trastes + texto).properties(height=300), use_container_width=True)

# --- Tabela de Diferenças ---
st.subheader("📏 A Diferença na Madeira")
st.write("Se você serrasse o braço no lugar errado, essa seria a diferença:")

# Criar tabela comparativa pivotada
df_pivot = df.pivot(index="Nome", columns="Sistema", values="mm")
df_pivot["Diferença (mm)"] = df_pivot["Temperado (Moderno)"] - df_pivot["Natural (Justo)"]
df_pivot = df_pivot.sort_values("Diferença (mm)", ascending=False)

st.dataframe(df_pivot.style.format("{:.2f}").background_gradient(subset=["Diferença (mm)"], cmap="RdBu_r"))
st.info("💡 Note como o Tritono (Tri) e as Terças tem as maiores discrepâncias físicas.")
# 🎵 Sonic Py-tagoras

### Uma Enciclopédia Interativa da Matemática Musical 📐🎻

![Status](https://img.shields.io/badge/Status-Concluído-success)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![Docker](https://img.shields.io/badge/Container-Docker-2496ED)

**Sonic Py-tagoras** é um laboratório de acústica open-source que explora a intersecção entre Física, Matemática e Música.

Este projeto não usa arquivos de áudio gravados (`.mp3`, `.wav`). Todo o som é **sintetizado matematicamente em tempo real** usando Python (NumPy), permitindo que você ouça a diferença exata entre a física pura e a música moderna.

---

## 💡 A Centelha (Origem do Projeto)

> *"Sou Engenheiro de Dados, mas queria ser músico."*

Sempre toquei instrumentos, mas minha carreira seguiu o caminho da engenharia. Recentemente, reencontrei o conceito teórico de **"Afinação Natural vs. Temperada"**. Eu sabia que existia uma diferença matemática entre elas, mas nunca tinha parado para **ouvir** essa diferença na prática.

A curiosidade técnica bateu forte: *"Como eu posso simular esse 'erro' matemático usando código?"*

Decidi unir minhas duas metades. Usei Python para calcular as frequências exatas, `NumPy` para gerar as ondas sonoras vetoriais e `Streamlit` para visualizar a geometria por trás da harmonia. O resultado é este projeto: uma prova de conceito de que a música é, essencialmente, dados vibrando.

---

## 📚 O Que Você Vai Encontrar

O projeto é dividido em 3 pilares educacionais:

### 1. 🧬 A Física (O Som)
* **Série Harmônica (Otimizada):** Visualizador de corda vibrante rodando a **60 FPS** (via HTML5 Canvas) com controles de **velocidade** e **pausa** para análise detalhada.
* **Geometria do Som:** Figuras de Lissajous reagindo a frequências em tempo real.

### 2. 📐 A Matemática (O Problema)
* **O Coma Pitagórico:** Demonstração do "bug" matemático que impede que a música seja cíclica.
* **Geometria Musical:** O Círculo das Quintas visualizado como polígonos. Por que 12 notas?
* **Intervalo do Lobo:** Ouça a dissonância proibida que assombrou músicos por séculos.

### 3. 🎻 A Aplicação (A Música)
* **Piano Comparativo:** Toque e compare a Afinação Justa (Pura) vs. Temperada (Moderna) usando seu **teclado ou mouse**.
* **Laboratório de Acordes:** A física das emoções (Acordes Maiores vs. Menores).
* **Treino Auditivo:** Um game para testar se seu ouvido percebe microtons.

---

## 🛠️ Tech Stack

* **[Streamlit](https://streamlit.io/):** Interface interativa e dashboards.
* **[NumPy](https://numpy.org/):** Síntese de áudio (DSP) e cálculos vetoriais.
* **[Matplotlib](https://matplotlib.org/) & [Altair](https://altair-viz.github.io/):** Visualização de dados estáticos.
* **HTML5 Canvas / JS:** Injeção de scripts para renderização de animações de alta performance no navegador (Client-side).
* **[UV](https://github.com/astral-sh/uv):** Gerenciamento de dependências ultra-rápido.

---

## 🚀 Como Rodar o Projeto

Você pode rodar localmente com Python ou usando Docker.

### Opção A: Rodando com Python (Padrão)

Se você tem o `uv` instalado (recomendado):
```bash
# 1. Clone o repositório
git clone https://github.com/stolpe22/sonic-pytagoras.git
cd sonic-pytagoras

# 2. Instale as dependências e rode
uv run streamlit run app.py
```

Ou usando pip tradicional:
```bash
# 1. Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute
streamlit run app.py
```

### Opção B: Rodando com Docker (Fácil) 🐳

Se você tem Docker e Docker Compose instalados, é só rodar um comando. O projeto já está containerizado.
```bash
# Sobe o container e libera na porta 8501
docker-compose up
```

Acesse no seu navegador: [http://localhost:8501](http://localhost:8501)

---

## 🤝 Contribuição

Curtiu a ideia de misturar código e som? Sinta-se à vontade para abrir Issues ou Pull Requests.

### Ideias para o futuro:
- [ ] Adicionar suporte a MIDI.
- [ ] Visualização de Espectrograma 3D.
- [ ] Simulação de outros temperamentos (Werckmeister, Meantone).

---

Feito com 🐍, 🎵 e curiosidade por Lucas Stolpe.
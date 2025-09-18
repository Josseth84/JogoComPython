import streamlit as st
from PIL import Image
from datetime import datetime
from database import SessionLocal, Resposta

# 🔧 Configuração da página para melhor usabilidade em celulares
st.set_page_config(
    page_title="Minijogo de Inclusão",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicialização do estado da sessão
if 'inicio' not in st.session_state:
    st.session_state.inicio = False
if 'fase' not in st.session_state:
    st.session_state.fase = 1
if 'escolhas' not in st.session_state:
    st.session_state.escolhas = []
if 'tempos' not in st.session_state:
    st.session_state.tempos = []
if 'tempo_inicio' not in st.session_state:
    st.session_state.tempo_inicio = None

# Tela de boas-vindas
if not st.session_state.inicio:
    st.markdown("## 👋 Bem-vindo ao Minijogo de Inclusão")
    st.markdown("""
    Este jogo interativo foi criado para promover empatia, respeito e inclusão de pessoas com autismo no ambiente de trabalho.

    Digite seu nome para começar. Ele será usado para compor o ranking final.
    """)
    nome = st.text_input("🕹️ Nome do jogador:")
    if st.button("🎮 Iniciar minijogo"):
        if nome.strip() == "":
            st.warning("Por favor, digite seu nome para começar.")
        else:
            st.session_state.inicio = True
            st.session_state.nome = nome
            st.session_state.tempo_inicio = datetime.now()
            st.rerun()

# Funções auxiliares
def avancar(escolha):
    tempo_resposta = (datetime.now() - st.session_state.tempo_inicio).total_seconds()
    st.session_state.escolhas.append(escolha)
    st.session_state.tempos.append(tempo_resposta)
    st.session_state.fase += 1
    st.session_state.tempo_inicio = datetime.now()

def mostrar_fase(numero, imagem_path, pergunta, opcao1, opcao2):
    st.image(Image.open(imagem_path), use_column_width=True)
    st.markdown(f"### {pergunta}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(opcao1):
            avancar(opcao1)
    with col2:
        if st.button(opcao2):
            avancar(opcao2)

def salvar_respostas(nome, escolhas, tempos):
    db = SessionLocal()
    for i, (escolha, tempo) in enumerate(zip(escolhas, tempos), start=1):
        resposta = Resposta(
            jogador=nome,
            fase=i,
            escolha=escolha,
            timestamp=datetime.now(),
            tempo_resposta=tempo  # Certifique-se de que essa coluna existe no modelo e no banco
        )
        db.add(resposta)
    db.commit()
    db.close()

def gerar_ranking():
    db = SessionLocal()
    resultados = db.query(
        Resposta.jogador,
        db.func.count(Resposta.id).label("pontuacao")
    ).filter(Resposta.escolha.like("✅%")).group_by(Resposta.jogador).order_by(db.desc("pontuacao")).limit(10).all()
    db.close()
    return resultados

# Fases do minijogo
if st.session_state.fase == 1:
    mostrar_fase(
        1,
        "img/fase1.png",
        "Um colega autista está em silêncio no refeitório. O que você faz?",
        "✅ Convidá-lo para se juntar",
        "❌ Fingir que não viu"
    )

elif st.session_state.fase == 2:
    mostrar_fase(
        2,
        "img/fase2.jpg",
        "Um gestor faz uma piada sobre 'ser estranho'. O que você faz?",
        "✅ Conversar com o gestor sobre respeito",
        "❌ Rir junto para não causar conflito"
    )

elif st.session_state.fase == 3:
    mostrar_fase(
        3,
        "img/fase3.jpg",
        "Um colaborador autista evita contato visual durante uma conversa. O que você faz?",
        "✅ Respeitar seu estilo de comunicação",
        "❌ Insistir para que ele olhe nos seus olhos"
    )

elif st.session_state.fase == 4:
    mostrar_fase(
        4,
        "img/fase4.jpg",
        "A equipe está decidindo quem vai liderar um novo projeto. Um colaborador autista se voluntaria. O que você faz?",
        "✅ Apoiar sua candidatura com confiança",
        "❌ Ignorar e sugerir outro nome"
    )

elif st.session_state.fase == 5:
    mostrar_fase(
        5,
        "img/fase5.jpg",
        "Um colaborador autista pede para trabalhar em um ambiente mais silencioso. O que você faz?",
        "✅ Ajustar o ambiente para reduzir o ruído",
        "❌ Negar o pedido por questões práticas"
    )

# Tela final + ranking + reinício
elif st.session_state.fase > 5:
    st.markdown("## 🧠 Seu perfil de inclusão")
    st.markdown("Você completou todas as fases do minijogo. Aqui estão suas escolhas:")
    for i, escolha in enumerate(st.session_state.escolhas, start=1):
        st.markdown(f"**Fase {i}:** {escolha}")

    if st.button("📤 Enviar respostas"):
        salvar_respostas(st.session_state.nome, st.session_state.escolhas, st.session_state.tempos)
        st.success("Respostas enviadas com sucesso!")

    st.markdown("## 🏆 Ranking dos Jogadores")
    ranking = gerar_ranking()
    for i, r in enumerate(ranking, start=1):
        medalha = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🔹"
        st.markdown(f"{medalha} **{r.jogador}** — {r.pontuacao} escolhas inclusivas")

    if st.button("🔄 Jogar novamente"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
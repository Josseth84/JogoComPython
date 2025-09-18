import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 🎨 Configuração da página
st.set_page_config(page_title="Painel Interativo", layout="wide", page_icon="📊")

# 🏷️ Título principal
st.markdown("## 📊 Painel Interativo – Minijogo de Inclusão")
st.markdown("#### Uma visão analítica sobre escolhas, tempos de resposta e perfis de jogadores")

# 🛠️ Conexão com banco de dados
engine = create_engine('postgresql://jose_user:sua_senha_segura@localhost/jogocompython')
df = pd.read_sql('SELECT * FROM resposta', engine)

# 🔧 Renomear colunas para consistência
df.rename(columns={
    'jogador': 'player_id',
    'fase': 'scenario_id',
    'escolha': 'choice',
    'timestamp': 'response_time'
}, inplace=True)

# ⏱️ Calcular tempo de resposta por fase
df = df.sort_values(by=['player_id', 'scenario_id'])
df['response_time'] = df.groupby('player_id')['response_time'].diff().dt.total_seconds()

# 🎛️ Filtros
with st.expander("🎛️ Filtros de seleção"):
    col1, col2 = st.columns(2)
    with col1:
        player_selecionado = st.selectbox("👤 Selecione o jogador:", df['player_id'].unique())
    with col2:
        fase_selecionada = st.selectbox("🎮 Selecione a fase:", sorted(df['scenario_id'].unique()))

# 📊 Gráficos
st.markdown("### ⏱️ Tempo de resposta e escolhas")
col3, col4 = st.columns(2)

with col3:
    st.markdown("#### Tempo de resposta por fase")
    fig1, ax1 = plt.subplots()
    sns.set_palette("Blues")
    sns.boxplot(x='scenario_id', y='response_time', data=df, ax=ax1)
    ax1.set_xlabel("Fase")
    ax1.set_ylabel("Tempo de Resposta (s)")
    st.pyplot(fig1)

with col4:
    st.markdown("#### Distribuição de escolhas")
    df_fase = df[df['scenario_id'] == fase_selecionada]
    if not df_fase.empty:
        fig2, ax2 = plt.subplots()
        sns.set_palette("Purples")
        sns.countplot(x='choice', data=df_fase, ax=ax2)
        ax2.set_xlabel("Escolha")
        ax2.set_ylabel("Frequência")
        st.pyplot(fig2)
    else:
        st.warning("⚠️ Nenhum dado disponível para a fase selecionada.")

# 🧠 Agrupamento de perfis
st.markdown("### 🧠 Perfis por agrupamento")
X = df[['scenario_id', 'choice', 'response_time']].dropna()
X_encoded = pd.get_dummies(X, columns=['choice'])
X_scaled = StandardScaler().fit_transform(X_encoded)

if X_scaled.shape[0] >= 3:
    kmeans = KMeans(n_clusters=3, random_state=42)
    df.loc[X.index, 'perfil'] = kmeans.fit_predict(X_scaled)
    perfil_counts = df.loc[X.index].groupby('perfil')['player_id'].nunique()
    st.bar_chart(perfil_counts)
    st.markdown("""
    **Interpretação sugerida dos perfis:**
    - Perfil 0 → Colaborador com atitude inclusiva  
    - Perfil 1 → Colaborador em transição (neutro)  
    - Perfil 2 → Colaborador com resistência à inclusão
    """)
else:
    st.warning("⚠️ Dados insuficientes para formar 3 clusters. É necessário pelo menos 3 amostras.")
    df['perfil'] = ['Indefinido'] * df.shape[0]

# 📋 Tabela de respostas
st.markdown("### 📋 Respostas do jogador selecionado")
respostas_jogador = df[df['player_id'] == player_selecionado]
if not respostas_jogador.empty:
    st.dataframe(respostas_jogador)
else:
    st.info("ℹ️ Nenhuma resposta registrada para o jogador selecionado.")

# 📎 Rodapé
st.markdown("---")
st.markdown("**Projeto acadêmico – UNINORTE | Desenvolvido por Jose Ramirez**")
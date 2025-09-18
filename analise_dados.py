# 🔍 ANÁLISE EXPLORATÓRIA DO MINIJOGO
print("\n🔍 INÍCIO DA ANÁLISE EXPLORATÓRIA")
print("-" * 50)

# 📦 Importação de bibliotecas
import pandas as pd
from sqlalchemy import create_engine
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# 🛠️ Conexão com PostgreSQL
engine = create_engine('postgresql://jose_user:sua_senha_segura@localhost/jogocompython')

# 📥 Leitura da tabela
df = pd.read_sql('SELECT * FROM resposta', engine)

# 👀 Visualização inicial
print("\n📄 Primeiros registros:")
print(df.head())

# 📊 Estatísticas descritivas
print("\n📊 Estatísticas descritivas:")
print(df.describe())

# 📈 Distribuição de escolhas
print("\n📈 Distribuição de escolhas:")
print(df['choice'].value_counts())

# ⏱️ Tempo médio por fase
print("\n⏱️ Tempo médio por fase:")
print(df.groupby('scenario_id')['response_time'].mean())

# 📊 Visualização: Boxplot do tempo de resposta por fase
sns.set(style="whitegrid")
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x='scenario_id', y='response_time', data=df, ax=ax)
ax.set_title('Tempo de Resposta por Fase')
ax.set_xlabel('Fase')
ax.set_ylabel('Tempo (segundos)')
plt.tight_layout()
plt.savefig("boxplot_tempo_por_fase.png")
plt.show()

# ✅ Encerramento da análise exploratória
print("\n✅ Fim da análise exploratória. Pronto para avançar para classificação de perfis.")

# 🧠 INÍCIO DA CLASSIFICAÇÃO DE PERFIS
print("\n🧠 INÍCIO DA CLASSIFICAÇÃO DE PERFIS")
print("-" * 50)

# 🔍 Seleção de variáveis relevantes
X = df[['scenario_id', 'choice', 'response_time']].dropna()

# 🧩 Codificação das escolhas
X_encoded = pd.get_dummies(X, columns=['choice'])

# ⚖️ Normalização dos dados
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_encoded)

# 🧪 Aplicação do KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
df.loc[X.index, 'perfil'] = kmeans.fit_predict(X_scaled)

# 📐 Validação dos clusters
score = silhouette_score(X_scaled, df.loc[X.index, 'perfil'])
print(f"\n📐 Silhouette Score: {score:.2f}")

# 📌 Perfis atribuídos
print("\n📌 Perfis atribuídos aos jogadores:")
print(df[['player_id', 'perfil']].drop_duplicates())

# 🧭 Interpretação sugerida
print("\n📋 Interpretação sugerida dos perfis:")
print("Perfil 0 → Colaborador com atitude inclusiva")
print("Perfil 1 → Colaborador em transição (neutro)")
print("Perfil 2 → Colaborador com resistência à inclusão")

# 📤 Exportação dos dados classificados
df.to_csv("dados_classificados.csv", index=False)

# 🔚 Encerramento
print("\n✅ Classificação concluída. Dados prontos para visualização e relatório.")
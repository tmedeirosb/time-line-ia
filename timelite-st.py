import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Carrega a base de dados CSV
df = pd.read_csv('ia_historico.csv')

# Título da página
st.title("A Evolução da Inteligência Artificial")

# Filtro para selecionar por ano
selected_year = st.slider(
    'Selecione o ano:',
    int(df['ano'].min()),
    int(df['ano'].max()),
    int(df['ano'].min())
)

# Filtra a base de dados pelo ano selecionado
df_filtered = df[df['ano'] == selected_year]

# Cria a timeline interativa
st.markdown("## Timeline da IA")
st.markdown("---")

for index, row in df_filtered.iterrows():
    st.markdown(f"**{row['ano']}: {row['título']}**")
    st.markdown(row['descrição'])
    st.markdown("---")

# Gera o histograma da quantidade de artigos publicados por ano
st.markdown("## Artigos Publicados por Ano")
st.markdown("---")

fig, ax = plt.subplots(figsize=(10, 5))
df['ano'].value_counts().sort_index().plot(kind='bar', ax=ax)
ax.set_xlabel("Ano")
ax.set_ylabel("Número de Artigos")
ax.set_title("Histograma de Artigos Publicados por Ano")
st.pyplot(fig)

# Cria a wordcloud
st.markdown("## Palavras-chave da História da IA")
st.markdown("---")

text = " ".join(df['descrição'].astype(str))
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
st.pyplot(plt)
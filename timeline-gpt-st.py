import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit.components.v1 as components

# Carregar a base de dados
df = pd.read_csv('ia_historico.csv')

# Título da aplicação
st.title("Timeline Interativa de IA")

# Filtro por ano
anos = st.multiselect('Selecione o(s) ano(s):', options=df['ano'].unique(), default=df['ano'].unique())

# Filtrando os dados
df_filtrado = df[df['ano'].isin(anos)]

# Função para agrupar por décadas
def get_decade(year):
    return f"{(year // 10) * 10}s"

df_filtrado['década'] = df_filtrado['ano'].apply(get_decade)

# Exibindo a timeline
st.subheader("Timeline de IA")
for decada in sorted(df_filtrado['década'].unique()):
    with st.expander(f"Década de {decada}"):
        decada_df = df_filtrado[df_filtrado['década'] == decada]
        for index, row in decada_df.iterrows():
            st.write(f"**{row['ano']}: {row['título']}**")
            st.write(f"*{row['descrição']}*")

# Gráfico de barras (Histograma)
st.subheader("Histograma de Artigos por Ano")
fig, ax = plt.subplots()
df['ano'].value_counts().sort_index().plot(kind='bar', ax=ax)
ax.set_xlabel("Ano")
ax.set_ylabel("Quantidade de Artigos")
ax.set_title("Quantidade de Artigos Publicados por Ano")
st.pyplot(fig)

# Wordcloud
st.subheader("Wordcloud dos Títulos")
wordcloud_text = ' '.join(df['título'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(wordcloud_text)

fig_wordcloud, ax_wordcloud = plt.subplots()
ax_wordcloud.imshow(wordcloud, interpolation='bilinear')
ax_wordcloud.axis('off')
st.pyplot(fig_wordcloud)

# Visualização HTML com slidedown
st.subheader("Visualização Estática")
with st.expander("Clique aqui para visualizar a timeline"):
    # Carregar o arquivo HTML
    with open('timeline.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    # Renderizar o HTML
    components.html(html_content, height=600, scrolling=True)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit.components.v1 as components
import plotly.express as px
import re

# Função para carregar e processar os dados dos artigos
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    year_data = []
    for line in lines:
        match = re.match(r'.*,"(\d{4})","(\d+)",.*', line)
        if match:
            year = int(match.group(1))
            count = int(match.group(2))
            year_data.append((year, count))

    year_df = pd.DataFrame(year_data, columns=['Year', 'Count'])
    year_df['Decade'] = (year_df['Year'] // 10) * 10
    return year_df.groupby('Decade').sum().reset_index()

# Carregar a base de dados de fatos históricos
df = pd.read_csv('ia_historico.csv')

# Função para agrupar por décadas
def get_decade(year):
    return f"{(year // 10) * 10}s"

df['década'] = df['ano'].apply(get_decade)

# Configuração das abas
tab1, tab2 = st.tabs(["Gráficos de Fatos Históricos", "Artigos"])

# Primeira aba: Gráficos de Fatos Históricos
with tab1:
    st.title("Timeline Interativa de IA")

    # Filtro por ano
    anos = st.multiselect('Selecione o(s) ano(s):', options=df['ano'].unique(), default=df['ano'].unique())

    # Filtrando os dados
    df_filtrado = df[df['ano'].isin(anos)]

    # Exibindo a timeline
    st.subheader("Timeline de IA")
    for decada in sorted(df_filtrado['década'].unique()):
        with st.expander(f"Década de {decada}"):
            decada_df = df_filtrado[df_filtrado['década'] == decada]
            for index, row in decada_df.iterrows():
                st.write(f"**{row['ano']}: {row['título']}**")
                st.write(f"*{row['descrição']}*")

    # Gráfico de barras (Histograma) agrupado por década
    st.subheader("Histograma de Fatos Históricos por Década")
    df['decade'] = (df['ano'] // 10) * 10
    decade_counts = df['decade'].value_counts().sort_index()
    fig, ax = plt.subplots()
    decade_counts.plot(kind='bar', ax=ax)
    ax.set_xlabel("Década")
    ax.set_ylabel("Quantidade de Fatos")
    ax.set_title("Quantidade de Fatos Publicados por Década")
    st.pyplot(fig)

    # Wordcloud
    st.subheader("Wordcloud dos Títulos")
    wordcloud_text = ' '.join(df['título'])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(wordcloud_text)

    fig_wordcloud, ax_wordcloud = plt.subplots()
    ax_wordcloud.imshow(wordcloud, interpolation='bilinear')
    ax_wordcloud.axis('off')
    st.pyplot(fig_wordcloud)

    # # Visualização HTML com slidedown
    # st.subheader("Visualização Estática")
    # with st.expander("Clique aqui para visualizar a timeline"):
    #     # Carregar o arquivo HTML
    #     with open('timeline.html', 'r', encoding='utf-8') as f:
    #         html_content = f.read()
    #     # Renderizar o HTML
    #     components.html(html_content, height=600, scrolling=True)

# Segunda aba: Artigos
with tab2:
    st.title('Artigos produzidos por década. Base de dados: Scopus')

    # Caminho do arquivo CSV
    file_path = 'Scopus_exported_refine_values.csv'

    # Carregar os dados
    decade_df = load_data(file_path)

    # Criação do gráfico usando Plotly
    fig = px.bar(decade_df, x='Decade', y='Count', title='Número de artigos produzidos por década',
                 labels={'Decade': 'Década', 'Count': 'Número de artigos'})

    # Configuração do layout do gráfico
    fig.update_layout(
        xaxis=dict(tickmode='linear', dtick=10),
        yaxis_title='Número de artigos',
        xaxis_title='Década'
    )

    # Exibir o gráfico
    st.plotly_chart(fig)

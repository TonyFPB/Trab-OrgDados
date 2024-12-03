import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#Configuração da página
st.set_page_config(layout='wide')
st.write("# Dashboard Netflix")
st.write("## Análise de Dados sobre Filmes e Séries da Netflix")

# PREPARAÇÃO DOS DADOS
df = pd.read_csv('netflix_titles.csv')

#Limpeza do dataset
dfLimpo = df.copy()

#Substituindo valores nulos
dfLimpo['director'] = dfLimpo['director'].fillna('Desconhecido')
dfLimpo['cast'] = dfLimpo['cast'].fillna('Desconhecido')
dfLimpo['country'] = dfLimpo['country'].fillna('Desconhecido')
dfLimpo['date_added'] = dfLimpo['date_added'].fillna('Desconhecido')
dfLimpo['rating'] = dfLimpo['rating'].fillna('Desconhecido')
dfLimpo['duration'] = dfLimpo['duration'].fillna('Desconhecido')

#Limpando valores de rating
dfLimpo = dfLimpo[dfLimpo['rating'] != '66 min']
dfLimpo = dfLimpo[dfLimpo['rating'] != '74 min']
dfLimpo = dfLimpo[dfLimpo['rating'] != '84 min']


#Preparando o dashboard para adentrar as informações
filme = dfLimpo[dfLimpo['type'] == 'Movie']
serie = dfLimpo[dfLimpo['type'] == 'TV Show']

tipo = st.sidebar.selectbox('Selecione o tipo de dado', ['Filme', 'Série']) #Seleciona o tipo de conteúdo a ser exibido
df_filtred = filme if tipo == 'Filme' else serie

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col5, col6 = st.columns(2)

# Gráfico de barras com a quantidade de filmes e séries por classificação etária
plt.figure(figsize=(10, 6))
ratingLimpo = df_filtred['rating'].value_counts()
sns.barplot(x=ratingLimpo.index, y=ratingLimpo.values, hue=ratingLimpo.index)
plt.title("Classificação etária mais comuns")
plt.xlabel("Classificação")
plt.ylabel("Contagem")
plt.xticks(rotation=45)
col1.pyplot(plt, use_container_width=True)

# Gráfico de barras com o top 15 Gêneros mais populares
generos = df_filtred['listed_in'].str.split(',', expand=True).stack().str.strip().value_counts()

plt.figure(figsize=(12, 8))
sns.barplot(x=generos.values[:15], y=generos.index[:15], hue=generos.index[:15])
plt.title("Top 15 Gêneros Mais Populares")
plt.xlabel("Contagem")
plt.ylabel("Gênero")
col2.pyplot(plt, use_container_width=True)

# Gráfico de barras com a frequencia de duração dos filmes e séries
df_filtred['duration_value'] = df_filtred['duration'].str.extract('([0-9]+)').astype(int)
df_filtred['duration_type'] = df_filtred['duration'].str.extract('([A-Za-z]+)')

plt.figure(figsize=(12, 8))

# Filmes
if tipo == 'Filme':
    sns.histplot(df_filtred['duration_value'], bins=30)
    plt.title("Duração dos Filmes")
    plt.xlabel("Duração (minutos)")
    plt.ylabel("Frequência")
else:  # Séries de TV
    sns.histplot(df_filtred['duration_value'], bins=30)
    plt.title("Temporadas das Séries de TV")
    plt.xlabel("Número de Temporadas")
    plt.ylabel("Frequência")
plt.tight_layout()
col3.pyplot(plt, use_container_width=True)

# Gráfico de barras com a quantidade de filmes e séries por país
paises = df_filtred['country'].str.split(',', expand=True).stack().str.strip().value_counts()

plt.figure(figsize=(12, 8))
sns.barplot(x=paises.values[:15], y=paises.index[:15], hue=paises.index[:15])
plt.title("Top 15 Países com Mais Títulos na Netflix")
plt.xlabel("Contagem")
plt.ylabel("País")
col4.pyplot(plt, use_container_width=True)

# Gráfico de barras com os top 15 atores com mais títulos na Netflix
atores = df_filtred['cast'].str.split(',', expand=True).stack().str.strip().value_counts()

plt.figure(figsize=(12, 8))
sns.barplot(x=atores.values[1:16], y=atores.index[1:16], hue=atores.index[1:16])
plt.title("Top 15 Atores com Mais Títulos na Netflix")
plt.xlabel("Quantidade de Titulos")
plt.ylabel("Atores")
col5.pyplot(plt, use_container_width=True)

plt.figure(figsize=(12, 8))
sns.barplot(x=atores.values[:15], y=atores.index[:15], hue=atores.index[:15])
plt.title("Top 15 Atores com Mais Títulos na Netflix (Com Elenco faltando)")
plt.xlabel("Quantidade de Titulos")
plt.ylabel("Atores")
col6.pyplot(plt, use_container_width=True)
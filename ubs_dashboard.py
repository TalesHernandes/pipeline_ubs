import streamlit as st
import pandas as pd
import plotly.express as px


# Carregar o arquivo atualizado
df = pd.read_csv("ubs_atualizado.csv", sep=";")

# Converter vírgulas para pontos nas colunas de latitude e longitude
df['LATITUDE'] = df['LATITUDE'].str.replace(',', '.').astype(float)
df['LONGITUDE'] = df['LONGITUDE'].str.replace(',', '.').astype(float)

# Contar a frequência de UBS por estado
df_freq = df['Nome_UF'].value_counts().reset_index()
df_freq.columns = ['Estado', 'Frequência']

df_freq_mun = df['Nome_Município'].value_counts().reset_index()
df_freq_mun.columns = ['Nome_Município', 'Frequência']

# Criar o dashboard
st.title("Dashboard de Unidades Básicas de Saúde (UBS)")

# Gráfico de barras
grafico = px.bar(df_freq, x='Estado', y='Frequência', 
                 title='Frequência de UBS por Estado', 
                 labels={'Estado': 'Estado', 'Frequência': 'Número de UBS'},
                 text_auto=True)

st.plotly_chart(grafico)

# Filtro para estados específicos
estados = st.multiselect("Selecione os estados", df_freq['Estado'].unique())
if estados:
    df_filtrado = df[df['Nome_UF'].isin(estados)]
    st.write(df_filtrado)

# Mapa Interativo das UBS por Estado
estados_selecionados = st.multiselect(
    "Selecione os estados para o Mapa Iterativo",
    options=df['Nome_UF'].unique(),
    default=[]
)

df_filtrado = df[df['Nome_UF'].isin(estados_selecionados)]

mapa = px.scatter_map(df_filtrado,
                     lat='LATITUDE',
                     lon='LONGITUDE',
                     hover_name='Nome_UF',
                     zoom=2,
                     title='UBS por Estado'
                     )

mapa.update_traces(cluster=dict(enabled=True))

st.plotly_chart(mapa)

# Gráfico de pizza
grafico_pizza = px.pie(df_freq,
                values='Frequência',
                names='Estado',
                )

st.plotly_chart(grafico_pizza)

# Histograma da Quantidade de UBS por Município
min_ubs = st.slider(
    "Selecione o número mínimo de UBS por município",
    min_value=1,
    max_value=df_freq_mun['Frequência'].max(),
    value=1,
    step=1
)

df_filtrado = df_freq_mun[df_freq_mun['Frequência'] >= min_ubs]

histograma = px.histogram(df_filtrado,
                          x='Nome_Município',
                          y='Frequência', 
                          title=f'Frequência de UBS por Município (Mínimo de {min_ubs} UBS)', 
                          labels={'Nome_Município': 'Município', 'Frequência': 'Número de UBS'},
                          text_auto=True)

histograma.update_layout(xaxis_title="Município", yaxis_title="Número de UBS")

st.plotly_chart(histograma)
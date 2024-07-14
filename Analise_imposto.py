import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# Função para carregar dados
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('arrecadacao-estado.csv', delimiter=';', encoding='latin1')
    except UnicodeDecodeError:
        df = pd.read_csv('arrecadacao-estado.csv', delimiter=';', encoding='cp1252')
    df = df.drop(columns=['IMPOSTO PROVIS.S/ MOVIMENT. FINANC. - IPMF'])
    df.fillna(0, inplace=True)
    df['Ano'] = df['Ano'].astype(int)
    df['Mês'] = df['Mês'].astype(str)
    df['UF'] = df['UF'].astype(str)
    cols_to_convert = df.columns[3:]
    df[cols_to_convert] = df[cols_to_convert].apply(pd.to_numeric, errors='coerce', axis=1)
    return df

# Carregar dados
df = load_data()

# Título do Streamlit App
st.title("Análise de Imposto e Arrecadação por Estado")

# Seleção de estado e ano
estado = st.sidebar.selectbox("Escolha o Estado (UF):", df['UF'].unique())
ano = st.sidebar.selectbox("Escolha o Ano:", df['Ano'].unique())

# Filtrar dados
df_filtrado = df[(df['UF'] == estado) & (df['Ano'] == ano)]

if df_filtrado.empty:
    st.write(f"Não há dados para o estado {estado} no ano {ano}.")
else:
    receita_por_imposto = df_filtrado.iloc[:, 3:].sum()
    
    # Remover valores NaN para evitar erros no gráfico
    receita_por_imposto = receita_por_imposto.dropna()
    
    # Gráfico de Barras
    st.subheader(f'Receita por Tipo de Imposto em {estado} no ano {ano}')
    fig, ax = plt.subplots(figsize=(14, 8))
    receita_por_imposto.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title(f'Receita por Tipo de Imposto em {estado} no ano {ano}')
    ax.set_xlabel('Tipo de Imposto')
    ax.set_ylabel('Receita')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(fig)
    
    # Gráfico de Pizza
    st.subheader(f'Distribuição Percentual de Receita por Tipo de Imposto em {estado} no ano {ano}')
    fig, ax = plt.subplots(figsize=(10, 10))
    receita_por_imposto.plot(kind='pie', ax=ax, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
    ax.set_title(f'Distribuição Percentual de Receita por Tipo de Imposto em {estado} no ano {ano}')
    ax.set_ylabel('')
    st.pyplot(fig)
    
    # Gráfico Interativo de Barras
    st.subheader('Gráfico Interativo de Barras')
    fig = px.bar(receita_por_imposto, title=f'Receita por Tipo de Imposto em {estado} no ano {ano}', labels={'value': 'Receita', 'index': 'Tipo de Imposto'})
    st.plotly_chart(fig)
    
    # Resumo Estatístico
    st.subheader('Resumo Estatístico')
    resumo_estatistico = receita_por_imposto.describe()
    st.write(resumo_estatistico)

    # Correlação
    st.subheader('Matriz de Correlação')
    corr = df_filtrado.select_dtypes(include=[float, int]).corr()
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title(f'Matriz de Correlação para {estado} no ano {ano}')
    st.pyplot(fig)

# Executar o aplicativo
if __name__ == "__main__":
    st.run()

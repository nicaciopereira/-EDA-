
import pandas as pd
import matplotlib.pyplot as plt

# Caminho do arquivo CSV
arquivo_csv = 'Preços semestrais - AUTOMOTIVOS_2023.02.csv' 

# Definindo os tipos de dados esperados para cada coluna
dtype_dict = {
    'Regiao - Sigla': 'str',
    'Estado - Sigla': 'str',
    'Municipio': 'str',
    'Revenda': 'str',
    'CNPJ da Revenda': 'str',
    'Nome da Rua': 'str', 
    'Numero Rua': 'str',
    'Complemento': 'str',
    'Bairro': 'str',
    'Cep': 'str',
    'Produto': 'str',
    'Data da Coleta': 'str',  # Converteremos para datetime posteriormente
    'Valor de Venda': 'str',  # Converteremos para float posteriormente
    'Valor de Compra': 'str',
    'Unidade de Medida': 'str',
    'Bandeira': 'str'
}

try:
    # Leitura do arquivo CSV com delimitador ;
    df = pd.read_csv(arquivo_csv, delimiter=';', on_bad_lines='skip', dtype=dtype_dict, low_memory=False)
    
    # Filtrar os dados para incluir apenas gasolina comum em postos de São Paulo
    df_gasolina_sp = df.loc[(df['Produto'] == 'GASOLINA') & (df['Estado - Sigla'] == 'SP')].copy()
    
    # Visualizar as primeiras linhas do DataFrame filtrado
    print("\nPrimeiras linhas do DataFrame filtrado para gasolina comum em postos de São Paulo:")
    print(df_gasolina_sp.head())
    
except Exception as e:
    print(f"Erro ao ler o arquivo CSV: {e}")
    print()

# Tratamento de dados ausentes
df_gasolina_sp.dropna(subset=['Valor de Venda'], inplace=True)

# Conversão de tipos de dados
df_gasolina_sp['Valor de Venda'] = df_gasolina_sp['Valor de Venda'].str.replace(',', '.').astype(float)

# Tratamento de valores duplicados
df_gasolina_sp.drop_duplicates(inplace=True)

# Conversão de data
df_gasolina_sp['Data da Coleta'] = pd.to_datetime(df_gasolina_sp['Data da Coleta'], dayfirst=True)

# Ordenar pelo campo de data
df_gasolina_sp.sort_values('Data da Coleta', inplace=True)

# Visualizar informações gerais do DataFrame após o pré-processamento
print("\nInformações gerais do DataFrame após o pré-processamento:")
print(df_gasolina_sp.info())

# Visualizar estatísticas descritivas dos preços de venda
print("\nEstatísticas descritivas dos preços de venda:")
print(df_gasolina_sp['Valor de Venda'].describe())

# Visualizar as primeiras linhas do DataFrame após o pré-processamento
print("\nPrimeiras linhas do DataFrame após o pré-processamento:")
print(df_gasolina_sp.head())

# Análise Exploratória

# Histograma dos preços de venda
plt.figure(figsize=(10, 6))
plt.hist(df_gasolina_sp['Valor de Venda'], bins=20, color='skyblue', edgecolor='black')
plt.title('Distribuição dos Preços de Venda da Gasolina Comum em São Paulo')
plt.xlabel('Preço de Venda (R$/litro)')
plt.ylabel('Frequência')
plt.grid(True)
plt.show()

# Boxplot para identificar outliers
plt.figure(figsize=(10, 6))
plt.boxplot(df_gasolina_sp['Valor de Venda'], vert=False)
plt.title('Boxplot dos Preços de Venda da Gasolina Comum em São Paulo')
plt.xlabel('Preço de Venda (R$/litro)')
plt.show()

# Gráfico de linhas da evolução dos preços ao longo do tempo
plt.figure(figsize=(12, 6))
plt.plot(df_gasolina_sp['Data da Coleta'], df_gasolina_sp['Valor de Venda'], marker='o', linestyle='-', color='b')
plt.title('Evolução dos Preços de Venda da Gasolina Comum em São Paulo')
plt.xlabel('Data')
plt.ylabel('Preço de Venda (R$/litro)')
plt.grid(True)
plt.xticks(rotation=45)
plt.show()

# Salvando o DataFrame preprocessado para uso futuro
df_gasolina_sp.to_csv('gasolina_sp_preprocessado.csv', index=False)

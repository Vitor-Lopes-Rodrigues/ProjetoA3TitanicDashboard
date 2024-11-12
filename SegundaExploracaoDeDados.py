# Obs: Pelo código ser feito no Pycharm, tivemos que fazer algumas adaptações em  relação
# a resposta feita, com isso em mente note que substituimos o "display" por "print".
# Mas se caso rodar exclussivamente este caso no COLAB, ele irá funcionar com as tabelas também, só que estilizadas

import pandas as pd

# Carregamento do conjunto de dados Titanic
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
titanic = pd.read_csv(url)

# Renomeando as colunas
titanic.columns = [
    'ID_Passageiro', 'Sobreviveu', 'Classe', 'Nome', 'Sexo',
    'Idade', 'Irmãos_Cônjuges', 'Pais_Filhos', 'Bilhete',
    'Tarifa', 'Cabine', 'Embarque'
]

# Dicionário de descrição das colunas
colunas = {
    'Sobreviveu': 'Sobreviveu (0 = não, 1 = sim) (qualitativa binária)',
    'Classe': 'Classe do passageiro (qualitativa ordinal)',
    'Sexo': 'Sexo do passageiro (masculino ou feminino) (qualitativa binária)',
    'Embarque': 'Porto de embarque (qualitativa ordinal)'
}

# Criando o DataFrame de descrição
descricao_df = pd.DataFrame(list(colunas.items()), columns=['Coluna', 'Descrição'])

# Exibindo o DataFrame de descrição como texto
print("\nDescrição das Colunas do Conjunto de Dados:")
print(descricao_df.to_string(index=False))

# Análise das variáveis qualitativas
qualitativas = ['Sobreviveu', 'Classe', 'Sexo', 'Embarque']
for coluna in qualitativas:
    print(f"\nTabela de frequências para {coluna}:")

    # Calculando frequências absolutas e relativas
    frequencias_absolutas = titanic[coluna].value_counts().reset_index()
    frequencias_absolutas.columns = [coluna, 'Frequência Absoluta']

    frequencias_relativas = (titanic[coluna].value_counts(normalize=True) * 100).reset_index()
    frequencias_relativas.columns = [coluna, 'Frequência Relativa (%)']

    # Juntando frequências absolutas e relativas
    resultado = pd.merge(frequencias_absolutas, frequencias_relativas, on=coluna)

    # Exibindo a tabela de frequências como texto
    print(resultado.to_string(index=False))

# Análise das variáveis quantitativas
quantitativas = ['Idade', 'Irmãos_Cônjuges', 'Pais_Filhos', 'Tarifa']
for coluna in quantitativas:
    print(f"\nEstatísticas descritivas para {coluna}:")

    # Calculando estatísticas descritivas
    media = titanic[coluna].mean()
    mediana = titanic[coluna].median()
    moda = titanic[coluna].mode()[0] if not titanic[coluna].mode().empty else None
    quartis = titanic[coluna].quantile([0.25, 0.5, 0.75])
    desvio_padrao = titanic[coluna].std()
    amplitude = titanic[coluna].max() - titanic[coluna].min()

    # Exibindo estatísticas
    print(f"Média: {media:.2f}")
    print(f"Mediana: {mediana:.2f}")
    print(f"Moda: {moda:.2f}" if moda is not None else "Moda: Nenhuma")
    print(f"Quartis:\n{quartis}")
    print(f"Desvio padrão: {desvio_padrao:.2f}")
    print(f"Amplitude: {amplitude:.2f}")

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output

# IMPORTANDO DADOS DO TITANIC
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
titanic = pd.read_csv(url)

# FAZENDO AS LIMPEZAS E AJUSTES
titanic['Age'] = titanic['Age'].fillna(titanic['Age'].mean()).round(0).astype(int)  # Arredondando a idade para inteiro
titanic['Embarked'] = titanic['Embarked'].fillna(titanic['Embarked'].mode()[0])
titanic = titanic.drop(columns=['Cabin'])

titanic['Sex'] = titanic['Sex'].map({'male': 'Masculino', 'female': 'Feminino'})
titanic['Embarked'] = titanic['Embarked'].map({'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'})

titanic['Pclass'] = titanic['Pclass'].map({1: 'Primeira Classe', 2: 'Segunda Classe', 3: 'Terceira Classe'})

# Renomeando colunas para português
titanic.rename(columns={
    'Survived': 'Sobreviveu',
    'Pclass': 'Classe',
    'Sex': 'Sexo',
    'Age': 'Idade',
    'SibSp': 'Irmãos/Cônjuges a Bordo',
    'Parch': 'Pais/Filhos a Bordo',
    'Fare': 'Tarifa',
    'Embarked': 'Embarque',
    'PassengerId': 'ID Passageiro',
    'Name': 'Nome',
    'Ticket': 'Bilhete'
}, inplace=True)


def gerar_grafico(tipo_grafico):
    if tipo_grafico == 'barras':
        taxa_sobrevivencia = titanic.groupby('Sexo')['Sobreviveu'].mean().reset_index()
        taxa_sobrevivencia['Sobreviveu'] *= 100

        fig = px.bar(taxa_sobrevivencia, x='Sexo', y='Sobreviveu', color='Sexo',
                     labels={'Sexo': 'Gênero', 'Sobreviveu': 'Taxa de Sobrevivência (%)'},
                     title='Taxa de Sobrevivência por Gênero')

    elif tipo_grafico == 'tarifa_classe':
        fig = px.box(titanic, x='Classe', y='Tarifa', color='Classe',
                     labels={'Classe': 'Classe', 'Tarifa': 'Tarifa'},
                     title='Distribuição de Tarifas por Classe')

    elif tipo_grafico == 'distribuicao_idade':
        fig = px.histogram(titanic, x='Idade', nbins=20,
                           labels={'Idade': 'Idade', 'count': 'Número de Passageiros'},
                           title='Distribuição da Idade dos Passageiros')

    elif tipo_grafico == 'sobrevivencia_classe':
        taxa_sobrevivencia_classe = titanic.groupby('Classe')['Sobreviveu'].mean().reset_index()
        taxa_sobrevivencia_classe['Sobreviveu'] *= 100

        fig = px.bar(taxa_sobrevivencia_classe, x='Classe', y='Sobreviveu',
                     labels={'Classe': 'Classe', 'Sobreviveu': 'Taxa de Sobrevivência (%)'},
                     title='Taxa de Sobrevivência por Classe')

    elif tipo_grafico == 'proporcao_sobreviventes':
        prop_sobreviventes = titanic['Sobreviveu'].value_counts().reset_index()
        prop_sobreviventes.columns = ['Sobrevivência', 'Count']
        prop_sobreviventes['Sobrevivência'] = prop_sobreviventes['Sobrevivência'].map(
            {0: 'Não Sobreviveu', 1: 'Sobreviveu'})

        fig = px.bar(prop_sobreviventes, x='Count', y='Sobrevivência', orientation='h',
                     labels={'Count': 'Número de Passageiros'},
                     title='Número de Sobreviventes vs Não Sobreviventes')

    elif tipo_grafico == 'tarifa_sobrevivencia':
        fig = px.box(titanic, x='Sobreviveu', y='Tarifa', color='Sobreviveu',
                     labels={'Sobreviveu': 'Sobreviventes', 'Tarifa': 'Tarifa'},
                     title='Distribuição de Tarifa por Sobrevivência')

    elif tipo_grafico == 'sobrevivencia_faixa_etaria':
        taxa_sobrevivencia_idade = titanic.groupby('FaixaEtaria')['Sobreviveu'].mean().reset_index()
        taxa_sobrevivencia_idade['Sobreviveu'] *= 100

        fig = px.bar(taxa_sobrevivencia_idade, x='FaixaEtaria', y='Sobreviveu',
                     labels={'FaixaEtaria': 'Faixa Etária', 'Sobreviveu': 'Taxa de Sobrevivência (%)'},
                     title='Taxa de Sobrevivência por Faixa Etária')

    elif tipo_grafico == 'tarifa_idade':
        fig = px.scatter(titanic, x='Idade', y='Tarifa', color='Classe',
                         labels={'Idade': 'Idade', 'Tarifa': 'Tarifa', 'Classe': 'Classe'},
                         title='Relação entre Idade e Tarifa')

    else:
        fig = {}

    return fig


app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div(style={'backgroundColor': '#f7f7f7', 'padding': '20px'}, children=[

    html.H1('Projeto A3 2024 - Titanic Dashboard', style={'textAlign': 'center', 'color': '#4a4a4a'}),

    html.Div(style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '40px'}, children=[

        html.Div(style={'width': '30%', 'padding': '10px', 'border': '1px solid #dcdcdc', 'borderRadius': '10px'},
                 children=[
                     html.H4('Selecione o tipo de gráfico', style={'textAlign': 'center'}),
                     dcc.Dropdown(
                         id='grafico-selecao',
                         options=[
                             {'label': 'Taxa de Sobrevivência por Gênero (Barras)', 'value': 'barras'},
                             {'label': 'Distribuição de Tarifas por Classe (Boxplot)', 'value': 'tarifa_classe'},
                             {'label': 'Distribuição da Idade (Histograma)', 'value': 'distribuicao_idade'},
                             {'label': 'Taxa de Sobrevivência por Classe (Barras)', 'value': 'sobrevivencia_classe'},
                             {'label': 'Número de Sobreviventes vs Não Sobreviventes (Barras)', 'value': 'proporcao_sobreviventes'},
                             {'label': 'Distribuição de Tarifas por Sobrevivência (Boxplot)', 'value': 'tarifa_sobrevivencia'},
                             {'label': 'Taxa de Sobrevivência por Faixa Etária (Barras)', 'value': 'sobrevivencia_faixa_etaria'},
                             {'label': 'Relação entre Idade e Tarifa (Dispersão)', 'value': 'tarifa_idade'}
                         ],
                         value='barras',
                         clearable=False,
                         style={'marginBottom': '20px'}
                     ),
                     dcc.Graph(id='grafico-gerado')
                 ])
    ]),

    html.Div(style={'padding': '20px', 'border': '1px solid #dcdcdc', 'borderRadius': '10px'}, children=[
        html.H3('Lista de Dados do Titanic', style={'textAlign': 'center'}),
        dash_table.DataTable(
            id='tabela-dados',
            columns=[{"name": col, "id": col} for col in titanic.columns],
            data=titanic.to_dict('records'),
            page_size=10,
            style_table={
                'overflowX': 'auto',
                'border': '1px solid #dcdcdc',
                'borderRadius': '10px',
                'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'
            },
            style_header={
                'backgroundColor': '#4a4a4a',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center'
            },
            style_data={
                'backgroundColor': '#f9f9f9',
                'color': '#00000',
                'textAlign': 'center',
                'font-weight': 'bold'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#e6e6e6'
                }
            ],
            style_cell={
                'textAlign': 'center',
                'minWidth': '100px',
                'width': '150px',
                'maxWidth': '200px',
                'whiteSpace': 'normal',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis'
            }
        )
    ])
])


@app.callback(
    Output('grafico-gerado', 'figure'),
    Input('grafico-selecao', 'value')
)
def atualizar_grafico(tipo_grafico):
    return gerar_grafico(tipo_grafico)


if __name__ == '__main__':
    app.run_server(debug=True)

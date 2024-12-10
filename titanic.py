import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
titanic = pd.read_csv(url)
titanic['Age'].fillna(titanic['Age'].mean(), inplace=True)
titanic['Age'] = titanic['Age'].round(0).astype(int)
titanic['Embarked'].fillna(titanic['Embarked'].mode()[0], inplace=True)
titanic.drop(columns=['Cabin'], inplace=True)
titanic['Sex'] = titanic['Sex'].map({'male': 'Masculino', 'female': 'Feminino'})
titanic['Embarked'] = titanic['Embarked'].map({'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'})
titanic['Pclass'] = titanic['Pclass'].map({1: 'Primeira Classe', 2: 'Segunda Classe', 3: 'Terceira Classe'})

def gerar_grafico(tipo_grafico):
    try:
        if tipo_grafico == 'barras':
            taxa_sobrevivencia = titanic.groupby('Sex', observed=False)['Survived'].mean().reset_index()
            taxa_sobrevivencia['Survived'] *= 100
            fig = px.bar(taxa_sobrevivencia, x='Sex', y='Survived', color='Sex',
                         labels={'Sex': 'Gênero', 'Survived': 'Taxa de Sobrevivência (%)'},
                         title='Taxa de Sobrevivência por Gênero')

        elif tipo_grafico == 'tarifa_classe':
            fig = px.box(titanic, x='Pclass', y='Fare', color='Pclass',
                         labels={'Pclass': 'Classe', 'Fare': 'Tarifa'},
                         title='Distribuição de Tarifas por Classe')

        elif tipo_grafico == 'distribuicao_idade':
            fig = px.histogram(titanic, x='Age', nbins=20,
                               labels={'Age': 'Idade', 'count': 'Número de Passageiros'},
                               title='Distribuição da Idade dos Passageiros')

        elif tipo_grafico == 'sobrevivencia_classe':
            taxa_sobrevivencia_classe = titanic.groupby('Pclass', observed=False)['Survived'].mean().reset_index()
            taxa_sobrevivencia_classe['Survived'] *= 100
            fig = px.bar(taxa_sobrevivencia_classe, x='Pclass', y='Survived',
                         labels={'Pclass': 'Classe', 'Survived': 'Taxa de Sobrevivência (%)'},
                         title='Taxa de Sobrevivência por Classe')

        elif tipo_grafico == 'proporcao_sobreviventes':
            prop_sobreviventes = titanic['Survived'].value_counts().reset_index()
            prop_sobreviventes.columns = ['Sobrevivência', 'Count']
            prop_sobreviventes['Sobrevivência'] = prop_sobreviventes['Sobrevivência'].map(
                {0: 'Não Sobreviveu', 1: 'Sobreviveu'})
            fig = px.bar(prop_sobreviventes, x='Count', y='Sobrevivência', orientation='h',
                         labels={'Count': 'Número de Passageiros'},
                         title='Número de Sobreviventes vs Não Sobreviventes')

        elif tipo_grafico == 'tarifa_sobrevivencia':
            fig = px.box(titanic, x='Survived', y='Fare', color='Survived',
                         labels={'Survived': 'Sobreviventes', 'Fare': 'Tarifa'},
                         title='Distribuição de Tarifa por Sobrevivência')

        elif tipo_grafico == 'sobrevivencia_faixa_etaria':
            bins = [0, 12, 18, 35, 60, 80]
            labels = ['Criança', 'Adolescente', 'Adulto Jovem', 'Adulto', 'Idoso']
            titanic['FaixaEtaria'] = pd.cut(titanic['Age'], bins=bins, labels=labels)
            taxa_sobrevivencia_idade = titanic.groupby('FaixaEtaria', observed=False)['Survived'].mean().reset_index()
            taxa_sobrevivencia_idade['Survived'] *= 100
            fig = px.bar(taxa_sobrevivencia_idade, x='FaixaEtaria', y='Survived',
                         labels={'FaixaEtaria': 'Faixa Etária', 'Survived': 'Taxa de Sobrevivência (%)'},
                         title='Taxa de Sobrevivência por Faixa Etária')

        elif tipo_grafico == 'tarifa_idade':
            fig = px.scatter(titanic, x='Age', y='Fare', color='Pclass',
                             labels={'Age': 'Idade', 'Fare': 'Tarifa', 'Pclass': 'Classe'},
                             title='Relação entre Idade e Tarifa')

        else:
            raise ValueError("Tipo de gráfico inválido.")
        return fig

    except Exception as e:
        print(f"Erro ao gerar gráfico {tipo_grafico}: {e}")
        return px.scatter(title=f"Erro ao gerar gráfico {tipo_grafico}")


colunas_traduzidas = {
    "PassengerId": "ID Passageiro",
    "Survived": "Sobreviveu",
    "Pclass": "Classe",
    "Name": "Nome",
    "Sex": "Sexo",
    "Age": "Idade",
    "SibSp": "Cônjuges/Irmãos",
    "Parch": "Pais/Filhos",
    "Ticket": "Bilhete",
    "Fare": "Tarifa",
    "Embarked": "Embarque",
    "FaixaEtaria": "Faixa Etária",
}


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.NavbarSimple(
        brand="Projeto A3",
        color="dark",
        dark=True,
        className="mb-4"
    ),
    html.Div([
        html.H1("Se Aventurando Pelo Titanic", className="text-center mb-4", style={"fontWeight": "bold"}),
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("Total de Passageiros", className="card-title text-center"),
                    html.H4(f"{len(titanic)}", className="card-text text-center")
                ])
            ], color="info", inverse=True, style={"boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"}), width=2),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("Sobreviventes (%)", className="card-title text-center"),
                    html.H4(f"{(titanic['Survived'].mean() * 100):.2f}%", className="card-text text-center")
                ])
            ], color="success", inverse=True, style={"boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"}), width=2),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("Idade Média", className="card-title text-center"),
                    html.H4(f"{titanic['Age'].mean():.1f}", className="card-text text-center")
                ])
            ], color="primary", inverse=True, style={"boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"}), width=2),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("Passageiros Masculinos", className="card-title text-center"),
                    html.H4(f"{(titanic['Sex'] == 'Masculino').sum()}", className="card-text text-center")
                ])
            ], color="warning", inverse=True, style={"boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"}), width=2),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("Passageiros Femininos", className="card-title text-center"),
                    html.H4(f"{(titanic['Sex'] == 'Feminino').sum()}", className="card-text text-center")
                ])
            ], color="danger", inverse=True, style={"boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"}), width=2),
        ], justify="center", className="mb-4"),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Tabs(
                            [
                                dbc.Tab(label="Dashboard", tab_id="dashboard"),
                                dbc.Tab(label="Tabela", tab_id="tabela"),
                            ],
                            id="toggle-view",
                            active_tab="dashboard",
                            className="mb-3",
                        )
                    ], className="text-center")
                ])
            ]),
            html.Div(id="view-container", children=[
                dbc.Row([
                    dbc.Col(dcc.Graph(figure=gerar_grafico('barras')), width=6),
                    dbc.Col(dcc.Graph(figure=gerar_grafico('tarifa_classe')), width=6),
                ]),
                dbc.Row([
                    dbc.Col(dcc.Graph(figure=gerar_grafico('distribuicao_idade')), width=6),
                    dbc.Col(dcc.Graph(figure=gerar_grafico('sobrevivencia_classe')), width=6),
                ]),
                dbc.Row([
                    dbc.Col(dcc.Graph(figure=gerar_grafico('proporcao_sobreviventes')), width=6),
                    dbc.Col(dcc.Graph(figure=gerar_grafico('tarifa_sobrevivencia')), width=6),
                ]),
                dbc.Row([
                    dbc.Col(dcc.Graph(figure=gerar_grafico('sobrevivencia_faixa_etaria')), width=6),
                    dbc.Col(dcc.Graph(figure=gerar_grafico('tarifa_idade')), width=6),
                ]),
            ], style={"margin": "20px"}),
        ]),
    ], style={"textAlign": "center", "padding": "0 100px"}),
    html.Div(id="table-container", children=[
        dash_table.DataTable(
            id='tabela-dados',
            columns=[{"name": colunas_traduzidas[i], "id": i} for i in titanic.columns],
            data=titanic.to_dict('records'),
            page_size=20,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'}
        )
    ], style={"padding": "0 100px"}),
], style={"backgroundColor": "#F6F6F6", "minHeight": "100vh", "margin": "0"})

@app.callback(
    [Output("view-container", "style"),
     Output("table-container", "style")],
    Input("toggle-view", "active_tab"),
)

def alternar_view(toggle_value):
    if toggle_value == "tabela":
        return {"display": "none"}, {"display": "block", "padding": "0 100px"}
    else:
        return {"display": "block"}, {"display": "none", "padding": "0 100px"}

if __name__ == '__main__':
    app.run_server(debug=True)

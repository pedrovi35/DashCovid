import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import plotly.express as px
import pandas as pd
import io # Para ler a string de dados como um arquivo

# --- 1. Preparação dos Dados ---
# Dados fornecidos como uma string multi-linha
data_string = """Regiao/Unidade da Federacao,Internacoes,Taxa_mortalidade,Obitos,Valor_total
Regiao Norte,5358594,3.47,186173,6045855298
Rondonia,610193,3.56,21721,704313849.4
Acre,263235,3.66,9624,253052891.4
Amazonas,1059101,4.11,43487,1255118657
Roraima,212716,3.71,7882,212217841
Para,2522279,3.09,77845,2852346275
Amapa,232374,3.27,7609,211815713.6
Tocantins,458696,3.93,18005,556990069.3
Regiao Nordeste,16538523,4.5,743596,24222319611
Maranhao,2309097,3.24,74767,2394472344
Piaui,1057251,4.03,42609,1330149880
Ceara,2662931,4.68,124678,3938833104
Rio Grande do Norte,967456,4.25,41142,1749938104
Paraiba,1046775,5.64,58996,1781345374
Pernambuco,2965655,5.02,148959,5180771133
Alagoas,802875,4.93,39588,1205717331
Sergipe,534097,5.52,29469,851894922.3
Bahia,4192386,4.37,183388,5789197418
Regiao Sudeste,24839236,6.05,1501643,45232930366
Minas Gerais,6773852,5.37,363795,12601187552
Espirito Santo,1371215,4.58,62776,2426729593
Rio de Janiero,4032040,7.64,307915,6968312097
Sao Paulo,12662129,6.06,767157,23236701124
Regiao Sul,10969014,5.33,584324,21524131329
Parana,4409778,4.96,218840,8960437448
Santa Catarina,2715768,4.8,130466,5498121203
Rio Grande do Sul,3843468,6.11,235018,7065572678
Regiao Centro-Oeste,5074544,4.21,213553,7632678349
Mato Grosso do Sul,951289,4.9,46648,1537264961
Mato Grosso,1053818,3.92,41342,1401060282
Goias,1892484,4.52,85602,2996584122
Distrito Federal,1176953,3.4,39961,1697768984
Total,62779911,5.14,3229289,1.05E+11
"""

# Usar io.StringIO para ler a string como se fosse um arquivo CSV
data_io = io.StringIO(data_string)
df = pd.read_csv(data_io)

# Renomear colunas para facilitar o acesso (sem espaços, acentos)
df.columns = ['localidade', 'internacoes', 'taxa_mortalidade', 'obitos', 'valor_total']

# Converter colunas numéricas
numeric_cols = ['internacoes', 'taxa_mortalidade', 'obitos', 'valor_total']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce') # errors='coerce' transforma erros em NaN

# Identificar Regiões e Estados
df['tipo'] = df['localidade'].apply(lambda x: 'Região' if x.startswith('Regiao') else ('Total' if x == 'Total' else 'Estado'))

# Separar os dataframes
df_total = df[df['tipo'] == 'Total'].iloc[0] # Pegar a linha de totais como uma Series
df_regioes = df[df['tipo'] == 'Região'].copy()
df_estados = df[df['tipo'] == 'Estado'].copy()

# Mapear estados para suas regiões (para possível uso futuro, como filtros ou cores)
region_map = {}
current_region = None
for index, row in df.iterrows():
    if row['tipo'] == 'Região':
        current_region = row['localidade']
    elif row['tipo'] == 'Estado':
        region_map[row['localidade']] = current_region

df_estados['regiao'] = df_estados['localidade'].map(region_map)

# --- 2. Inicialização do App Dash ---
# Usar um tema escuro do Bootstrap (ex: DARKLY, CYBORG, SOLAR)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}] # Responsividade
                )
server = app.server # Para deploy (ex: Heroku)

# --- 3. Layout do Dashboard ---
app.layout = dbc.Container([
    # Linha 1: Título e Período
    dbc.Row(
        dbc.Col(html.H1("Dashboard COVID-19 - Brasil", className='text-center text-primary mb-4'), width=12)
    ),
    dbc.Row(
        dbc.Col(html.P("Período de Análise (Dados Agregados): Fev/2020 - Fev/2025*", className='text-center text-muted'), width=12)
    ),
     dbc.Row(
        dbc.Col(html.P("*Nota: Os dados apresentados são agregados e refletem os totais consolidados, não uma série temporal detalhada mês a mês até Fev/2025.",
                       className='text-center text-info fst-italic small'), width=12)
    ),

    # Linha 2: KPIs (Indicadores Chave de Desempenho)
    dbc.Row([
        dbc.Col(dbc.Card([
                    dbc.CardHeader("Total de Internações"),
                    dbc.CardBody(f"{df_total['internacoes']:,.0f}".replace(",", ".")) # Formatação PT-BR
                ], color="info", inverse=True, className='text-center mb-2'), lg=3, md=6),
        dbc.Col(dbc.Card([
                    dbc.CardHeader("Total de Óbitos"),
                    dbc.CardBody(f"{df_total['obitos']:,.0f}".replace(",", "."))
                ], color="danger", inverse=True, className='text-center mb-2'), lg=3, md=6),
        dbc.Col(dbc.Card([
                    dbc.CardHeader("Taxa de Mortalidade Média (%)"),
                    dbc.CardBody(f"{df_total['taxa_mortalidade']:.2f}".replace(".", ","))
                ], color="warning", inverse=True, className='text-center mb-2'), lg=3, md=6),
        dbc.Col(dbc.Card([
                    dbc.CardHeader("Custo Total Estimado (R$)"),
                    dbc.CardBody(f"R$ {df_total['valor_total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")) # Formatação PT-BR
                ], color="success", inverse=True, className='text-center mb-2'), lg=3, md=6),
    ], className='mb-4'),

    # Linha 3: Controles (Dropdown para selecionar métrica)
    dbc.Row([
        dbc.Col([
            html.Label("Selecione a Métrica para Visualização:", className="fw-bold"),
            dcc.Dropdown(
                id='metric-selector',
                options=[
                    {'label': 'Internações', 'value': 'internacoes'},
                    {'label': 'Óbitos', 'value': 'obitos'},
                    {'label': 'Taxa de Mortalidade (%)', 'value': 'taxa_mortalidade'},
                    {'label': 'Custo Total (R$)', 'value': 'valor_total'}
                ],
                value='obitos', # Valor inicial
                clearable=False,
                className='mb-3' # Adiciona margem inferior
            )
        ], width=12)
    ]),

    # Linha 4: Gráficos (Regiões e Estados)
    dbc.Row([
        # Coluna para Gráfico de Regiões
        dbc.Col([
            html.H4("Visão por Região", className="text-center"),
            dcc.Graph(id='graph-regioes', figure={}) # Figura inicial vazia
        ], lg=6, md=12, className='mb-4'), # lg=6 (metade em telas grandes), md=12 (largura total em médias/pequenas)

        # Coluna para Gráfico de Estados
        dbc.Col([
            html.H4("Visão por Estado", className="text-center"),
            dcc.Graph(id='graph-estados', figure={}) # Figura inicial vazia
        ], lg=6, md=12, className='mb-4'),
    ])

], fluid=True) # fluid=True usa a largura total da tela

# --- 4. Callbacks para Interatividade ---
@app.callback(
    [Output('graph-regioes', 'figure'),
     Output('graph-estados', 'figure')],
    [Input('metric-selector', 'value')]
)
def update_graphs(selected_metric):
    # Mapear valor da métrica para um título legível
    metric_labels = {
        'internacoes': 'Internações',
        'obitos': 'Óbitos',
        'taxa_mortalidade': 'Taxa de Mortalidade (%)',
        'valor_total': 'Custo Total (R$)'
    }
    readable_metric_name = metric_labels.get(selected_metric, selected_metric.replace('_', ' ').title())

    # Gráfico 1: Regiões
    df_regioes_sorted = df_regioes.sort_values(by=selected_metric, ascending=False)
    fig_regioes = px.bar(
        df_regioes_sorted,
        x='localidade',
        y=selected_metric,
        title=f'{readable_metric_name} por Região',
        labels={'localidade': 'Região', selected_metric: readable_metric_name},
        template='plotly_dark', # Aplicar tema escuro ao gráfico
        text_auto=True # Mostra o valor em cima da barra
    )
    fig_regioes.update_traces(textposition='outside') # Coloca o texto fora da barra
    fig_regioes.update_layout(xaxis_title=None, title_x=0.5) # Centralizar título

    # Gráfico 2: Estados
    df_estados_sorted = df_estados.sort_values(by=selected_metric, ascending=False)
    fig_estados = px.bar(
        df_estados_sorted,
        x='localidade',
        y=selected_metric,
        title=f'{readable_metric_name} por Estado (Top {len(df_estados_sorted)})',
        labels={'localidade': 'Estado', selected_metric: readable_metric_name},
        template='plotly_dark', # Aplicar tema escuro ao gráfico
        color='regiao', # Colorir barras pela região (opcional, mas informativo)
        color_discrete_sequence=px.colors.qualitative.Pastel # Escolher uma paleta de cores
    )
    fig_estados.update_layout(xaxis_title=None, title_x=0.5) # Centralizar título
    # fig_estados.update_xaxes(tickangle=45) # Inclinar rótulos do eixo X se forem muitos

    # Formatação condicional do eixo Y para moeda
    if selected_metric == 'valor_total':
        fig_regioes.update_layout(yaxis_tickprefix="R$ ", yaxis_tickformat=",.2f")
        fig_estados.update_layout(yaxis_tickprefix="R$ ", yaxis_tickformat=",.2f")
    elif selected_metric == 'taxa_mortalidade':
         fig_regioes.update_layout(yaxis_ticksuffix=" %")
         fig_estados.update_layout(yaxis_ticksuffix=" %")
    else: # Formatação para números inteiros (internações, óbitos)
        fig_regioes.update_layout(yaxis_tickformat=",.0f")
        fig_estados.update_layout(yaxis_tickformat=",.0f")

    return fig_regioes, fig_estados

# --- 5. Execução do Servidor ---
if __name__ == '__main__':
    app.run(debug=True) # debug=True para desenvolvimento (recarrega automaticamente e mostra erros)
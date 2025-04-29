📊 Dashboard COVID-19 Brasil (2020–2025)
Este projeto é um Dashboard Interativo desenvolvido com Dash e Plotly, que apresenta dados agregados sobre internações, óbitos, taxa de mortalidade e custos estimados relacionados à COVID-19 no Brasil, abrangendo o período de fevereiro de 2020 até fevereiro de 2025.

🧾 Sobre os Dados
Os dados utilizados neste painel foram coletados de fontes oficiais do Governo Federal e consolidados em um arquivo CSV único. As informações estão agregadas por:

Região Geográfica

Unidade da Federação (Estado)

Totais Nacionais

📌 Nota: Os dados são totalizados por localidade para o período analisado. Não há série temporal mês a mês.

⚙️ Tecnologias Utilizadas
Python 3

Dash - Framework para criação de dashboards interativos.

Plotly Express - Geração de gráficos interativos.

Dash Bootstrap Components - Componentes de UI responsivos e estilizados.

Pandas - Manipulação de dados.

📁 Estrutura do Projeto
bash
Copiar
Editar
📦 covid_dashboard
├── app.py                 # Código principal do aplicativo
├── data.csv               # Arquivo de dados agregados (formato string lido com io.StringIO)
├── README.md              # Este arquivo
📌 Funcionalidades
🔢 Indicadores (KPIs)
Total de Internações

Total de Óbitos

Taxa de Mortalidade Média (%)

Custo Total Estimado (R$)

📈 Gráficos Interativos
Gráfico de Barras por Região

Gráfico de Barras por Estado, com coloração diferenciada por região

🎛️ Filtros
Dropdown para seleção da métrica de visualização

🧮 Processamento dos Dados
Os dados são lidos a partir de uma string CSV.

As colunas são padronizadas (nomes sem acentos ou espaços).

Estados são mapeados para suas respectivas regiões.

O dataset é separado em três grupos:

Regiões

Estados

Total Geral

💡 Como Executar Localmente
Pré-requisitos
Certifique-se de que o Python 3.7+ está instalado e instale os pacotes necessários com:
pip install dash dash-bootstrap-components pandas plotly
Rodando a Aplicação
python app.py
Acesse o painel em http://127.0.0.1:8050/ no navegador.

🌐 Visual do Dashboard
Estilização com tema escuro DARKLY do Bootstrap

Totalmente responsivo para diferentes tamanhos de tela

Títulos centralizados e legendas autoexplicativas

Formatação de valores no padrão brasileiro (ex: R$ 1.234.567,89)

📌 Observações
Os dados utilizados neste dashboard são fictícios ou simulados com base em fontes oficiais.

O painel não substitui relatórios epidemiológicos oficiais, mas serve como ferramenta visual analítica.

📄 Licença
Este projeto é livre para uso acadêmico e pessoal. Para usos comerciais, consulte a licença ou entre em contato com o autor.


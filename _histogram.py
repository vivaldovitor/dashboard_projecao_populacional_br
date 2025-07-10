from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import html


fig = go.Figure()
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0, 0, 0, 0)",
    bargap=0.2,
    xaxis_title="Idade",
    yaxis_title="População",
    font=dict(size=12)
)

hist = dbc.Row([
    dbc.Col(html.H4("Histograma Populacional por Idade"), width=12),
    dbc.Col([
        dcc.Graph(id="hist-graph", figure=fig),
        html.Div(id="total-pop", className="text-center text-muted my-2")
    ], width=12),
    dbc.Row([
        html.Footer([
        html.Span("Fonte: "),
        html.A("IBGE - Projeção da População 2025", href="https://www.ibge.gov.br/", target="_blank"),
        html.Br(),
        html.Span("Desenvolvido por Vivaldo Vítor"),
        html.Br(),
        html.A("GitHub", href="https://github.com/vivaldovitor", target="_blank"),
        html.Span(" • "),
        html.A("LinkedIn", href="https://www.linkedin.com/in/vivaldovitor", target="_blank"),
    ], className="credits")
    ])
])

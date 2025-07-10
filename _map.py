from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

fig = go.Figure()
fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0, 0, 0, 0)")

map = dbc.Card([
    dbc.CardHeader("Mapa Populacional por Região"),
    dbc.CardBody([
        dcc.Graph(
            id="map-graph",
            figure=fig,
            style={"height": "80vh", "width": "100%"}
        )
    ], style={"padding": "0"})
], className="shadow mb-4")


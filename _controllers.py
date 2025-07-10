from dash import dcc
import dash_bootstrap_components as dbc
from data_treatment import population_data, macro_regions

nomes_estados = population_data[
    ~population_data["LOCAL"].isin(["Centro-Oeste", "Norte", "Nordeste", "Sudeste", "Sul", "Brasil"])
]["LOCAL"].unique().tolist()
nomes_estados.sort()

controllers = dbc.Row([

    dbc.Col(dcc.Dropdown(
        id="macro-dropdown",
        options=[{"label": k, "value": k} for k in macro_regions],
        multi=True,
        placeholder="Selecione macro-região"
    ), width=2),

    dbc.Col(dcc.Dropdown(
        id="state-dropdown",
        options=[{"label": estado, "value": estado} for estado in nomes_estados],
        multi=True,
        placeholder="Selecione Estado"
    ), width=2),

    dbc.Col(dcc.Dropdown(
        id="year-dropdown",
        options=[{"label": y, "value": y} for y in range(2000, 2071)],
        multi=False,
        placeholder="Selecione ano"
    ), width=2),

    dbc.Col(dcc.Dropdown(
        id="age-min-dropdown",
        options=[{"label": str(i), "value": i} for i in range(0, 91)],
        value=0,
        clearable=False
    ), width=2),

    dbc.Col(dcc.Dropdown(
        id="age-max-dropdown",
        options=[{"label": str(i), "value": i} for i in range(0, 91)],
        value=90,
        clearable=False
    ), width=2),

    dbc.Col(dcc.Dropdown(
        id="sex-dropdown",
        options=[
            {"label": "Ambos", "value": "Ambos"},
            {"label": "Homens", "value": "Homens"},
            {"label": "Mulheres", "value": "Mulheres"}
        ],
        value="Ambos",
        clearable=False
    ), width=2)
])

from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

from app import app
from _map import map
from _histogram import hist
from _controllers import controllers
from data_treatment import population_data, macro_regions


# GeoJSON do Brasil
geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
brazil_geojson = requests.get(geojson_url).json()

app.layout = dbc.Container([
    html.H1("Projeções da População do Brasil e Unidades da Federação: 2000-2070",
            className="my-4 text-center"),

    dbc.Row([
        dbc.Col(controllers, width=12)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(map, width=12)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(hist, width=12)
    ]),
    

], fluid=True)



@app.callback(
    Output("map-graph", "figure"),
    Output("hist-graph", "figure"),
    Output("total-pop", "children"),
    Input("macro-dropdown", "value"),
    Input("state-dropdown", "value"),
    Input("year-dropdown", "value"),
    Input("age-min-dropdown", "value"),
    Input("age-max-dropdown", "value"),
    Input("sex-dropdown", "value"),
)
def update_figs(macros, states, year, age_min, age_max, sex):
    try:
        selected_macros = macros or []
        selected_states = states or population_data["LOCAL"].unique().tolist()
        selected_year = int(year) if year else 2025
        start_age = age_min or 0
        if age_min > age_max:
            age_min = 0
            age_max = 90
        if age_max == 0:
            end_age = age_max
        else:
            end_age = age_max or 90
            
        selected_sex = sex or "Ambos"

        if selected_macros:
            estados = [estado for m in selected_macros for estado in macro_regions.get(m, [])]
        elif selected_states:
            estados = selected_states
        else:
            estados = population_data["LOCAL"].unique().tolist()
            
        estados = population_data.loc[population_data["LOCAL"].isin(estados), "LOCAL"].unique().tolist()
        df = population_data[
            (population_data["LOCAL"].isin(estados)) &
            (population_data["SEXO"] == selected_sex) &
            (population_data["IDADE"] >= start_age) &
            (population_data["IDADE"] <= end_age)
        ]

        # MAPA
        map_df = df[["LOCAL", selected_year]].groupby("LOCAL").sum().reset_index()
        melted_map_df = map_df.melt(id_vars="LOCAL", var_name="Ano", value_name="População")

        max_population = melted_map_df[~melted_map_df["LOCAL"].isin(["Brasil", "Centro-Oeste", "Norte", "Nordeste", "Sudeste", "Sul"])]["População"].max()

        fig_map = px.choropleth(
            melted_map_df,
            geojson=brazil_geojson,
            featureidkey="properties.name",
            locations="LOCAL",
            color="População",
            color_continuous_scale="YlGnBu",
            range_color=(0, max_population),
            scope="south america"
        )
        fig_map.update_geos(fitbounds="locations", visible=False)
        fig_map.update_layout(template="plotly_dark", paper_bgcolor="rgba(0, 0, 0, 0)",
        coloraxis_colorbar=dict(title="População por UF"))

        # HISTOGRAMA
        df_hist = df.drop_duplicates(subset=["IDADE"])[["IDADE", selected_year]].groupby("IDADE", as_index=False).sum()
        total_pessoas = int(df_hist[selected_year].sum())
        total_text = f"Total de Pessoas no ano de {selected_year}: {total_pessoas:,}".replace(",", ".")

        # Define faixas etárias
        last_bin = ((end_age // 5) + 1) * 5
        bins = list(range(start_age, last_bin, 5))
        if bins[-1] < 91:
            bins.append(91)
        labels = [f"{i}-{i+4}" for i in bins[:-1]]
        if bins[-1] == 91:
            labels[-1] = f"{bins[-2]}+"
        df_hist["FaixaEtaria"] = pd.cut(
            df_hist["IDADE"],
            bins=bins,
            labels=labels,
            right=False
        )

        # Agrupa pela faixa etária
        grouped = df_hist.groupby("FaixaEtaria", observed=False)[selected_year].sum().reset_index()
        
        # Cria histograma
        if (end_age - start_age) <= 15:
            fig_hist = px.bar(
                df_hist,
                x="IDADE",
                y=selected_year,
                labels={"IDADE": "Idade", selected_year: "População"},
                color_discrete_sequence=px.colors.sequential.Plasma
            )
        else:
            fig_hist = px.bar(
            grouped,
            x="FaixaEtaria",
            y=selected_year,
            labels={"FaixaEtaria": "Idade", selected_year: "População"},
            color_discrete_sequence=px.colors.sequential.Plasma
            )

        fig_hist.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            bargap=0.2,
            xaxis_title="Idade",
            yaxis_title="População",
            font=dict(size=12),
            margin={"t": 30, "b": 40}
        )



        return fig_map, fig_hist, total_text

    except Exception as e:
        print("Erro no callback:", e)
        return go.Figure(), go.Figure(), ""


if __name__ == '__main__':
    app.run(debug=True)

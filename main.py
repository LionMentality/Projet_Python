from dash import Dash, html, dash_table, dcc, callback, Output, Input
from get_data import read
import requests
import plotly.express as px


data = read()
"""dataframe_map = data.groupby("code_departement")[["taux_de_logements_sociaux_en"]].sum().reset_index()
print(dataframe_map)
"""
app = Dash(__name__)
departement = requests.get(
    "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"
    ).json()

"""""     
graph = px.choropleth(
        data,
        geojson=departement,
        locations="code_departement",
        featureidkey="properties.code",
        color="taux_de_logements_sociaux_en",
        color_continuous_scale="Plasma",
        labels={"taux_de_logements_sociaux_en": "Taux de logements sociaux (en %)", "code_departement": "Département"},
        basemap_visible=False,
        locationmode="geojson-id",
        projection="mercator",
        )
graph.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
graph.update_geos(fitbounds="locations", visible=False)
"""

default_year = 2022
default_graph = px.choropleth(
    data[data['annee'] == default_year],
    geojson=departement,
    locations="code_departement",
    featureidkey="properties.code",
    color="taux_de_logements_sociaux_en",
    color_continuous_scale="Plasma",
    labels={"taux_de_logements_sociaux_en": f"Taux de logements sociaux (en %) - Année {default_year}", "code_departement": "Département"},
    basemap_visible=False,
    locationmode="geojson-id",
    projection="mercator",
)
default_graph.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
default_graph.update_geos(fitbounds="locations", visible=False)

# Définissez des styles CSS pour améliorer l'apparence de votre dashboard.
app.layout = html.Div([
        html.H1(children='Dashboard', style={'textAlign': 'center'}),
        
        # Ajoutez une carte géographique ici en utilisant dcc.Graph.

        dcc.Graph(
            id = "carte",
            figure = default_graph,
        )

        dcc.Dropdown(
            id='year-dropdown',
            options=[
                {'label': str(year), 'value': year} for year in data['annee'].unique()
            ],
            value=default_year,  # Année par défaut
            style={'width': '50%', 'margin': 'auto'}
        )
])


if __name__ == '__main__':
    app.run(debug=True)

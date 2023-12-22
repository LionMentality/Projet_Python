# Importation des bibliothèques nécessaires
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
from get_data import read  # Importation de la fonction read depuis get_data.py
import requests
import pandas as pd

# Lecture des données en utilisant la fonction read de get_data.py
data = read()

# Sélection des colonnes nécessaires pour la carte
columns_for_map = [
    'annee_publication',
    'code_departement',
    'taux_de_logements_sociaux_en',
    'taux_de_pauvrete_en',  # Ajouter d'autres colonnes si nécessaire
]

# Création d'un DataFrame spécifique aux colonnes de la carte
map_data = data[columns_for_map].copy()
map_data['annee_publication'] = map_data['annee_publication'].astype('Int64')
map_data = map_data.dropna(subset=['annee_publication'])

# Initialisation de l'application Dash
app = Dash(__name__)

# Chargement des données GeoJSON pour les départements français depuis un dépôt GitHub
departement = requests.get(
    "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"
).json()

# Utilisation de dcc.Store pour stocker les données
app.layout = html.Div([
    html.H1(children='Dashboard', style={'textAlign': 'center'}),

    # Stockage uniquement du DataFrame spécifique aux colonnes de la carte
    dcc.Store(id='data-store', data=map_data.to_dict('records')),

    # Utilisation de dcc.Loading pour afficher un spinner de chargement pendant la mise à jour du graphique
    dcc.Loading(
        id="loading",
        type="circle",  # Autres options : "default", "circle", "dot"
        children=[
            # Affichage de la carte choroplèthe
            dcc.Graph(
                id="carte",
                config={'scrollZoom': False, 'displayModeBar': False},
            )
        ]
    ),

    # Menu déroulant pour sélectionner l'année
    dcc.Dropdown(
        id='year-dropdown',
        options=[
            {'label': str(int(year)), 'value': int(year)} for year in map_data['annee_publication'].unique()
        ],
        value=map_data['annee_publication'].max(),  # Année par défaut
        style={'width': '50%', 'margin': 'auto'}
    ),

    # Menu déroulant pour sélectionner le filtre (Logements Sociaux ou Taux de Pauvreté)
    dcc.Dropdown(
        id='filter-dropdown',
        options=[
            {'label': 'Logements Sociaux', 'value': 'taux_de_logements_sociaux_en'},
            {'label': 'Taux de Pauvreté', 'value': 'taux_de_pauvrete_en'},
        ],
        value='taux_de_logements_sociaux_en',  # Filtre par défaut
        style={'width': '50%', 'margin': 'auto'}
    )
])

# Définition d'un rappel pour mettre à jour la carte et les données lorsque les valeurs des menus déroulants changent
@app.callback(
    [Output('carte', 'figure'),
     Output('data-store', 'data')],
    [Input('year-dropdown', 'value'),
     Input('filter-dropdown', 'value'),
     Input('data-store', 'data')]
)
def update_map(selected_year, selected_filter, stored_data):
    map_data = pd.DataFrame(stored_data)

    # Filtrer les données en fonction de l'année sélectionnée
    filtered_data = map_data[(map_data['annee_publication'] == selected_year)]

    # Mettre à jour la carte choroplèthe
    fig = px.choropleth(
        filtered_data,
        geojson=departement,
        locations="code_departement",
        featureidkey="properties.code",
        color=selected_filter,  # Utilisation du filtre sélectionné
        color_continuous_scale="Plasma_r",
        labels={selected_filter: f"{selected_filter} - Année {selected_year}", "code_departement": "Département"},
        basemap_visible=False,
        locationmode="geojson-id",
        projection="mercator",
    )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_geos(fitbounds="locations", visible=False)

    return fig, filtered_data.to_dict('records')

# Exécute l'application si le script est lancé
if __name__ == '__main__':
    app.run(debug=True)
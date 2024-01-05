# Import packages
from dash import Dash, html, dcc, dash_table, callback, Output, Input
import plotly.express as px
import requests
import pandas as pd
import urllib.request

# Incorporate data
df = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/bf82e99f-cb74-48e6-b49f-9a0da726d5dc', sep=';')

# Initialize the app
app = Dash(__name__)

# Sélection des colonnes nécessaires pour la carte
columns_for_map = [
    'annee_publication',
    'code_departement',
    'taux_de_logements_sociaux_en',
    'taux_de_pauvrete_en',  
    'nom_departement',
    'nombre_d_habitants',
    'nombre_de_logements',
]

# Création d'un DataFrame spécifique aux colonnes de la carte
map_data = df[columns_for_map].copy()
map_data['annee_publication'] = map_data['annee_publication'].astype('Int64')
map_data = map_data.dropna(subset=['annee_publication'])
map_data['nombre_d_habitants'] = map_data['nombre_d_habitants'].astype('Int64')
map_data['nombre_de_logements'] = map_data['nombre_de_logements'].astype('Int64')


# Chargement des données GeoJSON pour les départements français depuis un dépôt GitHub
departement = requests.get(
    "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"
).json()

# Utilisation d'une variable globale pour stocker les données
stored_data = map_data.to_dict('records')

# App layout
app.layout = html.Div([

    html.H1(children='Logements et logements sociaux', style={'textAlign': 'center'}),

    # dash_table.DataTable(data=df.to_dict('records'), page_size=15),

    dcc.Graph(figure=px.histogram(
        df,
        x='densite_de_population_au_km2',
        y='variation_de_la_population_sur_10_ans_en',
        histfunc='avg',
        labels={
            "densite_de_population_au_km2": "Densité de population au km² ",
            "variation_de_la_population_sur_10_ans_en": "Variation de la population sur 10 ans ",
        },
        color_discrete_sequence=['orange']
    ).update_layout(
        title='Histogramme de densité de population par variation sur 10 ans depuis 2018',
        xaxis_title='Densité de population au km²',
        yaxis_title='Variation de la population sur 10 ans (en %)'
    ).update_traces(marker=dict(line=dict(color='black', width=1)))),

    dcc.Graph(
        id='histogramme-individuels',
        figure=px.histogram(
            df,
            x='parc_social_taux_de_logements_individuels_en',
            y='parc_social_nombre_de_logements',
            histfunc='avg',
            labels={
                "parc_social_taux_de_logements_individuels_en": "Parc social : taux de logements individuels en % ",
                "parc_social_nombre_de_logements": "Parc social : nombre de logements ",
            },
            color_discrete_sequence=['violet']
        ).update_layout(
            title='Histogramme du taux de logements individuels par nombre de logements des parcs sociaux depuis 2018',
            xaxis_title='Parc social : taux de logements individuels (en %)',
            yaxis_title='Parc social : nombre de logements'
        ).update_traces(
            marker=dict(line=dict(color='black', width=1))
        ),
    ),

    html.Label('Filtre par taux de logements individuels :'),
    dcc.RangeSlider(
        id='filter-slider-individuels',
        min=df['parc_social_taux_de_logements_individuels_en'].min(),
        max=df['parc_social_taux_de_logements_individuels_en'].max(),
        value=[df['parc_social_taux_de_logements_individuels_en'].min(), df['parc_social_taux_de_logements_individuels_en'].max()],
        tooltip={'placement': 'bottom', 'always_visible': True},  # Afficher la valeur du slider
        pushable=1,  # Permettre de "pousser" l'autre poignée du slider
    ),

    dcc.Graph(
        id = "histogramme-vacants",
        figure=px.histogram(
            df,
            x='parc_social_taux_de_logements_vacants_en',
            y='parc_social_nombre_de_logements',
            histfunc='avg',
            labels={
                "taux_de_logements_sociaux_en": "Parc social : taux de logements vacants en % ",
                "parc_social_nombre_de_logements": "Parc social : nombre de logements ",
            },
            color_discrete_sequence=['skyblue']
            ).update_layout(
                title='Histogramme du taux de logements vacants par nombre de logements des parcs sociaux depuis 2018',
                xaxis_title='Parc social : taux de logements vacants (en %)',
                yaxis_title='Parc social : nombre de logements'
            ).update_traces(marker=dict(line=dict(color='black', width=1)))),

    html.Label('Filtre par taux de logements vacants :'),
    dcc.RangeSlider(
        id='filter-slider-vacants',
        min=df['parc_social_taux_de_logements_vacants_en'].min(),
        max=df['parc_social_taux_de_logements_vacants_en'].max(),
        value=[df['parc_social_taux_de_logements_vacants_en'].min(), df['parc_social_taux_de_logements_vacants_en'].max()],
        tooltip={'placement': 'bottom', 'always_visible': True},  # Afficher la valeur du slider
        pushable=1,  # Permettre de "pousser" l'autre poignée du slider
    ),

    html.H1(children='Dashboard', style={'textAlign': 'center'}),

html.Div([
        # Menu déroulant pour sélectionner l'année
        dcc.Dropdown(
            id='year-dropdown',
            options=[
                {'label': str(int(year)), 'value': int(year)} for year in map_data['annee_publication'].unique()
            ],
            value=map_data['annee_publication'].max(),  # Année par défaut
            style={'width': '45%', 'display': 'inline-block'}
        ),

        # Menu déroulant pour sélectionner le filtre (Logements Sociaux ou Taux de Pauvreté)
        dcc.Dropdown(
            id='filter-dropdown',
            options=[
                {'label': 'Logements Sociaux (%)', 'value': 'taux_de_logements_sociaux_en'},
                {'label': 'Taux de Pauvreté (%)', 'value': 'taux_de_pauvrete_en'},
                {'label': 'Nombre d\'Habitants', 'value': 'nombre_d_habitants'},
                {'label': 'Nombre de Logements', 'value': 'nombre_de_logements'},
            ],
            value='taux_de_logements_sociaux_en',  # Filtre par défaut
            style={'width': '45%', 'display': 'inline-block'}
        ),
    ], style={'textAlign': 'center', 'margin': 'auto', 'width': '90%'}),

    # Div englobante pour la carte
    html.Div([
        # Affichage de la carte choroplèthe
        dcc.Loading(
            id="loading",
            type="circle",
            children=[
                dcc.Graph(
                    id="carte",
                    config={'scrollZoom': False, 'displayModeBar': False},
                )
            ]
        )
    ], style={'width': '60%', 'margin': 'auto', 'border': '1px solid #ddd', 'padding': '10px', 'marginTop': '10px'}),

])

# Définition d'un rappel pour mettre à jour l'histogramme lorsque les valeurs du slider changent
@app.callback(
    Output('histogramme-vacants', 'figure'),
    [Input('filter-slider-vacants', 'value')],
)
def update_histogram(filter_slider_values):
    filtered_data = df[
        (df['parc_social_taux_de_logements_vacants_en'] >= filter_slider_values[0]) &
        (df['parc_social_taux_de_logements_vacants_en'] <= filter_slider_values[1])
    ]
    fig=px.histogram(
            df,
            x='parc_social_taux_de_logements_vacants_en',
            y='parc_social_nombre_de_logements',
            histfunc='avg',
            labels={
                "taux_de_logements_sociaux_en": "Parc social : taux de logements vacants en % ",
                "parc_social_nombre_de_logements": "Parc social : nombre de logements ",
            },
            color_discrete_sequence=['skyblue']
            ).update_layout(
                title='Histogramme du taux de logements vacants par nombre de logements des parcs sociaux depuis 2018',
                xaxis_title='Parc social : taux de logements vacants (en %)',
                yaxis_title='Parc social : nombre de logements'
            ).update_traces(marker=dict(line=dict(color='black', width=1))),

    return fig

# Définition d'un rappel pour mettre à jour l'histogramme lorsque les valeurs du slider changent
@app.callback(
    Output('histogramme-individuels', 'figure'),
    [Input('filter-slider-individuels', 'value')],
)
def update_histogram(filter_slider_values):
    filtered_data = df[
        (df['parc_social_taux_de_logements_individuels_en'] >= filter_slider_values[0]) &
        (df['parc_social_taux_de_logements_individuels_en'] <= filter_slider_values[1])
    ]
    fig = px.histogram(
            df,
            x='parc_social_taux_de_logements_individuels_en',
            y='parc_social_nombre_de_logements',
            histfunc='avg',
            labels={
                "parc_social_taux_de_logements_individuels_en": "Parc social : taux de logements individuels en % ",
                "parc_social_nombre_de_logements": "Parc social : nombre de logements ",
            },
            color_discrete_sequence=['violet']
            ).update_layout(
                title='Histogramme du taux de logements individuels par nombre de logements des parcs sociaux depuis 2018',
                xaxis_title='Parc social : taux de logements individuels (en %)',
                yaxis_title='Parc social : nombre de logements'
            ).update_traces(marker=dict(line=dict(color='black', width=1))),

    return fig

# Définition d'un rappel pour mettre à jour la carte et les données lorsque les valeurs des menus déroulants changent
@app.callback(
    Output('carte', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('filter-dropdown', 'value'),
    ],
)

def update_map(selected_year, selected_filter):
    global stored_data  # Utilisation de la variable globale

    map_data = pd.DataFrame(stored_data)

    # Filtrer les données en fonction de l'année sélectionnée
    filtered_data = map_data[(map_data['annee_publication'] == selected_year)]

    # Mettre à jour la carte choroplèthe
    fig = px.choropleth(
        filtered_data,
        geojson=departement,
        locations="code_departement",
        featureidkey="properties.code",
        color=selected_filter,  
        color_continuous_scale="Plasma_r",
        labels={
            selected_filter: f"{selected_filter} ",
            "code_departement": "Département ",
            #"nom_departement": "Département",  
            "nombre_d_habitants": "Nombre d'Habitants ",
            "nombre_de_logements": "Nombre de Logements ",
            "taux_de_logements_sociaux_en": "Taux de logements sociaux (%) ",
            "taux_de_pauvrete_en": "Taux de pauvrete (%) ",
        },
        basemap_visible=False,
        locationmode="geojson-id",
        projection="mercator",
    )

    # Personnaliser les étiquettes de l'échelle de couleur
    if selected_filter == 'nombre_de_logements':
        fig.update_coloraxes(colorbar_title=f"Nombre de Logements - Année {selected_year}")
    elif selected_filter == 'nombre_d_habitants':
        fig.update_coloraxes(colorbar_title=f"Nombre d'Habitants - Année {selected_year} ")
    elif selected_filter == 'taux_de_logements_sociaux_en':
        fig.update_coloraxes(colorbar_title=f"Taux de logements sociaux (%) - Année {selected_year} ")
    elif selected_filter == 'taux_de_pauvrete_en':
        fig.update_coloraxes(colorbar_title=f"Taux de pauvrete en (%) - Année {selected_year} ")

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_geos(fitbounds="locations", visible=False)


    return fig

# Exécute l'application si le script est lancé
if __name__ == '__main__':
    app.run(debug=True)
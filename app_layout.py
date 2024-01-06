# Importing necessary libraries 
from imports import *
from data import *

# Creating a Dash application instance
app = Dash(__name__)

# App layout
app.layout = html.Div(style={'backgroundColor': '#eefcff', 'textAlign' : 'center', 'margin-top': 0}, children=[

    # Header 1 for the main title
    html.H1(
        children='Logements et Indicateurs Socio-Économiques depuis 2018',
        style={'textAlign': 'center', 'fontFamily': 'Cooper Black', 'fontSize': 28}
    ),

    # Header 1 for the histogram title
    html.H1(
        children='Histogramme des parc sociaux : loyer moyen et logements mis en location par année',
        style={'textAlign': 'center', 'fontFamily': 'Cooper Black', 'fontSize': 20, 'margin-top': 50}
    ),

    # Dropdown for selecting the year in the histogram
    dcc.Dropdown(
        id='year-dropdown-histogramme',
        options=[
            {'label': str(int(year)), 'value': int(year)} for year in map_data['annee_publication'].unique()
        ],
        value=map_data['annee_publication'].max(),
        style={
            'width': '45%',
            'display': 'inline-block',
            'borderRadius': '10px',
            'boxShadow': '0px 0px 10px 0px rgba(0,0,0,0.1)',
            'margin': 'auto',
            'textAlign': 'center'
        }
    ),

    # Histogram graph
    dcc.Graph(
        id='histogramme',
        config={'scrollZoom': False, 'displayModeBar': False},
        figure=px.histogram(
            df,
            x='parc_social_loyer_moyen_en_eur_m2_mois',
            y='parc_social_logements_mis_en_location',
            color_discrete_sequence=['orange'],
            labels={
                'parc_social_loyer_moyen_en_eur_m2_mois': 'Parc social : loyer moyen ',
                'parc_social_logements_mis_en_location': 'Parc social : nombre de logements mis en location '
            }
        ).update_layout(
            xaxis_title='Parc social : loyer moyen (en euros / m² / mois)',
            yaxis_title='Parc social : nombre de logements mis en location'
        ).update_traces(marker=dict(line=dict(color='black', width=1))),

        style={'width': '80%', 'margin': 'auto', 'border': '1px solid #ddd', 'padding': '10px', 
              'marginTop': '10px', 'backgroundColor': '#fff', 'borderRadius': '10px', 
              'boxShadow': '0px 0px 10px 0px rgba(0,0,0,0.1)'}
    ),

    # Header 1 for the population graph title
    html.H1(
        children='Graphique de l\'évolution du nombre d\'habitants par région',
        style={'textAlign': 'center', 'fontFamily': 'Cooper Black', 'fontSize': 20, 'margin-top': 50}
    ),

    # Dropdown for selecting the region in the population graph
    dcc.Dropdown(
        id='filter-dropdown-graphique',
        options=[
            {'label': region, 'value': region} for region in df_filtered['nom_region'].unique()
        ],
        value=df_filtered['nom_region'].unique()[0],
        multi=False,
        style={
            'width': '45%',
            'display': 'inline-block',
            'borderRadius': '10px',
            'boxShadow': '0px 0px 10px 0px rgba(0,0,0,0.1)'
        }
    ),

    # Population graph
    dcc.Graph(
        id='graphique',
        config={'scrollZoom': False, 'displayModeBar': False},
        figure=px.line(
            df, 
            x='annee_publication', 
            y='nombre_d_habitants', 
        ),
        style={'width': '80%', 'margin': 'auto', 'border': '1px solid #ddd', 'padding': '10px', 
              'marginTop': '10px', 'backgroundColor': '#fff', 'borderRadius': '10px', 
              'boxShadow': '0px 0px 10px 0px rgba(0,0,0,0.1)'}
    ),

    # Header 1 for the geographic visualization title
    html.H1(
        children='Visualisation géographique : Logements sociaux et indicateurs socio-économiques',
        style={'textAlign': 'center', 'fontFamily': 'Cooper Black', 'fontSize': 20, 'margin-top': 50}
    ),

    # Dropdowns for selecting year and filter in the geographic visualization
    html.Div([
        dcc.Dropdown(
            id='year-dropdown',
            options=[
                {'label': str(int(year)), 'value': int(year)} for year in map_data['annee_publication'].unique()
            ],
            value=map_data['annee_publication'].max(),
            style={
                'width': '45%',
                'display': 'inline-block',
                'borderRadius': '10px',
                'boxShadow': '0px 0px 10px 0px rgba(0,0,0,0.1)'
            }
        ),

        dcc.Dropdown(
            id='filter-dropdown',
            options=[
                {'label': 'Logements Sociaux (%)', 'value': 'taux_de_logements_sociaux_en'},
                {'label': 'Taux de Pauvreté (%)', 'value': 'taux_de_pauvrete_en'},
                {'label': 'Nombre d\'Habitants', 'value': 'nombre_d_habitants'},
                {'label': 'Nombre de Logements', 'value': 'nombre_de_logements'},
            ],
            value='taux_de_logements_sociaux_en',
            style={
                'width': '45%',
                'display': 'inline-block',
                'borderRadius': '10px',
                'boxShadow': '0px 0px 10px 0px rgba(0,0,0,0.1)'
            }
        ),
    ], style={'textAlign': 'center', 'margin': 'auto', 'width': '90%', 'display': 'flex', 'justifyContent': 'space-between'}),

    # Loading and map visualization
    html.Div([
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
    ], style={'width': '60%', 'margin': 'auto', 'border': '1px solid #ddd', 'padding': '10px', 
              'marginTop': '10px', 'backgroundColor': '#fff', 'borderRadius': '10px', 
              'boxShadow': '0px 0px 10px 0px rgba(0,0,0,0.1)'}),
    ])
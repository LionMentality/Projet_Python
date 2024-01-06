from app_layout import *

@app.callback(
    Output('graphique', 'figure'),
    [Input('filter-dropdown-graphique', 'value')],
)
def update_graphique(selected_region):

    filtered_data = df[df['nom_region'] == selected_region]
    
    # Regrouper les données par année et calculer la somme des habitants pour chaque année
    grouped_data = filtered_data.groupby('annee_publication')['nombre_d_habitants'].sum().reset_index()

    figure = px.line(
        grouped_data, 
        x='annee_publication', 
        y='nombre_d_habitants', 
    ).update_layout(
        xaxis_title='Année',
        yaxis_title='Nombre d\'habitants'
    )
    
    return figure

@app.callback(
    Output('histogramme', 'figure'),
    [Input('year-dropdown-histogramme', 'value')],
)
def update_histogramme(selected_year):

    filtered_data = df[df['annee_publication'] == selected_year]
    
    figure=px.histogram(
            filtered_data,
            x='parc_social_nombre_de_logements',
            y='parc_social_logements_mis_en_location',
            color_discrete_sequence=['orange'],
            labels={
                'parc_social_nombre_de_logements': 'Parc social : nombre de logements ',
                'parc_social_logements_mis_en_location': 'Parc social : nombre de logements mis en location '
            }
        ).update_layout(
            xaxis_title='Parc social : nombre de logements',
            yaxis_title='Parc social : nombre de logements mis en location'
        ).update_traces(marker=dict(line=dict(color='black', width=1)))

    return figure

@app.callback(
    Output('carte', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('filter-dropdown', 'value')],
    [State('carte', 'figure')]
)
def update_map(selected_year, selected_filter, stored_map_figure):
    map_data_filtered = map_data[map_data['annee_publication'] == selected_year]

    figure = px.choropleth(
        map_data_filtered,
        geojson=departement,
        locations="code_departement",
        featureidkey="properties.code",
        color=selected_filter,
        color_continuous_scale="Plasma_r",
        labels={
            selected_filter: f"{selected_filter} ",
            "code_departement": "Département ",
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
        figure.update_coloraxes(colorbar_title=f"Nombre de Logements - Année {selected_year}")
    elif selected_filter == 'nombre_d_habitants':
        figure.update_coloraxes(colorbar_title=f"Nombre d'Habitants - Année {selected_year} ")
    elif selected_filter == 'taux_de_logements_sociaux_en':
        figure.update_coloraxes(colorbar_title=f"Taux de logements sociaux (%) - Année {selected_year} ")
    elif selected_filter == 'taux_de_pauvrete_en':
        figure.update_coloraxes(colorbar_title=f"Taux de pauvrete en (%) - Année {selected_year} ")

    figure.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    figure.update_geos(fitbounds="locations", visible=False)

    return figure
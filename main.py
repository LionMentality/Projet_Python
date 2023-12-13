from dash import Dash, html, dash_table, dcc, callback, Output, Input
from get_data import read

data = read()

app = Dash(__name__)

# Définissez des styles CSS pour améliorer l'apparence de votre dashboard.
app.layout = html.Div([
    html.H1(children='Dashboard', style={'textAlign': 'center'}),
    
    # Utilisez dash_table.DataTable pour afficher les données dans un tableau.
    dash_table.DataTable(
        id='table',
        columns=[{'name': col, 'id': col} for col in data.columns],
        data=data.to_dict('records'),
        style_table={'overflowX': 'auto'},  # Pour permettre le défilement horizontal.
    ),

    # Ajoutez une carte géographique ici en utilisant dcc.Graph.

])

if __name__ == '__main__':
    app.run(debug=True)

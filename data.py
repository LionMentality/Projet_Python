# Importing necessary libraries 
from imports import *

# Incorporate data
df = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/bf82e99f-cb74-48e6-b49f-9a0da726d5dc', sep=';')

# Selecting necessary columns for the map
columns_for_map = [
    'annee_publication',
    'code_departement',
    'taux_de_logements_sociaux_en',
    'taux_de_pauvrete_en',
    'nom_departement',
    'nombre_d_habitants',
    'nombre_de_logements',
]

# Creating a DataFrame specific to the map columns
map_data = df[columns_for_map].copy()
map_data['annee_publication'] = map_data['annee_publication'].astype('Int64')
map_data = map_data.dropna(subset=['annee_publication'])
map_data['nombre_d_habitants'] = map_data['nombre_d_habitants'].astype('Int64')
map_data['nombre_de_logements'] = map_data['nombre_de_logements'].astype('Int64')

# Filtering DataFrame for regions with non-null values
df_filtered = df.dropna(subset=['nom_region'])

# Loading GeoJSON data for French departments from a GitHub repository
departement = requests.get(
    "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"
).json()
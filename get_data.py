# Importation de la bibliothèque pandas
import pandas as pd

# Lire le fichier CSV dans un DataFrame
df = pd.read_csv('logements-et-logements-sociaux-dans-les-departements.csv', sep=';')
print(df)  # Afficher le DataFrame dans la console


"""""
def read ():
    df = pd.read_csv('logements-et-logements-sociaux-dans-les-departements.csv', sep = ';')
    return df
"""""

# Fonction pour lire les données à partir d'un fichier CSV ou d'une URL
def read():
    # URL du fichier CSV contenant les données
    url = "https://www.data.gouv.fr/fr/datasets/r/bf82e99f-cb74-48e6-b49f-9a0da726d5dc"
    # Lire les données du fichier CSV dans un DataFrame
    df = pd.read_csv(url, sep=';')
    return df
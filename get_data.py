import pandas as pd

df = pd.read_csv('logements-et-logements-sociaux-dans-les-departements.csv', sep = ';')
print (df)

"""""
def read ():
    df = pd.read_csv('logements-et-logements-sociaux-dans-les-departements.csv', sep = ';')
    return df
"""""

def read():
    url = "https://www.data.gouv.fr/fr/datasets/r/bf82e99f-cb74-48e6-b49f-9a0da726d5dc"
    df = pd.read_csv(url, sep=';')
    return df
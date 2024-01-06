# Importing necessary libraries 
import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('logements-et-logements-sociaux-dans-les-departements.csv', sep=';')
print(df)  # Display the DataFrame in the console



# Function to read data from a CSV file or URL
def read():
    # URL of the CSV file containing the data
    url = "https://www.data.gouv.fr/fr/datasets/r/bf82e99f-cb74-48e6-b49f-9a0da726d5dc"
    
    # Read data from the CSV file into a DataFrame
    df = pd.read_csv(url, sep=';')
    dftest = df[['annee_publication','code_departement']]
    return dftest
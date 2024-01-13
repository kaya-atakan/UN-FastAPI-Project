from fastapi import FastAPI
import requests
import pandas as pd
from io import StringIO
import numpy as np

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/un_data")
async def get_un_data():
    # Fetch the CSV data from the API
    response = requests.get("https://data.un.org/_Docs/SYB/CSV/SYB66_327_202310_International%20Migrants%20and%20Refugees.csv")

    # Check if the request was successful
    if response.status_code != 200:
        return {"error": "Failed to fetch data"}

    # Convert CSV data to a Pandas DataFrame
    df = pd.read_csv(StringIO(response.text))

    # Replace NaN, Inf, -Inf with "N/A"
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.fillna("N/A", inplace=True)

    # List of EU countries
    eu_countries = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 
                    'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland', 
                    'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 
                    'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden']

    # Filter the DataFrame for only EU countries
    # Replace 'Country' with the actual column name for countries in your dataset
    df = df[df['International migrants and refugees'].isin(eu_countries)]

    # Drop unwanted columns
    df = df.drop(columns=["T04","Unnamed: 5", "Unnamed: 6"])

    # Generate a unique list of countries and create a mapping to new IDs
    unique_countries = df['International migrants and refugees'].unique()
    country_id_map = {country: idx + 1 for idx, country in enumerate(unique_countries)}

    # Map the countries in the DataFrame to their new IDs
    df['country_id'] = df['International migrants and refugees'].map(country_id_map)

    # Rename columns
    df = df.rename(columns={"Unnamed: 2": "year", "Unnamed: 3": "statistic_type", "Unnamed: 4": "value"})

    # Reorder columns
    df = df[['country_id', 'year', 'statistic_type', 'value']]

    # Convert the filtered DataFrame to a list of dictionaries
    data = df.to_dict(orient='records')
    return data

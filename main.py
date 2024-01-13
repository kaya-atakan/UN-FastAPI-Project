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

    # Convert the filtered DataFrame to a list of dictionaries
    data = df.to_dict(orient='records')
    return data

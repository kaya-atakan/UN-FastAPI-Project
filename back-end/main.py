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
    df = df.drop(columns=["Unnamed: 5", "Unnamed: 6"])

    # Generate a unique list of countries and create a mapping to new IDs
    unique_countries = df['International migrants and refugees'].unique()
    country_id_map = {country: idx + 1 for idx, country in enumerate(unique_countries)}

    # Map the countries in the DataFrame to their new IDs
    df['country_id'] = df['International migrants and refugees'].map(country_id_map)

    # Rename columns
    df = df.rename(columns={"International migrants and refugees": "country_name", "Unnamed: 2": "year", "Unnamed: 3": "statistic_type", "Unnamed: 4": "value"})

    # Reorder columns
    df = df[['country_name','country_id', 'year', 'statistic_type', 'value']]

    df = df.query("statistic_type == 'International migrant stock: Both sexes (% total population)'")

    # Check if each country has data for all four years
    # years_required = {2005, 2010, 2015, 2020}
    # check_years = df.groupby(['country_id', 'country_name'])['year'].apply(lambda x: set(x.astype(int)) == years_required)

    # Convert the check result to a dictionary and return it
    # check_years_dict = check_years.reset_index().rename(columns={'year': 'has_all_years'}).to_dict(orient='records')
    # return check_years_dict

    # Convert the filtered DataFrame to a list of dictionaries
    data = df.to_dict(orient='records')
    return data

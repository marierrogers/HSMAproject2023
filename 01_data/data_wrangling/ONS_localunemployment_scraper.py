# Script to scrape local unemployment data by Region from ONS website
# 
# Outputs CSV file with unemployment by month and region in thousands and %
# test
# Import libraries
import requests
import pandas as pd
import urllib.parse
import io

# Function to download data from urls
def download_data(url):
    decoded_url = urllib.parse.unquote(url)
    response = requests.get(decoded_url)
    response.raise_for_status()  # Check if the request was successful

    data = response.content.decode('utf-8')
    df = pd.read_csv(io.StringIO(data))

    return df

# Get info from ref table to decode URLs - ensure saved in working folder
url_codes = pd.read_csv('REF_localunemployment_codes.csv')

suffixes = url_codes['Suffix']

base_url = "https://www.ons.gov.uk/generator?format=csv&uri=/employmentandlabourmarket/peoplenotinwork/unemployment/timeseries/"

combined_df = pd.DataFrame()

# Run loop extracting csv data from each URL using base + suffix list

for suffix in suffixes:
    url = f"{base_url}{suffix}"
    df = download_data(url)
    # Exclude first 8 rows - contains metadata
    df = df.iloc[8:, :]
    current_columns = df.columns
    # Rename columns to allow concat
    new_columns = {current_columns[0]: 'Date',current_columns[1]:"Value"}
    df = df.rename(columns=new_columns)
    # Add DataFrame source column
    df['Source'] = suffix
    combined_df = pd.concat([combined_df, df], ignore_index=True)

# Make ref table merge column name match df
url_codes = url_codes.rename(columns={'Suffix': 'Source'})

merged_df = combined_df.merge(url_codes, on='Source')

# Dataframe now contains data in format monthly, yearly and quarterly
# Use regex to identify monthly date format and only keep this data

# Define the regex pattern to extract the monthly values
pattern = r'(\d{4} [A-Z]{3})'  # Matches YYYY MMM format

# Extract the monthly values using regex
merged_df['Date'] = merged_df['Date'].str.extract(pattern)

# Drop rows with missing values (non-monthly values)
merged_df.dropna(subset=['Date'], inplace=True)

merged_df['Date'] = pd.to_datetime(merged_df['Date'], format='%Y %b')

merged_df.to_csv('ONS_localunemployment_monthly.csv', index=False)






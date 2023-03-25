import psycopg2
import requests
import os
from datetime import datetime

# Read HS codes from the text file
hs_codes_file = "hs_codes.txt"
with open(hs_codes_file, "r") as f:
    hs_codes = [line.strip() for line in f.readlines()]

# Connect to the PostgreSQL database
conn = psycopg2.connect(database='your_database_name', user='postgres', password='your_password', host='localhost', port='5432')
cur = conn.cursor()

# Define helper functions to fetch data from different APIs
def fetch_itc_data(hs_code, year):
    # Fetch data from the ITC Trade Map API
    api_key = 'YOUR_ITC_TRADEMAP_API_KEY'
    url = f'https://api.trademap.org/data?hs_code={hs_code}&year={year}&api_key={api_key}'
    response = requests.get(url)
    return response.json()

def fetch_un_comtrade_data(hs_code, year):
    # Fetch data from the UN Comtrade Database API
    url = f'https://comtrade.un.org/api/get?max=500&type=C&freq=A&px=HS&ps={year}&r=world&p=0&rg=2&cc={hs_code}&fmt=json'
    response = requests.get(url)
    return response.json()

# Function to insert data into the metal_data table
def insert_data(hs_code, source, year, value):
    cur.execute("INSERT INTO metal_data (hs_code, source, year, value) VALUES (%s, %s, %s, %s);", (hs_code, source, year, value))

# Fetch data for the last ten years
current_year = datetime.now().year
start_year = current_year - 10

# Iterate over the HS codes and years, fetch data, and insert it into the database
for hs_code in hs_codes:
    for year in range(start_year, current_year + 1):
        # Fetch data from the ITC Trade Map API
        itc_data = fetch_itc_data(hs_code, year)
        if itc_data:
            insert_data(hs_code, 'ITC', year, itc_data)

        # Fetch data from the UN Comtrade Database API
        un_comtrade_data = fetch_un_comtrade_data(hs_code, year)
        if un_comtrade_data and un_comtrade_data['validation']['status'] == 'success':
            trade_value = un_comtrade_data['dataset'][0]['TradeValue'] if un_comtrade_data['dataset'] else 0
            insert_data(hs_code, 'UN Comtrade', year, trade_value)

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()
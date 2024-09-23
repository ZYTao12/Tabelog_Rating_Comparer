import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import pandas as pd

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv('PLACES_API_KEY')

# Scraping tabelog.com
restaurants = []
location = input("Enter the location (city or prefecture, e.g., tokyo, aomori, etc.):")
print("If the location is not found, the data will be based on all restaurants in Japan.")
print("Please wait for a moment... Scraping data from tabelog.com and Google Places API...")
for page in range(1,4):
    url = "https://tabelog.com/" + location + "/rstLst/" + str(page)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for restaurant in soup.find_all('div', class_='list-rst'):
            name_tag = restaurant.find('a', class_='list-rst__rst-name-target')
            rating_tag = restaurant.find('span', class_='c-rating__val')
            
            if name_tag and rating_tag:
                name = name_tag.text.strip()
                tabelog_rating = rating_tag.text.strip()
                restaurants.append({'name': name, 'tabelog_rating': tabelog_rating})
    else:
        response.raise_for_status()

# Fetch Places API data
places_api_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
for restaurant in restaurants:
    params = {
        'input': restaurant['name'],
        'inputtype': 'textquery',
        'fields': 'formatted_address,rating',
        'key': API_KEY
    }
    places_response = requests.get(places_api_url, params=params)
    if places_response.status_code == 200:
        places_data = places_response.json()
        if places_data['candidates']:
            candidate = places_data['candidates'][0]
            restaurant['google_rating'] = candidate.get('rating', 'No rating found')
            restaurant['address'] = candidate.get('formatted_address', 'No address found')
        else:
            restaurant['places_data'] = 'No data found'
    else:
        restaurant['places_data'] = 'Error fetching data'

# Convert to DataFrame
df = pd.DataFrame(restaurants)
print("Preview:")
print(df[1:10])
print("... The rest of the data is saved in 'combined_ratings.csv'.")
# Save to CSV
df.to_csv('combined_ratings.csv', index=False)

def analyze_rating_difference(df):
    # Convert ratings to numeric values
    df['tabelog_rating'] = pd.to_numeric(df['tabelog_rating'], errors='coerce')
    df['google_rating'] = pd.to_numeric(df['google_rating'], errors='coerce')

    # Drop rows with NaN values in either rating column
    df = df.dropna(subset=['tabelog_rating', 'google_rating'])

    # Calculate the difference between Tabelog and Google ratings
    df.loc[:, 'rating_difference'] = df['tabelog_rating'] - df['google_rating']

    # Calculate statistical measures
    mean_diff = df['rating_difference'].mean()
    median_diff = df['rating_difference'].median()
    std_diff = df['rating_difference'].std()

    return {
        'mean_difference': mean_diff,
        'median_difference': median_diff,
        'std_difference': std_diff
    }
pd.options.mode.chained_assignment = None   # Disable SettingWithCopyWarning (does not affect my case)
stats = analyze_rating_difference(df)
print("The mean difference between Tabelog and Google ratings is:", stats['mean_difference'])
print("The standard deviation of the difference between Tabelog and Google ratings is:", stats['std_difference'])

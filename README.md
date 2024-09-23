# Tabelog_Rating_Comparer
A Python tool that compares ratings from Tabelog and Google Maps reviews, and more.

## Overview

Finding the Google-rated restaurants that locals frequent in Japan has been notoriously challenging. Instead of relying on the globally used Google Maps, many Japanese food enthusiasts prefer to share their experiences on Tabelog, a local restaurant review platform. However, Tabelog is primarily available in Japanese, making it difficult for foreign visitors to access. This program creates a convenient tool that generates a dataset of reviews from both platforms. By the end of the program execution, you'll see just how different the ratings on these two platforms can be!

## Features

- Scrapes restaurant data from Tabelog.com
- Retrieves corresponding restaurant data from Google Places API
- Generates a CSV file with combined data
- Performs statistical analysis on rating differences

## Data Pipeline

- Web Scraping: Tabelog.com（食べログ）
- API: Google Places API

## Requirements

- Python 3.7+
- Libraries: requests, python-dotenv, beautifulsoup4, pandas

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/Tabelog_Rating_Comparer.git
   cd Tabelog_Rating_Comparer
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Google Places API key:
   - Create a `.env` file in the project root
   - Add your API key: `PLACES_API_KEY=your_api_key_here`
   - How to get your Google API key: https://developers.google.com/maps/documentation/places/web-service/get-api-key

## Usage

Run the main script:
```
python main.py
```

## Data Analysis

The program generates a CSV file with the following columns:
- `name`: The name of the restaurant on Tabelog
- `tabelog_rating`: The rating of the restaurant on Tabelog
- `google_rating`: The rating of the restaurant on Google Maps
- `address`: Formatted address of the restaurant from Google Maps

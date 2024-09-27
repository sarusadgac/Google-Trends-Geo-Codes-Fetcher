import requests
import re
import pycountry
import os
from datetime import datetime

# Function to get geo location from the atom feed link
def get_geo_from_pn(pn):
    url = f'https://trends.google.com/trends/hottrends/atom/feed?pn={pn}'
    response = requests.get(url)
    if response.status_code == 200:
        # Extract geo information from the atom feed
        match = re.search(r'geo=([A-Z]{2})', response.text)
        if match:
            return pn, match.group(1)  # Returns geo codes like US, IN
        else:
            return pn, ''  # Leave empty if no geo info
    else:
        return pn, 'Error'  # Mark as 'Error' if no trend data

# Function to get country name from ISO country code
def get_country_name(geo):
    try:
        country = pycountry.countries.get(alpha_2=geo)
        if country:
            return country.name
    except KeyError:
        return 'Unknown Country'
    return 'Unknown Country'

# Get current time for the last update timestamp
current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

# Starting content for the README file
readme_content = f"""
## Google Trends Geo Code Fetcher

Using Google Trends data, this tool automatically collects and updates the pn codes and their respective country names.

**Last Update:** {current_time}

| pn code | Country |
|---------|---------|
"""

# Write results to a file and append to README.md
with open('found_geo_codes.txt', 'w') as f, open('README.md', 'w') as readme:
    # Initialize README content
    readme.write(readme_content)
    
    for i in range(101):  # Iterate through first 101 entries
        pn = f'p{i}'
        pn, geo = get_geo_from_pn(pn)
        if geo != '' and geo != 'Error':
            # Get country name using pycountry
            country_name = get_country_name(geo)
            
            # Write to found_geo_codes.txt
            f.write(f'{pn} belongs to: {country_name} ({geo})\n')
            
            # Write to README.md in table format
            readme.write(f'| {pn} | {country_name} |\n')

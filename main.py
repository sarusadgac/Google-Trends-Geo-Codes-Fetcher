import requests 
import re

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

# Write results to a file
with open('found_geo_codes.txt', 'w') as f:
    for i in range(1001):
        pn = f'p{i}'
        pn, geo = get_geo_from_pn(pn)
        if geo != '' and geo != 'Error':
            f.write(f'{pn} belongs to: {geo}\n')

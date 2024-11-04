import requests
import json
import time
import logging

# Set up logging
logging.basicConfig(filename='api_data_collection.log', level=logging.INFO)

# Function to fetch data from the API
def fetch_data(page_num):
    headers = {
        'Authorization': f'Bearer {api_auth}',
        'Content-Type': 'application/json'
    }
    params = {
        'page': page_num,
        'limit': 50
    }
    
    try:
        response = requests.get(api_uri, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f'Error fetching data from API: {e}')
        return None

# Function to save data to a file
def save_data(data, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info(f'Data saved to {filename}')
    except Exception as e:
        logging.error(f'Error saving data to file: {e}')

# Main data collection loop
page = 1
total_pages = float('inf')
all_data = []
api_uri = 'https://www.instagram.com/8324travelblog/'
api_auth = {
    'api_key': 'your_api_key_here',
    'api_id': 'your_api_id_here',
    'api_secret':  'your_api_secret_here'
}
while page <= total_pages:
    data = fetch_data(page)
    if data:
        all_data.extend(data['results'])
        total_pages = data['total_pages']
        logging.info(f'Fetched data from page {page}/{total_pages}')
        page += 1
        time.sleep(1)  # Add a delay to avoid overwhelming the API
    else:
        break

# Save the collected data to a file
save_data(all_data, 'api_data.json')

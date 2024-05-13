import sys
import requests
from dotenv import load_dotenv
import os

def get_geolocation(ip):
    api_key = os.getenv('IPGEO_API_KEY')
    url = f'https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip}&fields=all'
    response = requests.get(url)
    data = response.json()
    return data

def main():
    load_dotenv()
    for line in sys.stdin:
        ip = line.strip()
        try:
            geolocation_data = get_geolocation(ip)
            print(geolocation_data)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()


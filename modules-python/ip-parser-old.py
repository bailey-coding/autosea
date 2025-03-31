import requests
import json


def update_cloudflare_ip_list():
    cloudflare_api_url = "https://api.cloudflare.com/client/v4/ips"
    cloudflare_ip_list_path = "./data/cloudflare-ip-ranges.json"

    # Download Cloudflare IP ranges
    try:
        response = requests.get(cloudflare_api_url)
        response.raise_for_status()  # Raises an HTTPError if the response was an error

        # Write to file
        with open(cloudflare_ip_list_path, "w") as outfile:
            json.dump(response.json(), outfile)
    except requests.exceptions.RequestException as e:
        print("Error: Failed to download Cloudflare IP ranges.", e)
        exit(1)


# Example usage (commented out to prevent automatic execution):
# update_aws_ip_list()
# update_cloudflare_ip_list()

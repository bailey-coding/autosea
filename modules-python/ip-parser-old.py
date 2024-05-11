import requests
import json
import os

def update_aws_ip_list():
    aws_ip_list_url = "https://project-fabulizer.s3.amazonaws.com/ip-ranges.json"
    aws_ip_list_temp_path = "./data/aws-ip-ranges-temp.json"
    aws_ip_list_path = "./data/aws-ip-ranges.json"
    
    # Attempt to download the AWS IP list
    try:
        response = requests.get(aws_ip_list_url)
        response.raise_for_status()  # Raises an HTTPError if the response was an error
        
        # Write temporary file
        with open(aws_ip_list_temp_path, 'w') as temp_file:
            json.dump(response.json(), temp_file)
        
        # Replace the old IP list with the new one
        os.replace(aws_ip_list_temp_path, aws_ip_list_path)
    except requests.exceptions.RequestException as e:
        print("Error: Failed to download AWS IP ranges. Are you on the VPN?", e)
        exit(1)

def update_cloudflare_ip_list():
    cloudflare_api_url = "https://api.cloudflare.com/client/v4/ips"
    cloudflare_ip_list_path = "./data/cloudflare-ip-ranges.json"
    
    # Download Cloudflare IP ranges
    try:
        response = requests.get(cloudflare_api_url)
        response.raise_for_status()  # Raises an HTTPError if the response was an error
        
        # Write to file
        with open(cloudflare_ip_list_path, 'w') as outfile:
            json.dump(response.json(), outfile)
    except requests.exceptions.RequestException as e:
        print("Error: Failed to download Cloudflare IP ranges.", e)
        exit(1)

# Example usage (commented out to prevent automatic execution):
# update_aws_ip_list()
# update_cloudflare_ip_list()

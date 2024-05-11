import requests
import json
import os
import ipaddress
import sys

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


# Function to check if a given IP is in the provided CIDR ranges in the JSON file
def check_if_cloudflare_ip(ip, file_path):
    try:
        # Open and load the JSON file
        with open(file_path, 'r') as file:
            data_dict = json.load(file)
        
        # Extract both IPv4 and IPv6 CIDR ranges
        ipv4_cidrs = data_dict['result']['ipv4_cidrs']
        ipv6_cidrs = data_dict['result']['ipv6_cidrs']

        # Convert the given IP address into an ipaddress object
        ip_obj = ipaddress.ip_address(ip)

        # Check against IPv4 CIDRs
        for cidr in ipv4_cidrs:
            if ip_obj in ipaddress.ip_network(cidr, strict=False):
                return True

        # Check against IPv6 CIDRs
        for cidr in ipv6_cidrs:
            if ip_obj in ipaddress.ip_network(cidr, strict=False):
                return True

        # If IP is not in any range
        return False
    except ValueError as e:
        # In case of any errors (e.g., invalid IP address format)
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # Check if an IP address is provided via stdin
    if not sys.stdin.isatty():
        ip_address = sys.stdin.read().strip()
        file_path = './data/cloudflare-ip-ranges.json'
        
        # Check if the IP is in the ranges
        is_in_ranges = check_if_cloudflare_ip(ip_address, file_path)
        
        # Adjusted print statement to reflect TRUE/FALSE output
        print("TRUE" if is_in_ranges else "FALSE")
    else:
        print("Please provide an IP address.")
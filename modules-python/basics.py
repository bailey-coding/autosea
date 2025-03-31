import sys
import re
import requests
import subprocess
from dotenv import dotenv_values
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ENV_PATH = SCRIPT_DIR.parent / "data" / ".env"
env_vars = dotenv_values(ENV_PATH)

DEFAULT_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0"
USER_AGENT = env_vars.get("CUSTOM_USER_AGENT", DEFAULT_USER_AGENT)


def url_formatter(url):
    # Validate URL format
    pattern = r"^(http|https)://[a-zA-Z0-9.-]+[a-zA-Z0-9]\.[a-zA-Z]{2,}.*$"
    if re.match(pattern, url):
        # url_base64 = base64.b64encode(url.encode()).decode().rstrip("=")
        # url_sha256 = hashlib.sha256(url.encode()).hexdigest()
        # Debug statements for VT API.
        # print(f"Base64: {url_base64}")
        # print(f"SHA256: {url_sha256}")
        ...
    else:
        print("Please ensure you've inputted a valid URL including http(s)://")
        print("Example: https://example.com/")
        sys.exit(2)


def curl_headers(url):
    try:
        response = requests.get(
            url, headers={"User-Agent": USER_AGENT}, allow_redirects=True
        )

        if response.history:
            print("Redirect path:")
            for redirect in response.history:
                location = redirect.headers.get("Location", "Unknown")
                print(f"  Redirected from: {redirect.url} to {location}")
            print(f"  Final URL: {response.url}")

        print("response:")
        print(f"  status code: {response.status_code}")
        for header in ["Date", "Content-Type", "Server", "Location", "Via"]:
            if header in response.headers:
                print(f"  {header.lower()}: {response.headers[header]}")

    except requests.RequestException as e:
        error_message = str(e)
        # Match SSL Certificate Verification Errors
        ssl_cert_error = re.search(r"SSLCertVerificationError\((.*)\)", error_message)
        # Match Hostname Mismatch Errors
        hostname_mismatch_error = re.search(
            r"hostname '.*' doesn't match either of (.*)", error_message
        )

        if ssl_cert_error:
            error_summary = (
                f"SSL Certificate Verification Failed: {ssl_cert_error.group(1)}"
            )
        elif hostname_mismatch_error:
            error_summary = f"Hostname Mismatch: {hostname_mismatch_error.group(1)}"
        else:
            # Simplify the general connection error message
            simple_error_message = re.search(
                r"Failed to establish a new connection: \[(.*)\]", error_message
            )
            if simple_error_message:
                error_summary = simple_error_message.group(1)
            else:
                error_summary = "Failed to make a request due to a network error."

        print(f"curl failed: {error_summary}")
        sys.exit(1)


def host_lookup(url):
    domain_regex = r"^(?:http[s]?://)?(?:[a-zA-Z0-9-]+\.)+([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(?:[/?].*)?$"
    match = re.match(domain_regex, url)
    if match:
        domain = match.group(1)
        print("host:")
        print(f"  domain: {domain}")
        print("  output:")
        try:
            result = subprocess.check_output(["host", domain], universal_newlines=True)
            for line in result.splitlines():
                print(f"    - {line}")
        except subprocess.CalledProcessError:
            # Catch the exception and instead of printing the error, we exit with a custom message
            print("Host lookup failed: no DNS records found.")
            sys.exit(
                1
            )  # Using exit code 1 to indicate an error, see readme for all exit codes in use.
    else:
        print("Invalid domain format.")


def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py [function] [URL]")
        sys.exit(1)

    function = sys.argv[1]
    url = sys.argv[2]

    if function == "url_formatter":
        url_formatter(url)
    elif function == "curl_headers":
        curl_headers(url)
    elif function == "host_lookup":
        host_lookup(url)
    else:
        print("Invalid function specified.")
        sys.exit(2)


if __name__ == "__main__":
    main()

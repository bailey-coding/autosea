#!/usr/bin/env bash

# URL Formatter for Debug tools and ensuring URL is parsed correctly. 
__UrlFormatter__ () {
    local URL=$1
    # Check for a valid URL using regex
    if [[ $URL =~ ^(http|https)://[a-zA-Z0-9.-]+[a-zA-Z0-9]\.[a-zA-Z]{2,}.*$ ]]; then
        local URLBase64=$(echo -n "$URL" | base64 | cut -d '=' -f 1)
        local URLSha256=$(echo -n "$URL" | sha256sum | cut -d ' ' -f 1)
        declare -g InputURLBase64=$URLBase64
        declare -g InputURLSha256=$URLSha256
    else
        echo "Please ensure you've inputted a valid URL including http(s)://"
        echo "Example: https://example.com/"
        echo "example.com will not parse."
        exit 2
    fi
}

# user agent creator

__SetUserAgent__


# required software parser, ensuring reqs are all present on the system.
__CheckInstalledSoftware__() {
    local yaml_file="$1"
    requirements=()

    while IFS=": " read -r key value; do
        case "$key" in
            -)
                # Check if the line is a requirement
                if [ -n "$value" ]; then
                    requirements+=("$value")
                fi
                ;;
        esac
    done < <(sed -n '/^requirements:/,/^$/p' "$yaml_file" | grep -v '^requirements:$')

    # Trim leading and trailing spaces from requirements
    requirements=("${requirements[@]// /}")

}


# Curl given URL, and respond with response and relevant things such as server, content type, time, redirect location if given.
#    TODO:  Parse for other relevant data in the returned header. 
__CurlHeaders__ () {
    local URL=$1
    echo "curl ${URL}"
    local CURL_OUTPUT=$(curl -sI -A 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0' "${URL}" 2>&1)
    local HTTP_STATUS=$(echo "${CURL_OUTPUT}" | grep -Ei "^HTTP")
    if [ -n "${HTTP_STATUS}" ]; then
        echo "${CURL_OUTPUT}" | awk -v url="${URL}" '
            BEGIN {
              print "response:"
            }
            /^HTTP/ {
              print "  status code:", $1, $2
            }
            /^(date|Date):/ {
              print "  time:", $2, $3, $4, $5, $6, $7
            }
            /^(content-type|Content-Type):/ {
              print "  content_type:", $2
            }
            /^(server|Server):/ {
              print "  server:", $2
            }
            /^(location|Location):/ {
              print "  redirect-location:", $2
            }
            /^(via|Via):/ {
              print "  via:", $3, $4
            }
          ' | sed 's/,$//' | sed 's/^/  /'
    else
      echo "error: ${CURL_OUTPUT}"
    fi
    echo ""
}


# HOST against given domain, stripping the rest of the URL, HTTP(S), anything more than a domain name. 
__HostLookup__ () {
    local URL=$1
    local HostParsedURL=$(echo "${URL}" | sed -E 's/.*\/\/([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,}).*/\1.\2/')
    echo "host:"
    echo "  domain: ${HostParsedURL}"
    echo "  output:"
    # Run the host command and format output into YAML
    while read -r line; do
        echo "    - $line"
    done < <(host "${HostParsedURL}")
    echo ""
}


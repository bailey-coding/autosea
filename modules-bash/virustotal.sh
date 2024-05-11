#!/usr/bin/env bash
__VirusTotalCheck__ () {
    # Constant variables
    local URL=$1

    # Make the request to VirusTotal API
    local VT_ANALYSE=$(curl -s -X POST --url "https://www.virustotal.com/api/v3/urls" --form "url=${URL}"   --header "x-apikey: ${VTAPI_KEY}")
    
    # Extract the scan_id from the response
    local VT_SCAN_ID=$(echo "${VT_ANALYSE}" | jq -r '.data.id')

    # Retrieve the scan report and build a count.
    local VTREPORT=$(curl -s -X GET --url "https://www.virustotal.com/api/v3/analyses/${VT_SCAN_ID}" --header "x-apikey: ${VTAPI_KEY}")
    
    # Generate a web browser URL for the scan
    local VT_URL=$(echo "${VT_SCAN_ID}" | sed 's/^u-\(.*\)-[0-9]*$/\1/') 

    # Extract relevant information from the report
    local VT_HARMLESS_COUNT=$(echo "${VTREPORT}" | jq -r '.data.attributes.stats.harmless')
    local VT_UNDETECTED_COUNT=$(echo "${VTREPORT}" | jq -r '.data.attributes.stats.undetected')
    local VT_SUSPICIOUS_COUNT=$(echo "${VTREPORT}" | jq -r '.data.attributes.stats.suspicious')
    local VT_MALICIOUS_COUNT=$(echo "${VTREPORT}" | jq -r '.data.attributes.stats.malicious')
    local VT_TOTAL=$(("${VT_HARMLESS_COUNT}" + "${VT_UNDETECTED_COUNT}" + "${VT_SUSPICIOUS_COUNT}" + "${VT_MALICIOUS_COUNT}"))
    local VT_POSITIVES=$(("${VT_SUSPICIOUS_COUNT}" + "${VT_MALICIOUS_COUNT}"))
    
    # If VT_TOTAL is still 0, sleep for 20 seconds and rerun VT_REPORT
    if [[ ${VT_TOTAL} -eq 0 ]]; then
        echo "VirusTotal: Waiting for additional 20s for results."
        sleep 20
        VTREPORT=$(curl -s -X GET --url "https://www.virustotal.com/api/v3/analyses/${VT_SCAN_ID}" --header "x-apikey: ${VTAPI_KEY}")
        VT_HARMLESS_COUNT=$(echo "${VTREPORT}" | jq -r '.data.attributes.stats.harmless')
        VT_UNDETECTED_COUNT=$(echo "${VTREPORT}" | jq -r '.data.attributes.stats.undetected')
        VT_SUSPICIOUS_COUNT=$(echo "${VTREPORT}" | jq -r '.data.attributes.stats.suspicious')
        VT_MALICIOUS_COUNT=$(echo "${VTREPORT}" | jq -r '.data.attributes.stats.malicious')
        VT_TOTAL=$(("${VT_HARMLESS_COUNT}" + "${VT_UNDETECTED_COUNT}" + "${VT_SUSPICIOUS_COUNT}" + "${VT_MALICIOUS_COUNT}"))
        VT_POSITIVES=$(("${VT_SUSPICIOUS_COUNT}" + "${VT_MALICIOUS_COUNT}"))
    fi

    # Print the results
    echo "VirusTotal:"
    echo "    Submitted URL: $URL"
    echo "    VT Detection Count: ${VT_POSITIVES}/${VT_TOTAL}"
    echo "    VT Link: https://virustotal.com/gui/url/${VT_URL}"  
    echo ""

}

__VirusTotalDebug__ () {
    echo "--------------------------------"
    echo "----------DEBUG OUTPUT----------"
    echo "--------------------------------"
    echo "Input URL Base64: ${InputURLBase64}"
    echo "Input URL Sha256: ${InputURLSha256}"
    echo "VT SCAN ID: ${VT_SCAN_ID}"
    echo "VT REPORT JSON: ${VTREPORT}"
    echo "VT UNDETECTED: ${VT_UNDETECTED_COUNT}"
    echo "VT HARMLESS:   ${VT_HARMLESS_COUNT}"
    echo "VT SUSPICIOUS: ${VT_SUSPICIOUS_COUNT}"
    echo "VT MALICIOUS:  ${VT_MALICIOUS_COUNT}"
    echo "VT MATH TOTAL: ${VT_TOTAL}"
    echo "VT MATH DETECTED: ${VT_POSITIVES}"
    echo "--------------------------------"
}
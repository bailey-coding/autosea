import re
import sys
import validators

def deobfuscate_url(url):
    # Check and deobfuscate `http/s` in all common ways
    url = re.sub(r'hxxp[s]?[:\[\(\{\]\)\}]*//', lambda m: 'https://' if 's' in m.group(0) else 'http://', url, flags=re.IGNORECASE)
    
    # Check and deobfuscate full enclosure of the scheme in any type of braces like [https://], (https://), {https://}
    braces = r'[\[\(\{][^/\s]*?://[^/\s]*?[\]\)\}]'
    url = re.sub(braces, lambda m: m.group(0)[1:-1], url)
    
    # Check and deobfuscate `.` in all common ways
    url = re.sub(r'[\[\(\{\s]*[\.\s]+[\]\)\}\s]*', '.', url)
    
    return url.strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 deobfuscator.py <URL>")
        sys.exit(1)
    
    obfuscated_url = sys.argv[1]
    deobfuscated_url = deobfuscate_url(obfuscated_url)
    
    if validators.url(deobfuscated_url):
        print(deobfuscated_url)
    else:
        print(f"The URL was deobfuscated to {deobfuscated_url}, does this look correct?")

if __name__ == "__main__":
    main()

import re
import sys
import validators

def deobfuscate_url(url):
    # check and deobscufate `http/s`` in all the common ways
    url = re.sub(r'hxxp[s]?[:\[\(\{\]\)\}]*//', lambda m: 'https://' if 's' in m.group(0) else 'http://', url, flags=re.IGNORECASE)
    
    # check and deobscufate full enclosure of the scheme in any type of braces like [https://], (https://), {https://}
    # Note: We use separate patterns for each type of brace to maintain clarity and ensure correct matching
    url = re.sub(r'\[(https?)://\]', r'\1://', url)  # Square brackets
    url = re.sub(r'\((https?)://\)', r'\1://', url)  # Parentheses
    url = re.sub(r'\{(https?)://\}', r'\1://', url)  # Curly braces
    
    # check and deobscufate `.` in all the common ways
    url = re.sub(r'[\[\(\{\s]*[\.\s]+[\]\)\}\s]*', '.', url)
    return url


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
        exit(1)
if __name__ == "__main__":
    main()

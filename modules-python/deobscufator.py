import re
import sys
import validators


def deobfuscate_url(url):
    """
    Deobfuscates a given URL by handling obfuscation of 'http/s' and '.' characters in common ways.
    - Replaces 'hxxp[s]://', 'hxxps://', etc., with 'http://' or 'https://'.
    - Removes any enclosing brackets or braces around the URL scheme.
    - Replaces various obfuscated forms of '.' with a single dot.
    """

    # Deobfuscate `http/s` in all common ways
    url = re.sub(
        r"hxxp[s]?[:\[\(\{\]\)\}]*//",
        lambda m: "https://" if "s" in m.group(0) else "http://",
        url,
        flags=re.IGNORECASE,
    )

    # Remove enclosing brackets or braces around the URL scheme
    url = re.sub(r"[\[\(\{]?(https?://)[\]\)\}]?", r"\1", url)

    # Replace obfuscated forms of '.' with a single dot
    url = re.sub(r"[\[\(\{\s]*[\.\s]+[\]\)\}\s]*", ".", url)

    return url.strip()


def main():
    """
    Main function to handle command-line input, deobfuscate the provided URL, and validate it.
    """
    if len(sys.argv) < 2:
        print("Usage: python3 deobfuscator.py <URL>")
        sys.exit(1)

    obfuscated_url = sys.argv[1]
    deobfuscated_url = deobfuscate_url(obfuscated_url)

    if validators.url(deobfuscated_url):
        print(deobfuscated_url)
    else:
        print(
            f"The URL was deobfuscated to {deobfuscated_url}, does this look correct?"
        )


if __name__ == "__main__":
    main()

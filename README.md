# AutoSea:
The Internet is like a giant body of water, everything connected in ways we might not always *sea*.
This tool (AutoSea) allows Trust & Safety teams as well as Abuse Researchers to get a rough but very quick output of everything related to an input domain and what might show up related to it. 

## Installation:
clone repo, copy ./data/.env.example to ./data/.env and add your own virustotal API key, as found here. https://support.virustotal.com/hc/en-us/articles/115002100149-API
If you're on macOS, ensure you have brew, Python3, and Pip installed, and then run `python3 -m pip install -r /path/to/repository/data/python-requirements.txt --break-system-packages`
If you're on linux, the tool *should* successfully install all requirements.  You can run the install phase with the following: `/path/to/repository/core.sh --install-requirements`


## Releases:
The most current release can be found on my Github, https://github.com/wafflethief123/autosea
## Exit Codes
| Exit Code | Purpose |
|---|---|
| 1 | General Exit, always accompinied with text reason. |
| 2 | Bad Domain Entry, did not parse/pass regex. |
| 3 | Bad Domain Entry, no URL provided. |

## Contributing: 
If you have an idea for a change, or wrote an addon module, function, etc, by all means please make a Pull Request/Change Request against the repo with your additional code or tooling.  The desired output is yaml syntaxed to make pasting to notes easy, and looks roughly like so:
```
commandName:
    response:
        thing: output value
        another thing: with a value
        a list:
        - item 1
        - item 2
``` 

all you need to do is put the desired addon module in the workding directory, and it will be sourced on startup. If there are any requirements, add them to the YAML list in ./data/requirements.yml following the existing syntax.
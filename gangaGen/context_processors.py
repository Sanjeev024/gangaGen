import re

def extract_start_end(domain):
    match = re.search(r'\((\d+)-(\d+)\)', domain)
    if match:
        start = int(match.group(1))
        end = int(match.group(2))
        return start, end
    return None, None
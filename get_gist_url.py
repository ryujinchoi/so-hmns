import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()
    match = re.search(r'https://gist\.github\.com/ryujinchoi/[a-f0-9]+', content)
    if match:
        print(f"\n[🌐 SO-HMNS MASTER GIST NODE]\n{match.group(0)}\n")

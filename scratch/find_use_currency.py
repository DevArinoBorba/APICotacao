import os
import glob
import urllib.request
import re

# Vamos procurar nos outros chunks baixados ou baixar os demais chunks
with open("scratch/atacadoconnect.html", "r", encoding="utf-8") as f:
    html = f.read()

scripts = re.findall(r'src=["\'](/_next/static/chunks/[^"\']+)["\']', html)
base_url = "https://atacadoconnect.com"

for s in scripts:
    js_url = base_url + s
    try:
        req = urllib.request.Request(js_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            if "useCurrency" in content:
                print(f"Found 'useCurrency' in {s}")
                # Procura por fetch, axios, endpoints em volta de useCurrency
                for m in re.finditer(r'useCurrency\b', content):
                    start = max(0, m.start() - 300)
                    end = min(len(content), m.end() + 1000)
                    print(content[start:end])
                    print("=" * 60)
            if "cotacao" in content.lower() or "cambio" in content.lower():
                matches = re.findall(r'https?://[^\s"\'`<>]+', content)
                for u in matches:
                    if any(x in u.lower() for x in ['api', 'cotacao', 'cambio', 'currency', 'rate']):
                        print(f"URL interessante em {s}: {u}")
    except Exception as e:
        print(f"Error {s}: {e}")

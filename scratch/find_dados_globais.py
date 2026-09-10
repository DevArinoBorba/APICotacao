with open("scratch/atacadoconnect.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
import urllib.request

scripts = re.findall(r'src=["\'](/_next/static/chunks/[^"\']+)["\']', html)
base_url = "https://atacadoconnect.com"

for s in scripts:
    js_url = base_url + s
    try:
        req = urllib.request.Request(js_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            if "useDadosGlobais" in content:
                print(f"\n==== ENCONTROU useDadosGlobais EM {s} ====")
                for m in re.finditer(r'useDadosGlobais\b', content):
                    start = max(0, m.start() - 200)
                    end = min(len(content), m.end() + 1500)
                    print(content[start:end])
                    print("-" * 50)
            if "getCurrencyRate" in content:
                print(f"\n==== ENCONTROU getCurrencyRate EM {s} ====")
                for m in re.finditer(r'getCurrencyRate\b', content):
                    start = max(0, m.start() - 200)
                    end = min(len(content), m.end() + 800)
                    print(content[start:end])
                    print("-" * 50)
    except Exception as e:
        print(e)

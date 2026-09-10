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
            # Procura a criação do Context ou Provider de DadosGlobais
            if "DadosGlobaisContext" in content or "DadosGlobaisProvider" in content or "useDadosGlobais=" in content or "useDadosGlobais:" in content:
                print(f"ENCONTROU PROVIDER EM {s}")
                pos = content.find("DadosGlobais")
                print(content[max(0, pos-300):min(len(content), pos+1500)])
            # Procura rotas de API no Next.js
            api_routes = re.findall(r'["\'](/api/[^"\']+)["\']', content)
            if api_routes:
                print(f"Rotas em {s}:", set(api_routes))
    except Exception as e:
        pass

import urllib.request
import re
import json

base_url = "https://atacadoconnect.com"

# Pega todos os scripts listados
with open("scratch/atacadoconnect.html", "r", encoding="utf-8") as f:
    html = f.read()

scripts = re.findall(r'src=["\'](/_next/static/chunks/[^"\']+)["\']', html)
print(f"Total chunks encontrados: {len(scripts)}")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

found_apis = set()
rate_keywords = ['cota', 'cambio', 'dolar', 'currency', 'rate', 'price', 'usd', 'brl', 'pyg']

for s in scripts:
    js_url = base_url + s
    try:
        req = urllib.request.Request(js_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            
            # Procura URLs completas
            urls = re.findall(r'https?://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(?:/[^\s"\'\`<>{}]*)?', content)
            for u in urls:
                if any(k in u.lower() for k in ['api', 'cotacao', 'cambio', 'currency', 'rate', 'backend', 'service', 'dolar']):
                    found_apis.add(u)
                    print(f"[{s}] -> API encontrada: {u}")
                    
            # Procura strings que mencionam "Cotação Dólar"
            if "Cotação Dólar" in content or "Cota" in content:
                # busca onde isso ocorre
                for m in re.finditer(r'Cota[çc][ãa]o\s*D[óo]lar', content, re.IGNORECASE):
                    start = max(0, m.start() - 200)
                    end = min(len(content), m.end() + 300)
                    print(f"\n--- Trecho relevante em {s} ---")
                    print(content[start:end])
                    print("--------------------------------")
    except Exception as e:
        print(f"Erro em {s}: {e}")

print("\nTodas as APIs encontradas nos chunks:")
for a in sorted(found_apis):
    print("  *", a)

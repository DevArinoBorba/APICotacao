import re
import json

with open("scratch/atacadoconnect.html", "r", encoding="utf-8") as f:
    html = f.read()

# Procura __NEXT_DATA__
next_data_match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
if next_data_match:
    print("Encontrou __NEXT_DATA__!")
    try:
        data = json.loads(next_data_match.group(1))
        print("Keys:", list(data.keys()))
        props = data.get("props", {})
        page_props = props.get("pageProps", {})
        print("pageProps keys:", list(page_props.keys()))
        with open("scratch/next_data.json", "w", encoding="utf-8") as out:
            json.dump(data, out, indent=2, ensure_ascii=False)
        print("Salvo em scratch/next_data.json")
    except Exception as e:
        print("Erro json:", e)
else:
    print("Não encontrou __NEXT_DATA__ clássico (pode ser Next.js App Router).")

# Busca por qualquer ocorrência de cotação ou valores numéricos de câmbio (ex: 5.xx, 5xxx, 1xxx)
matches = re.findall(r'Cotação|Cambio|Câmbio|Dólar|Dolar|Guarani|PYG|BRL|ARS', html, re.IGNORECASE)
print("Menções no texto:", len(matches), set(matches))

# Se for Next.js App Router, procura self.__next_f.push
app_router_chunks = re.findall(r'self\.__next_f\.push\(\[(.*?)\]\)', html, re.DOTALL)
print(f"Chunks App Router: {len(app_router_chunks)}")

# Busca todas as strings no html que contenham cotação, câmbio, dólar
padroes = [
    r'([^\"]*(?:cotação|cotacao|dólar|dolar|câmbio|cambio|guarani|peso)[^\"]*)',
    r'https?://[^\s\"\'<>]+',
    r'/api/[^\s\"\'<>]+'
]

urls = re.findall(r'https?://[^\s\"\'<>]+', html)
api_urls = [u for u in set(urls) if any(k in u.lower() for k in ['api', 'cotacao', 'cambio', 'currency', 'rate', 'backend', 'service'])]
print("\nURLs de APIs encontradas no HTML:")
for u in api_urls:
    print("  >", u)

internal_apis = set(re.findall(r'["\'](/api/[^"\']+)["\']', html))
print("\nRotas /api internas encontradas:")
for a in internal_apis:
    print("  >", a)

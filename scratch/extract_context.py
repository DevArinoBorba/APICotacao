with open("scratch/atacadoconnect.html", "r", encoding="utf-8") as f:
    html = f.read()

import re

# Procurar onde 'cotação' ou 'dólar' aparece com contexto
for m in re.finditer(r'(?:cotação|dólar|cotacao|dolar|cambio|câmbio)', html, re.IGNORECASE):
    start = max(0, m.start() - 150)
    end = min(len(html), m.end() + 200)
    snippet = html[start:end]
    # Limpa tags html excessivas
    clean = re.sub(r'<[^>]+>', ' ', snippet)
    clean = re.sub(r'\s+', ' ', clean)
    print("MATCH:", clean)
    print("-" * 60)

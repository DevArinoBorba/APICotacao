import urllib.request
import re
import json

url = "https://atacadoconnect.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
        print(f"Page fetched. Length: {len(html)}")

        # Salva o html para inspecionar se necessário
        with open("scratch/atacadoconnect.html", "w", encoding="utf-8") as f:
            f.write(html)

        # Procura referências a cotação, dólar, câmbio
        linhas_cambio = [linha.strip() for linha in html.splitlines() if any(w in linha.lower() for w in ["câmbio", "cambio", "cotação", "cotacao", "dolar", "dólar", "guarani", "peso", "pyg", "ars", "r$", "u$s", "us$"])]
        print(f"Linhas com termos de câmbio encontradas: {len(linhas_cambio)}")
        for l in linhas_cambio[:20]:
            print("  >", l[:120])

        # Procura scripts
        scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', html, re.IGNORECASE)
        print(f"\nScripts externos ({len(scripts)}):")
        for s in scripts:
            print("  -", s)

        # Procura blocos script inline com dados json ou configs
        inline_scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
        print(f"\nScripts inline: {len(inline_scripts)}")
        for i, s in enumerate(inline_scripts):
            if any(w in s.lower() for w in ["cambio", "cotacao", "dolar", "currency", "rates", "exchange"]):
                print(f"--- Script inline {i} contém termos de câmbio ---")
                print(s[:300])

except Exception as e:
    print(f"Erro ao acessar {url}: {e}")

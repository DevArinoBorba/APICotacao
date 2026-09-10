import urllib.request
import re

url = "https://atacadoconnect.com/_next/static/chunks/ddacb3c966098671.js?dpl=dpl_C8BQWUugKJumu9y9rPvDeVvUeBS9"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    content = resp.read().decode("utf-8", errors="ignore")

# Salva esse chunk para análise
with open("scratch/header_chunk.js", "w", encoding="utf-8") as f:
    f.write(content)

idx = content.find("Cotação Dólar")
if idx == -1:
    idx = content.find("Cota")

start = max(0, idx - 1500)
end = min(len(content), idx + 2000)
print(content[start:end])

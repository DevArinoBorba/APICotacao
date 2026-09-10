with open("scratch/header_chunk.js", "r", encoding="utf-8") as f:
    content = f.read()

import re

# Procura a definição de ez e as funções em volta
matches = re.findall(r'(?:const|let|var)\s+ez\s*=\s*\[[^\]]+\]', content)
print("Definição de ez:", matches)

# Procura o hook que busca os dados de câmbio (useQuery, useSWR, fetch, useEffect)
# Procura onde eE é definido:
for m in re.finditer(r'(?:const|let|function)\s+eE\b', content):
    start = max(0, m.start() - 100)
    end = min(len(content), m.end() + 500)
    print("Definição de eE:\n", content[start:end])
    print("-" * 50)

# Procura chamadas de API ou stores (zustand, redux, context)
for m in re.finditer(r'(?:useCurrency|useExchange|useRate|useCotacao|api/|/api)', content):
    start = max(0, m.start() - 100)
    end = min(len(content), m.end() + 200)
    print("Match de store/api:\n", content[start:end])
    print("-" * 50)

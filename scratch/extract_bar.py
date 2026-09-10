with open("scratch/blackshark.html", "r", encoding="utf-8") as f:
    html = f.read()

pos = html.find("currency-rates-bar")
if pos != -1:
    start = max(0, pos - 200)
    end = min(len(html), pos + 3500)
    with open("scratch/blackshark_rates_snippet.html", "w", encoding="utf-8") as out:
        out.write(html[start:end])
    print("Salvo em scratch/blackshark_rates_snippet.html!")
    print(html[start:start+1500])
else:
    print("Não encontrou currency-rates-bar")

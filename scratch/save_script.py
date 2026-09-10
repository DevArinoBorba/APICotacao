with open("scratch/blackshark.html", "r", encoding="utf-8") as f:
    html = f.read()

pos = html.find("currency-rates-items-currency-rates-bar")
if pos != -1:
    end = html.find("</script>", pos)
    with open("scratch/script_loja.js", "w", encoding="utf-8") as out:
        out.write(html[pos:end+9])
    print("Salvo com sucesso em scratch/script_loja.js")

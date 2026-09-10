with open("scratch/blackshark.html", "r", encoding="utf-8") as f:
    html = f.read()

pos = html.find("currency-rate-loading")
if pos != -1:
    end = html.find("</script>", pos)
    print(html[pos:end+10])

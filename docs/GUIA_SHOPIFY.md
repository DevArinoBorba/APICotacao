# Guia de Integração na Shopify

Este guia explica como integrar a API de cotação do dólar e conversão para **Real (BRL)**, **Guarani (PYG)** e **Peso Argentino (ARS)** na sua loja Shopify.

---

## Opção 1: Ticker / Barra Superior com as Cotações ao Vivo

1. No painel da Shopify, vá em **Loja Virtual** > **Temas**.
2. Clique no botão de três pontos (`...`) ao lado do seu tema ativo e selecione **Editar código**.
3. No menu à esquerda, abra o arquivo `layout/theme.liquid`.
4. Logo após a tag de abertura `<body>` (ou logo acima do cabeçalho da loja), adicione:

```html
<!-- Barra de Cotação de Moedas ao Vivo -->
<div id="ticker-cotacoes-moedas"></div>
<script src="https://SUA_API_URL/static/widget.js" data-ticker="#ticker-cotacoes-moedas" async></script>
```

*(Substitua `https://SUA_API_URL` pelo link onde sua API estiver hospedada)*

---

## Opção 2: Conversão Automática de Preços dos Produtos

Se a sua loja vende ou precifica em Dólar (USD) e você quer mostrar aos clientes o valor convertido em Real, Guarani ou Peso:

1. No arquivo `sections/main-product.liquid` (ou no snippet de card de produto `snippets/card-product.liquid`):
2. Adicione o atributo `data-usd`:

```liquid
<div class="preco-container">
  <span class="preco-usd">{{ product.price | money }}</span>
  <span data-usd="{{ product.price | divided_by: 100.0 }}" class="preco-convertido" style="color: #10b981; font-weight: bold; margin-left: 8px;">
    Calculando...
  </span>
</div>
```

3. No final do arquivo `layout/theme.liquid`, antes de `</body>`, adicione o seletor de moedas e o script:

```html
<!-- Seletor de moedas no rodapé ou cabeçalho -->
<div id="seletor-moedas"></div>

<script src="https://SUA_API_URL/static/widget.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', () => {
    // Renderiza o seletor de moedas (BRL, PYG, ARS, USD)
    CotacaoMoedas.renderSeletor('#seletor-moedas');
    
    // Converte automaticamente todos os preços marcados com data-usd
    CotacaoMoedas.autoConverter();
  });
</script>
```

---

## Opção 3: Consumo Direto via JavaScript (Fetch puro)

Você pode fazer requisições diretas via script no tema:

```javascript
fetch('https://SUA_API_URL/api/cotacoes')
  .then(res => res.json())
  .then(data => {
    console.log('Cotação USD/BRL:', data.cotacoes.BRL.compra);
    console.log('Cotação USD/PYG:', data.cotacoes.PYG.compra);
    console.log('Cotação USD/ARS:', data.cotacoes.ARS.compra);
  });
```
Como o **CORS está totalmente liberado**, não haverá nenhum bloqueio no navegador dos seus clientes.

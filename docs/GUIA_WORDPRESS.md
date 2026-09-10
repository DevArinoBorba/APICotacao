# Guia de Integração no WordPress / WooCommerce

Este guia ensina como exibir as cotações em tempo real e fazer conversões no seu site WordPress ou loja WooCommerce.

---

## Opção 1: Shortcode PHP no `functions.php` (Recomendado para WooCommerce)

Adicione o código abaixo no arquivo `functions.php` do seu tema filho (ou através do plugin *WPCode* / *Code Snippets*):

```php
/**
 * Shortcode [cotacao_dolar] para exibir as cotações ao vivo no WordPress
 */
function exibir_cotacao_dolar_shortcode($atts) {
    // URL da sua API
    $api_url = 'https://SUA_API_URL/api/cotacoes';

    // Tenta pegar do cache transitório do WordPress para velocidade máxima
    $dados = get_transient('cotacao_dolar_cache');

    if (false === $dados) {
        $resposta = wp_remote_get($api_url, array('timeout' => 5));
        if (is_wp_error($resposta)) {
            return '<span class="cotacao-erro">Cotação indisponível no momento.</span>';
        }
        $body = wp_remote_retrieve_body($resposta);
        $dados = json_decode($body, true);
        // Salva em cache no WordPress por 60 segundos
        set_transient('cotacao_dolar_cache', $dados, 60);
    }

    if (!isset($dados['cotacoes'])) {
        return '<span class="cotacao-erro">Dados não encontrados.</span>';
    }

    $brl = number_format($dados['cotacoes']['BRL']['compra'], 2, ',', '.');
    $pyg = number_format($dados['cotacoes']['PYG']['compra'], 0, ',', '.');
    $ars = number_format($dados['cotacoes']['ARS']['compra'], 2, ',', '.');

    return "
    <div class='box-cotacao-dolar' style='display:inline-flex;gap:15px;background:#f1f5f9;padding:8px 15px;border-radius:8px;font-size:14px;font-weight:600;'>
        <span>🇧🇷 USD/BRL: R$ {$brl}</span>
        <span>🇵🇾 USD/PYG: ₲ {$pyg}</span>
        <span>🇦🇷 USD/ARS: $ {$ars}</span>
    </div>
    ";
}
add_shortcode('cotacao_dolar', 'exibir_cotacao_dolar_shortcode');
```

**Como usar:**
Insira o shortcode `[cotacao_dolar]` em qualquer página, post, widget de texto ou no Elementor.

---

## Opção 2: Inserção via Elementor ou Bloco HTML

Se você usa o Elementor ou o editor de blocos (Gutenberg):
1. Adicione um widget **HTML Customizado** / **HTML**.
2. Cole o código:

```html
<div id="barra-cotacoes-topo"></div>
<script src="https://SUA_API_URL/static/widget.js" data-ticker="#barra-cotacoes-topo" async></script>
```

---

## Opção 3: Conversor Dinâmico de Valores via JavaScript

Para converter um valor digitado pelo cliente diretamente na página:

```html
<input type="number" id="valor-dolar" placeholder="Valor em USD" value="100">
<p id="resultado-conversao">Convertendo...</p>

<script>
  async function converter() {
    const valor = document.getElementById('valor-dolar').value;
    const res = await fetch(`https://SUA_API_URL/api/converter?valor=${valor}`);
    const data = await res.json();
    document.getElementById('resultado-conversao').innerHTML = `
      Real: ${data.conversoes.BRL.valor_formatado} | 
      Guarani: ${data.conversoes.PYG.valor_formatado} | 
      Peso: ${data.conversoes.ARS.valor_formatado}
    `;
  }
  document.getElementById('valor-dolar').addEventListener('input', converter);
  converter();
</script>
```

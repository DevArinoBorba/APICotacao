/**
 * Widget Universal de Cotação e Conversão de Moedas (USD -> BRL / PYG / ARS)
 * Compatível com: Shopify, WordPress / WooCommerce, Elementor, HTML puro, etc.
 * 
 * Uso rápido:
 * <script src="https://SEU_DOMINIO/static/widget.js" data-auto="true"></script>
 */

(function () {
  'use strict';

  // Descobre a URL base da API dinamicamente
  const currentScript = document.currentScript;
  let apiBase = '';
  if (currentScript && currentScript.src) {
    const url = new URL(currentScript.src);
    apiBase = `${url.protocol}//${url.host}`;
  }
  if (currentScript && currentScript.getAttribute('data-api')) {
    apiBase = currentScript.getAttribute('data-api');
  }

  const CotacaoMoedas = {
    apiBase: apiBase,
    cacheCotacoes: null,
    moedaAtiva: localStorage.getItem('cotacao_moeda_ativa') || 'BRL',

    /**
     * Busca cotações atualizadas da API
     */
    async obterCotacoes(forcar = false) {
      if (!forcar && this.cacheCotacoes) {
        return this.cacheCotacoes;
      }
      try {
        const res = await fetch(`${this.apiBase}/api/cotacoes`);
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const data = await res.json();
        this.cacheCotacoes = data;
        window.dispatchEvent(new CustomEvent('cotacao:atualizada', { detail: data }));
        return data;
      } catch (err) {
        console.error('[CotacaoMoedas] Erro ao carregar cotações:', err);
        return null;
      }
    },

    /**
     * Converte um valor numérico
     */
    async converter(valor, de = 'USD', para = 'BRL') {
      try {
        const params = new URLSearchParams({ valor, de, para });
        const res = await fetch(`${this.apiBase}/api/converter?${params.toString()}`);
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return await res.json();
      } catch (err) {
        console.error('[CotacaoMoedas] Erro ao converter valor:', err);
        return null;
      }
    },

    /**
     * Converte em tempo real todos os elementos do DOM com [data-usd] ou [data-price-usd]
     * Ideal para vitrines de lojas virtuais (Shopify e WooCommerce)
     */
    async autoConverter(moedaDestino) {
      if (moedaDestino) {
        this.moedaAtiva = moedaDestino;
        localStorage.setItem('cotacao_moeda_ativa', moedaDestino);
      }
      const moeda = this.moedaAtiva;
      const data = await this.obterCotacoes();
      if (!data || !data.cotacoes) return;

      const cotacao = data.cotacoes[moeda];
      const taxa = moeda === 'USD' ? 1.0 : (cotacao ? cotacao.compra : null);
      if (!taxa) return;

      const elementos = document.querySelectorAll('[data-usd], [data-price-usd]');
      elementos.forEach((el) => {
        const valorOriginal = parseFloat(el.getAttribute('data-usd') || el.getAttribute('data-price-usd'));
        if (isNaN(valorOriginal)) return;

        const valorConvertido = valorOriginal * taxa;
        let formatado = '';

        if (moeda === 'PYG') {
          formatado = '₲ ' + Math.round(valorConvertido).toLocaleString('de-DE');
        } else if (moeda === 'BRL') {
          formatado = 'R$ ' + valorConvertido.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        } else if (moeda === 'ARS') {
          formatado = '$ ' + valorConvertido.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        } else {
          formatado = '$ ' + valorConvertido.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        }

        el.textContent = formatado;
      });

      window.dispatchEvent(new CustomEvent('moeda:alterada', { detail: { moeda, taxa } }));
    },

    /**
     * Renderiza um Ticker (barra superior animada) com cotações
     */
    async renderTicker(selector) {
      const container = typeof selector === 'string' ? document.querySelector(selector) : selector;
      if (!container) return;

      const data = await this.obterCotacoes();
      if (!data || !data.cotacoes) return;

      const { BRL, PYG, ARS } = data.cotacoes;

      const formatBadge = (c) => {
        const varNum = c.variacao_pct || 0;
        const color = varNum >= 0 ? '#10b981' : '#ef4444';
        const arrow = varNum >= 0 ? '▲' : '▼';
        return `<span style="display:inline-flex;align-items:center;gap:4px;margin-right:20px;font-family:sans-serif;font-size:13px;">
          <strong>USD/${c.codigo}:</strong> ${c.simbolo} ${c.compra.toLocaleString()} 
          <span style="color:${color};font-size:11px;font-weight:bold;">${arrow} ${Math.abs(varNum)}%</span>
        </span>`;
      };

      container.innerHTML = `
        <div style="background:#0f172a;color:#f8fafc;padding:8px 16px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #334155;flex-wrap:wrap;gap:8px;">
          <div style="display:flex;align-items:center;flex-wrap:wrap;">
            <span style="background:#2563eb;color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:bold;margin-right:16px;">AO VIVO</span>
            ${formatBadge(BRL)}
            ${formatBadge(PYG)}
            ${formatBadge(ARS)}
          </div>
          <div style="font-size:11px;color:#94a3b8;">
            Atualizado a cada 30s
          </div>
        </div>
      `;
    },

    /**
     * Renderiza um seletor de moedas elegante para os clientes da loja
     */
    renderSeletor(selector) {
      const container = typeof selector === 'string' ? document.querySelector(selector) : selector;
      if (!container) return;

      container.innerHTML = `
        <div style="display:inline-flex;align-items:center;background:#1e293b;border:1px solid #475569;border-radius:8px;padding:4px 8px;font-family:system-ui,sans-serif;">
          <span style="font-size:12px;color:#94a3b8;margin-right:6px;">Moeda:</span>
          <select id="cotacao-currency-select" style="background:transparent;color:#f8fafc;border:none;outline:none;font-weight:600;cursor:pointer;font-size:13px;">
            <option value="BRL" style="background:#1e293b;color:#fff;" ${this.moedaAtiva === 'BRL' ? 'selected' : ''}>🇧🇷 BRL (Real)</option>
            <option value="PYG" style="background:#1e293b;color:#fff;" ${this.moedaAtiva === 'PYG' ? 'selected' : ''}>🇵🇾 PYG (Guarani)</option>
            <option value="ARS" style="background:#1e293b;color:#fff;" ${this.moedaAtiva === 'ARS' ? 'selected' : ''}>🇦🇷 ARS (Peso)</option>
            <option value="USD" style="background:#1e293b;color:#fff;" ${this.moedaAtiva === 'USD' ? 'selected' : ''}>🇺🇸 USD (Dólar)</option>
          </select>
        </div>
      `;

      const select = container.querySelector('#cotacao-currency-select');
      select.addEventListener('change', (e) => {
        this.autoConverter(e.target.value);
      });
    }
  };

  // Expõe globalmente
  window.CotacaoMoedas = CotacaoMoedas;

  // Inicialização automática se configurado
  document.addEventListener('DOMContentLoaded', () => {
    if (currentScript && currentScript.getAttribute('data-auto') === 'true') {
      CotacaoMoedas.autoConverter();
    }
    if (currentScript && currentScript.getAttribute('data-ticker')) {
      CotacaoMoedas.renderTicker(currentScript.getAttribute('data-ticker'));
    }
  });
})();

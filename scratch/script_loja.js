currency-rates-items-currency-rates-bar" class="currency-rates-items">
        <div class="currency-rate-chip skeleton">
          <span class="currency-rate-loading">Carregando cotações...</span>
        </div>
      </div>
    </div>
  </div>

  <style>
    .currency-rates-bar {
      background-color: var(--cr-bg, #0c0c10);
      color: var(--cr-text, #ffffff);
      border-bottom: 1px solid var(--cr-border, #22222a);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      font-size: var(--cr-font-size, 13px);
      padding: 7px 16px;
      line-height: 1.2;
      position: relative;
      z-index: 40;
      width: 100%;
    }

    .currency-rates-container {
      max-width: 1320px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-wrap: wrap;
      gap: 12px 20px;
    }

    .currency-rates-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(229, 9, 20, 0.12);
      border: 1px solid rgba(229, 9, 20, 0.35);
      border-radius: 999px;
      padding: 3px 10px;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      color: var(--cr-accent, #e50914);
      flex-shrink: 0;
    }

    .currency-rates-dot {
      width: 6px;
      height: 6px;
      background-color: var(--cr-accent, #e50914);
      border-radius: 50%;
      box-shadow: 0 0 8px var(--cr-accent, #e50914);
      animation: cr-pulse 2s infinite;
    }

    @keyframes cr-pulse {
      0% { opacity: 0.4; transform: scale(0.9); }
      50% { opacity: 1; transform: scale(1.15); }
      100% { opacity: 0.4; transform: scale(0.9); }
    }

    .currency-rates-items {
      display: inline-flex;
      align-items: center;
      gap: 12px;
      overflow-x: auto;
      scrollbar-width: none;
      -ms-overflow-style: none;
      padding: 2px 0;
    }
    .currency-rates-items::-webkit-scrollbar {
      display: none;
    }

    .currency-rate-chip {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 6px;
      padding: 4px 10px;
      transition: all 0.2s ease;
      white-space: nowrap;
      font-weight: 500;
    }

    .currency-rate-chip:hover {
      background: rgba(255, 255, 255, 0.1);
      border-color: var(--cr-accent, #e50914);
      transform: translateY(-1px);
    }

    .currency-rate-flag {
      width: 18px;
      height: 13px;
      border-radius: 2px;
      object-fit: cover;
      display: block;
      box-shadow: 0 1px 3px rgba(0,0,0,0.5);
    }

    .currency-rate-symbol {
      color: #9da0aa;
      font-size: 11px;
      font-weight: 600;
      margin-right: 1px;
    }

    .currency-rate-value {
      color: #ffffff;
      font-weight: 700;
      letter-spacing: -0.2px;
    }

    .currency-rate-loading {
      color: #888894;
      font-size: 12px;
    }

    @media (max-width: 768px) {
      .currency-rates-bar {
        padding: 6px 10px;
      }
      .currency-rates-container {
        justify-content: flex-start;
        gap: 8px;
        flex-wrap: nowrap;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
      }
      .currency-rates-badge {
        font-size: 10px;
        padding: 2px 7px;
      }
      .currency-rate-chip {
        padding: 3px 8px;
        font-size: 12px;
      }
    }
  </style>

  <script>
    (function() {
      const targetId = 'currency-rates-items-currency-rates-bar';
      function loadRates() {
        fetch('https://economia.awesomeapi.com.br/json/last/USD-BRL,USD-PYG,USD-ARS,USD-EUR')
          .then(res => {
            if (!res.ok) throw new Error('Network error');
            return res.json();
          })
          .then(data => {
            const pyg = data.USDPYG ? Math.round(parseFloat(data.USDPYG.bid)).toLocaleString('en-US') : '---';
            const brl = data.USDBRL ? parseFloat(data.USDBRL.bid).toFixed(2).replace('.', ',') : '---';
            const ars = data.USDARS ? Math.round(parseFloat(data.USDARS.bid)).toLocaleString('en-US') : '---';
            const eur = data.USDEUR ? parseFloat(data.USDEUR.bid).toFixed(2).replace('.', ',') : '---';

            const container = document.getElementById(targetId);
            if (!container) return;

            container.innerHTML = `
              <div class="currency-rate-chip" title="Cotação Dólar para Guarani Paraguaio">
                <img class="currency-rate-flag" src="https://flagcdn.com/w40/py.png" alt="Paraguai" loading="lazy" width="18" height="13">
                <span class="currency-rate-symbol">₲</span>
                <span class="currency-rate-value">${pyg}</span>
              </div>
              <div class="currency-rate-chip" title="Cotação Dólar para Real Brasileiro">
                <img class="currency-rate-flag" src="https://flagcdn.com/w40/br.png" alt="Brasil" loading="lazy" width="18" height="13">
                <span class="currency-rate-symbol">R$</span>
                <span class="currency-rate-value">${brl}</span>
              </div>
              <div class="currency-rate-chip" title="Cotação Dólar para Peso Argentino">
                <img class="currency-rate-flag" src="https://flagcdn.com/w40/ar.png" alt="Argentina" loading="lazy" width="18" height="13">
                <span class="currency-rate-symbol">ARS</span>
                <span class="currency-rate-value">${ars}</span>
              </div>
              <div class="currency-rate-chip" title="Cotação Dólar para Euro">
                <img class="currency-rate-flag" src="https://flagcdn.com/w40/eu.png" alt="União Europeia" loading="lazy" width="18" height="13">
                <span class="currency-rate-symbol">€</span>
                <span class="currency-rate-value">${eur}</span>
              </div>
            `;
          })
          .catch(() => {
            const container = document.getElementById(targetId);
            if (container) {
              container.innerHTML = '<span class="currency-rate-loading">Cotações atualizadas no momento da compra</span>';
            }
          });
      }

      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadRates);
      } else {
        loadRates();
      }
    })();
  </script>
# 💱 API de Cotação do Dólar em Tempo Real (USD → BRL, PYG, ARS)

API REST de alta performance para cotação em tempo real do **Dólar Americano (USD)** e conversão automática para:
- 🇧🇷 **Real Brasileiro (BRL)**
- 🇵🇾 **Guarani Paraguaio (PYG)**
- 🇦🇷 **Peso Argentino (ARS)**

Projetada com **CORS 100% liberado** e componentes plug-and-play para integração direta em **Shopify**, **WordPress / WooCommerce**, lojas virtuais e aplicações web.

---

## 🚀 Funcionalidades

- **Tempo Real**: Cotações atualizadas a cada 30 segundos (AwesomeAPI com fallback automático para Open Exchange Rates).
- **Cache Inteligente**: Respostas ultrarrápidas (< 5ms) com TTL de 30 segundos, evitando sobrecarga ou bloqueio.
- **CORS Universal**: Permite chamadas `fetch()` via JavaScript diretamente da vitrine da sua loja ou site em qualquer domínio.
- **Documentação Interativa**: Swagger UI (`/docs`) e ReDoc (`/redoc`) nativos para testar diretamente pelo navegador.
- **Painel Web Integrado**: Interface moderna em `/` com simulador de conversão e cotações ao vivo.
- **Widget Universal (`widget.js`)**: Script pronto para embutir ticker ou conversor de preços em qualquer site com 1 linha de HTML.
- **Deploy Simplificado**: `Dockerfile` pronto para publicação no Render, Railway, Fly.io ou VPS.

---

## 📦 Instalação e Execução Local

### Pré-requisitos
- Python 3.10 ou superior

### Passo a Passo

1. **Ative o ambiente virtual:**
   ```powershell
   # Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1
   ```

2. **Instale as dependências (já configuradas no ambiente):**
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicie o servidor:**
   ```bash
   python run.py
   ```
   O servidor estará disponível em: `http://localhost:8000`

---

## 🌐 Endpoints da API

### 1. Cotações em Tempo Real
`GET /api/cotacoes`

Retorna os valores atuais de compra, venda, máxima, mínima e variação do Dólar para as três moedas.

**Exemplo de Resposta:**
```json
{
  "sucesso": true,
  "base": "USD",
  "data_atualizacao": "2026-09-10T11:03:20Z",
  "fonte": "AwesomeAPI (Tempo Real)",
  "cotacoes": {
    "BRL": {
      "codigo": "BRL",
      "nome": "Real Brasileiro",
      "simbolo": "R$",
      "compra": 5.1362,
      "venda": 5.1378,
      "maxima": 5.146,
      "minima": 5.1028,
      "variacao_pct": 0.61,
      "data_hora": "2026-09-10 11:03:23"
    },
    "PYG": {
      "codigo": "PYG",
      "nome": "Guarani Paraguaio",
      "simbolo": "₲",
      "compra": 5711.7784,
      "venda": 6073.1201,
      "maxima": 5720.967,
      "minima": 5711.7784,
      "variacao_pct": -0.12,
      "data_hora": "2026-09-10 08:23:19"
    },
    "ARS": {
      "codigo": "ARS",
      "nome": "Peso Argentino",
      "simbolo": "$",
      "compra": 1515.2521,
      "venda": 1515.2621,
      "maxima": 1515.4958,
      "minima": 1512.4427,
      "variacao_pct": 0.1,
      "data_hora": "2026-09-10 11:03:20"
    }
  }
}
```

---

### 2. Conversão de Valores
`GET /api/converter`

#### Parâmetros de Consulta:
| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `valor` | float | Sim | - | Quantia a ser convertida (ex: `100`) |
| `de` | string | Não | `USD` | Moeda de origem: `USD`, `BRL`, `PYG`, `ARS` |
| `para` | string | Não | Todas | Moeda de destino. Se omitido, converte para todas as outras. |

#### Exemplo 1: Converter 100 USD para todas as moedas
`GET /api/converter?valor=100`

```json
{
  "sucesso": true,
  "origem": {
    "moeda": "USD",
    "nome": "Dólar Americano",
    "simbolo": "$",
    "valor": 100.0,
    "valor_formatado": "$ 100.00"
  },
  "data_cotacao": "2026-09-10T11:03:20Z",
  "fonte": "AwesomeAPI (Tempo Real)",
  "conversoes": {
    "BRL": {
      "codigo": "BRL",
      "nome": "Real Brasileiro",
      "simbolo": "R$",
      "taxa": 5.1362,
      "valor_convertido": 513.62,
      "valor_formatado": "R$ 513,62"
    },
    "PYG": {
      "codigo": "PYG",
      "nome": "Guarani Paraguaio",
      "simbolo": "₲",
      "taxa": 5711.7784,
      "valor_convertido": 571178.0,
      "valor_formatado": "₲ 571.178"
    },
    "ARS": {
      "codigo": "ARS",
      "nome": "Peso Argentino",
      "simbolo": "$",
      "taxa": 1515.2521,
      "valor_convertido": 151525.21,
      "valor_formatado": "$ 151.525,21"
    }
  }
}
```

#### Exemplo 2: Conversão específica entre pares
`GET /api/converter?valor=250&de=USD&para=BRL`

---

## 🛍️ Integração com Shopify e WordPress

Consulte os manuais passo a passo dedicados:
- 📖 [Guia de Integração Shopify](file:///c:/Users/arino/Documents/PROJETOS/APIs/Cotação/docs/GUIA_SHOPIFY.md)
- 📖 [Guia de Integração WordPress](file:///c:/Users/arino/Documents/PROJETOS/APIs/Cotação/docs/GUIA_WORDPRESS.md)

### Inclusão Rápida com Widget Universal:
Adicione o código abaixo em qualquer página HTML ou tema para carregar uma barra de cotações ao vivo:
```html
<div id="barra-cotacoes"></div>
<script src="https://SUA_API_URL/static/widget.js" data-ticker="#barra-cotacoes" async></script>
```

---

## 🧪 Testes Automatizados

Para executar os 10 testes automatizados:
```powershell
.\.venv\Scripts\pytest.exe -v tests/
```

---

## ☁️ Como Publicar na Nuvem (Deploy)

### 🥇 Opção Recomendada: Sua VPS com Coolify
O Coolify é a melhor opção pois gera **HTTPS (SSL Let's Encrypt)** automático e roda com consumo ínfimo de memória (< 50MB de RAM).

Consulte o passo a passo completo:
👉 [Guia de Deploy no Coolify](file:///c:/Users/arino/Documents/PROJETOS/APIs/Cotação/docs/GUIA_COOLIFY.md)

1. No Coolify, adicione um novo recurso apontando para seu repositório Git ou usando o arquivo [docker-compose.yml](file:///c:/Users/arino/Documents/PROJETOS/APIs/Cotação/docker-compose.yml).
2. Defina o **Build Pack** como **Dockerfile**.
3. Em **Port**, informe `8000`.
4. Defina seu domínio/subdomínio (ex: `https://cotacao.seudominio.com`).
5. Clique em **Deploy**.

---

### Opção 2: Render.com (Alternativa Gratuita)
1. Crie uma conta no [Render.com](https://render.com).
2. Conecte seu repositório Git.
3. Escolha **Web Service** > Runtime: **Python 3**.
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Opção 3: Railway.app / Fly.io
Basta apontar o repositório no Railway ou executar `fly launch` (utiliza o `Dockerfile` nativamente).

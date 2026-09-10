"""
Configurações da API de Cotação de Moedas
"""

# Tempo de vida do cache em segundos
CACHE_TTL_SECONDS: int = 30

# URLs das fontes de dados
AWESOME_API_URL: str = "https://economia.awesomeapi.com.br/last/USD-BRL,USD-PYG,USD-ARS"
FALLBACK_API_URL: str = "https://open.er-api.com/v6/latest/USD"

# Moedas suportadas
SUPPORTED_CURRENCIES = {
    "USD": {
        "nome": "Dólar Americano",
        "simbolo": "$",
        "decimais": 2,
    },
    "BRL": {
        "nome": "Real Brasileiro",
        "simbolo": "R$",
        "decimais": 2,
    },
    "PYG": {
        "nome": "Guarani Paraguaio",
        "simbolo": "₲",
        "decimais": 0,  # O guarani costumeiramente não utiliza centavos
    },
    "ARS": {
        "nome": "Peso Argentino",
        "simbolo": "$",
        "decimais": 2,
    }
}

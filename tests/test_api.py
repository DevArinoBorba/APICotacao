"""
Testes automatizados para a API de Cotação de Moedas
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Testa o endpoint de saúde do sistema."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "horario" in data


def test_index_page():
    """Testa se a página inicial serve o HTML interativo."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "API de Cotação de Moedas" in response.text


def test_widget_js():
    """Testa se o script do widget universal é servido corretamente."""
    response = client.get("/api/widget.js")
    assert response.status_code == 200
    assert "javascript" in response.headers["content-type"]
    assert "CotacaoMoedas" in response.text


def test_cors_headers():
    """Testa se as origens cruzadas (CORS) estão liberadas para Shopify e WordPress."""
    response = client.options(
        "/api/cotacoes",
        headers={
            "Origin": "https://minha-loja.myshopify.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    # O Starlette CORSMiddleware reflete a origem da loja quando allow_origins=["*"]
    allow_origin = response.headers.get("access-control-allow-origin")
    assert allow_origin in ("*", "https://minha-loja.myshopify.com")


def test_get_cotacoes():
    """Testa o endpoint de cotações ao vivo do Dólar."""
    response = client.get("/api/cotacoes")
    assert response.status_code == 200
    data = response.json()

    assert data["sucesso"] is True
    assert data["base"] == "USD"
    assert "data_atualizacao" in data
    assert "cotacoes" in data

    cotacoes = data["cotacoes"]
    assert "BRL" in cotacoes
    assert "PYG" in cotacoes
    assert "ARS" in cotacoes

    # Verifica valores das moedas
    assert cotacoes["BRL"]["compra"] > 0
    assert cotacoes["PYG"]["compra"] > 0
    assert cotacoes["ARS"]["compra"] > 0

    # Verifica se os símbolos estão corretos
    assert cotacoes["BRL"]["simbolo"] == "R$"
    assert cotacoes["PYG"]["simbolo"] == "₲"
    assert cotacoes["ARS"]["simbolo"] == "$"


def test_get_dados_globais():
    """Testa o endpoint simplificado compatível com o Atacado Connect."""
    response = client.get("/api/dados-globais")
    assert response.status_code == 200
    data = response.json()
    assert "cotacao" in data
    cotacao = data["cotacao"]
    assert "real" in cotacao and cotacao["real"] > 0
    assert "guarani" in cotacao and cotacao["guarani"] > 0
    assert "peso" in cotacao and cotacao["peso"] > 0


def test_conversao_multipla():
    """Testa conversão automática de 100 USD para BRL, PYG e ARS."""
    response = client.get("/api/converter?valor=100")
    assert response.status_code == 200
    data = response.json()

    assert data["sucesso"] is True
    assert data["origem"]["moeda"] == "USD"
    assert data["origem"]["valor"] == 100.0

    conversoes = data["conversoes"]
    assert "BRL" in conversoes
    assert "PYG" in conversoes
    assert "ARS" in conversoes

    assert conversoes["BRL"]["valor_convertido"] > 0
    assert "R$" in conversoes["BRL"]["valor_formatado"]
    assert conversoes["PYG"]["valor_convertido"] > 0
    assert "₲" in conversoes["PYG"]["valor_formatado"]


def test_conversao_especifica():
    """Testa conversão direta de USD para BRL."""
    response = client.get("/api/converter?valor=50&de=USD&para=BRL")
    assert response.status_code == 200
    data = response.json()

    assert data["sucesso"] is True
    assert data["origem"]["moeda"] == "USD"
    assert data["origem"]["valor"] == 50.0
    assert data["destino"]["codigo"] == "BRL"
    assert data["destino"]["valor_convertido"] > 0


def test_conversao_cruzada():
    """Testa conversão de Real (BRL) para Guarani (PYG)."""
    response = client.get("/api/converter?valor=100&de=BRL&para=PYG")
    assert response.status_code == 200
    data = response.json()

    assert data["sucesso"] is True
    assert data["origem"]["moeda"] == "BRL"
    assert data["destino"]["codigo"] == "PYG"
    assert data["destino"]["valor_convertido"] > 0


def test_conversao_moeda_invalida():
    """Testa validação de moeda inexistente."""
    response = client.get("/api/converter?valor=100&de=EUR&para=XYZ")
    assert response.status_code in (400, 422)


def test_conversao_valor_invalido():
    """Testa validação com valor menor ou igual a zero."""
    response = client.get("/api/converter?valor=-50")
    assert response.status_code in (400, 422)

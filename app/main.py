"""
Aplicação Principal FastAPI - API de Cotação de Moedas em Tempo Real
"""
from typing import Optional
from pathlib import Path
from datetime import datetime, timezone

from fastapi import FastAPI, Query, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from app.services.currency import currency_service
from app.schemas.currency import (
    CotacoesResponse,
    ConversaoResponse,
    ConversaoMultiplaResponse,
)

# Diretório base
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="API de Cotação do Dólar em Tempo Real",
    description=(
        "API de alta performance para cotação em tempo real do Dólar Americano (USD) "
        "e conversão automática para Real Brasileiro (BRL), Guarani Paraguaio (PYG) e Peso Argentino (ARS). "
        "Possui CORS totalmente habilitado para integração direta em lojas Shopify, sites WordPress e aplicações web."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuração de CORS Universal (vital para Shopify, WordPress e outros domínios)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite requisições de qualquer origem
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# Monta arquivos estáticos
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", include_in_schema=False)
async def serve_index():
    """Serve a interface visual de simulação e documentação de integração."""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return JSONResponse({"mensagem": "API de Cotação ativa. Acesse /docs para documentação interativa."})


@app.get("/health", tags=["Sistema"])
async def health_check():
    """Verifica a integridade e saúde da API."""
    return {
        "status": "ok",
        "horario": datetime.now(timezone.utc).isoformat(),
        "servico": "API de Cotação de Moedas",
    }


@app.get(
    "/api/cotacoes",
    response_model=CotacoesResponse,
    tags=["Cotações"],
    summary="Cotações em tempo real do Dólar (USD)",
    description=(
        "Retorna as cotações atuais do Dólar em relação ao Real (BRL), "
        "Guarani (PYG) e Peso Argentino (ARS), incluindo preço de compra, venda, máxima, mínima e variação."
    ),
)
async def get_cotacoes(
    response: Response,
    forcar: bool = Query(False, description="Forçar atualização ignorando o cache temporário"),
):
    try:
        dados = await currency_service.get_cotacoes(forcar_atualizacao=forcar)
        # Define cabeçalho de cache público de 30 segundos
        response.headers["Cache-Control"] = "public, max-age=30"
        return dados
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erro ao obter cotações: {str(e)}")


@app.get(
    "/api/converter",
    response_model=None,
    tags=["Conversão"],
    summary="Conversão de valores entre moedas",
    description=(
        "Converte um valor de uma moeda de origem para moeda(s) de destino. "
        "Se o destino não for especificado, converte automaticamente para todas as outras moedas suportadas."
    ),
)
async def converter(
    valor: float = Query(..., gt=0, description="Quantia numérica a ser convertida (ex: 100)"),
    de: str = Query("USD", description="Código da moeda de origem: USD, BRL, PYG, ARS"),
    para: Optional[str] = Query(None, description="Código da moeda de destino (opcional). Deixe vazio para converter para todas."),
):
    try:
        resultado = await currency_service.converter(
            valor=valor,
            moeda_origem=de,
            moeda_destino=para,
        )
        return resultado
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as err:
        raise HTTPException(status_code=502, detail=f"Erro no processamento da conversão: {str(err)}")


@app.get("/api/widget.js", include_in_schema=False)
async def serve_widget():
    """Atalho para servir o script universal de integração para lojas e sites."""
    widget_file = STATIC_DIR / "widget.js"
    return FileResponse(widget_file, media_type="application/javascript")

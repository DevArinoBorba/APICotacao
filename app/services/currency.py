"""
Serviço de busca de cotações em tempo real e conversão de moedas
"""
import time
import logging
from typing import Dict, Optional, Tuple, Union
from datetime import datetime, timezone
import httpx

from app.config import (
    AWESOME_API_URL,
    FALLBACK_API_URL,
    CACHE_TTL_SECONDS,
    SUPPORTED_CURRENCIES,
)
from app.schemas.currency import (
    CotacaoMoeda,
    CotacoesResponse,
    ConversaoItem,
    ConversaoResponse,
    ConversaoMultiplaResponse,
    OrigemConversao,
)

logger = logging.getLogger(__name__)


class CurrencyService:
    def __init__(self):
        self._cache_data: Optional[Dict[str, CotacaoMoeda]] = None
        self._cache_time: float = 0
        self._cache_source: str = ""
        self._cache_last_update: str = ""

    def _format_currency_value(self, valor: float, moeda: str) -> str:
        """Formata o valor monetário de acordo com a moeda e seus costumes locais."""
        config = SUPPORTED_CURRENCIES.get(moeda, {"simbolo": "$", "decimais": 2})
        simbolo = config["simbolo"]
        decimais = config.get("decimais", 2)

        if decimais == 0:
            # Padrão Guarani: ₲ 1.234.567
            formatado = f"{int(round(valor)):,}".replace(",", ".")
            return f"{simbolo} {formatado}"
        else:
            # Padrão BRL e ARS: R$ 1.234,56
            if moeda in ("BRL", "ARS"):
                parte_inteira = f"{int(valor):,}".replace(",", ".")
                centavos = f"{int(round((valor - int(valor)) * 100)):02d}"
                return f"{simbolo} {parte_inteira},{centavos}"
            else:
                # Padrão USD: $ 1,234.56
                return f"{simbolo} {valor:,.2f}"

    def _is_cache_valid(self) -> bool:
        """Verifica se o cache em memória ainda está dentro do TTL."""
        if not self._cache_data:
            return False
        return (time.time() - self._cache_time) < CACHE_TTL_SECONDS

    async def _fetch_from_awesome_api(self) -> Tuple[Dict[str, CotacaoMoeda], str]:
        """Busca cotações em tempo real da AwesomeAPI."""
        async with httpx.AsyncClient(timeout=6.0) as client:
            response = await client.get(AWESOME_API_URL)
            response.raise_for_status()
            data = response.json()

        cotacoes: Dict[str, CotacaoMoeda] = {}
        now_str = datetime.now(timezone.utc).isoformat()

        # Mapeamento dos pares retornados pela AwesomeAPI
        pares = {
            "BRL": data.get("USDBRL"),
            "PYG": data.get("USDPYG"),
            "ARS": data.get("USDARS"),
        }

        for moeda, cotacao in pares.items():
            if not cotacao:
                continue

            cfg = SUPPORTED_CURRENCIES[moeda]
            bid = float(cotacao["bid"])
            ask = float(cotacao.get("ask", bid))
            high = float(cotacao["high"]) if "high" in cotacao and cotacao["high"] else bid
            low = float(cotacao["low"]) if "low" in cotacao and cotacao["low"] else bid
            pct_change = float(cotacao["pctChange"]) if "pctChange" in cotacao and cotacao["pctChange"] else 0.0

            cotacoes[moeda] = CotacaoMoeda(
                codigo=moeda,
                nome=cfg["nome"],
                simbolo=cfg["simbolo"],
                compra=bid,
                venda=ask,
                maxima=high,
                minima=low,
                variacao_pct=round(pct_change, 2),
                data_hora=cotacao.get("create_date", now_str),
            )

        if len(cotacoes) < 3:
            raise ValueError("AwesomeAPI não retornou todas as 3 moedas necessárias")

        return cotacoes, "AwesomeAPI (Tempo Real)"

    async def _fetch_from_fallback_api(self) -> Tuple[Dict[str, CotacaoMoeda], str]:
        """Busca cotações do serviço de fallback (ExchangeRate Open API)."""
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.get(FALLBACK_API_URL)
            response.raise_for_status()
            data = response.json()

        rates = data.get("rates", {})
        cotacoes: Dict[str, CotacaoMoeda] = {}
        now_str = datetime.now(timezone.utc).isoformat()

        for moeda in ["BRL", "PYG", "ARS"]:
            if moeda in rates:
                rate = float(rates[moeda])
                cfg = SUPPORTED_CURRENCIES[moeda]
                cotacoes[moeda] = CotacaoMoeda(
                    codigo=moeda,
                    nome=cfg["nome"],
                    simbolo=cfg["simbolo"],
                    compra=rate,
                    venda=rate,
                    maxima=rate,
                    minima=rate,
                    variacao_pct=0.0,
                    data_hora=now_str,
                )

        if len(cotacoes) < 3:
            raise ValueError("Fallback API não retornou todas as moedas necessárias")

        return cotacoes, "Open Exchange Rates (Fallback)"

    async def get_cotacoes(self, forcar_atualizacao: bool = False) -> CotacoesResponse:
        """Obtém as cotações atuais do Dólar para BRL, PYG e ARS com cache e fallback."""
        if not forcar_atualizacao and self._is_cache_valid() and self._cache_data:
            return CotacoesResponse(
                sucesso=True,
                base="USD",
                data_atualizacao=self._cache_last_update,
                fonte=f"{self._cache_source} (Cache ativo)",
                cotacoes=self._cache_data,
            )

        # Tentativa 1: AwesomeAPI (tempo real a cada 30s)
        try:
            cotacoes, fonte = await self._fetch_from_awesome_api()
        except Exception as err:
            logger.warning(f"Falha ao obter cotações da AwesomeAPI: {err}. Tentando fallback...")
            try:
                cotacoes, fonte = await self._fetch_from_fallback_api()
            except Exception as fallback_err:
                logger.error(f"Falha também no fallback de cotações: {fallback_err}")
                # Se tínhamos cache antigo, devolvemos como último recurso
                if self._cache_data:
                    return CotacoesResponse(
                        sucesso=True,
                        base="USD",
                        data_atualizacao=self._cache_last_update,
                        fonte=f"{self._cache_source} (Dados anteriores)",
                        cotacoes=self._cache_data,
                    )
                raise RuntimeError(f"Não foi possível obter as cotações: {err} / {fallback_err}")

        # Atualiza o cache em memória
        now_iso = datetime.now(timezone.utc).isoformat()
        self._cache_data = cotacoes
        self._cache_time = time.time()
        self._cache_source = fonte
        self._cache_last_update = now_iso

        return CotacoesResponse(
            sucesso=True,
            base="USD",
            data_atualizacao=now_iso,
            fonte=fonte,
            cotacoes=cotacoes,
        )

    async def converter(
        self,
        valor: float,
        moeda_origem: str = "USD",
        moeda_destino: Optional[str] = None,
    ) -> Union[ConversaoResponse, ConversaoMultiplaResponse]:
        """
        Converte valores entre moedas suportadas.
        Se moeda_origem='USD' e moeda_destino=None, converte para BRL, PYG e ARS.
        """
        moeda_origem = moeda_origem.upper().strip()
        if moeda_destino:
            moeda_destino = moeda_destino.upper().strip()

        if moeda_origem not in SUPPORTED_CURRENCIES:
            raise ValueError(f"Moeda de origem '{moeda_origem}' não suportada. Moedas válidas: {list(SUPPORTED_CURRENCIES.keys())}")

        if moeda_destino and moeda_destino not in SUPPORTED_CURRENCIES:
            raise ValueError(f"Moeda de destino '{moeda_destino}' não suportada. Moedas válidas: {list(SUPPORTED_CURRENCIES.keys())}")

        if valor < 0:
            raise ValueError("O valor para conversão deve ser maior ou igual a zero.")

        cotacoes_resp = await self.get_cotacoes()
        cotacoes = cotacoes_resp.cotacoes

        # Taxas em relação a 1 USD (usando a taxa de compra/bid como referência de mercado)
        taxas_para_usd = {
            "USD": 1.0,
            "BRL": cotacoes["BRL"].compra,
            "PYG": cotacoes["PYG"].compra,
            "ARS": cotacoes["ARS"].compra,
        }

        # Primeiro normaliza o valor para USD
        taxa_origem_para_usd = taxas_para_usd[moeda_origem]
        valor_em_usd = valor if moeda_origem == "USD" else (valor / taxa_origem_para_usd)

        origem_info = OrigemConversao(
            moeda=moeda_origem,
            nome=SUPPORTED_CURRENCIES[moeda_origem]["nome"],
            simbolo=SUPPORTED_CURRENCIES[moeda_origem]["simbolo"],
            valor=round(valor, 2 if moeda_origem != "PYG" else 0),
            valor_formatado=self._format_currency_value(valor, moeda_origem),
        )

        # Se não especificou destino (ou pediu 'TODAS'), converte para todas as 3 outras moedas
        if not moeda_destino or moeda_destino in ("TODAS", "ALL"):
            conversoes: Dict[str, ConversaoItem] = {}
            for cod, taxa in taxas_para_usd.items():
                if cod == moeda_origem:
                    continue
                cfg = SUPPORTED_CURRENCIES[cod]
                convertido = valor_em_usd * taxa
                conversoes[cod] = ConversaoItem(
                    codigo=cod,
                    nome=cfg["nome"],
                    simbolo=cfg["simbolo"],
                    taxa=round(taxa if moeda_origem == "USD" else (taxa / taxa_origem_para_usd), 4),
                    valor_convertido=round(convertido, 0 if cod == "PYG" else 2),
                    valor_formatado=self._format_currency_value(convertido, cod),
                )

            return ConversaoMultiplaResponse(
                sucesso=True,
                origem=origem_info,
                data_cotacao=cotacoes_resp.data_atualizacao,
                fonte=cotacoes_resp.fonte,
                conversoes=conversoes,
            )

        # Conversão específica de uma moeda para outra
        taxa_final = 1.0 if moeda_origem == moeda_destino else (taxas_para_usd[moeda_destino] / taxa_origem_para_usd)
        valor_final = valor_em_usd * taxas_para_usd[moeda_destino]

        cfg_dest = SUPPORTED_CURRENCIES[moeda_destino]
        destino_item = ConversaoItem(
            codigo=moeda_destino,
            nome=cfg_dest["nome"],
            simbolo=cfg_dest["simbolo"],
            taxa=round(taxa_final, 4),
            valor_convertido=round(valor_final, 0 if moeda_destino == "PYG" else 2),
            valor_formatado=self._format_currency_value(valor_final, moeda_destino),
        )

        return ConversaoResponse(
            sucesso=True,
            origem=origem_info,
            destino=destino_item,
            data_cotacao=cotacoes_resp.data_atualizacao,
            fonte=cotacoes_resp.fonte,
        )


# Instância singleton do serviço
currency_service = CurrencyService()

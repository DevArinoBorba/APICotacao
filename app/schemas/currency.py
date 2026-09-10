"""
Modelos Pydantic para a API de Cotação de Moedas
"""
from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class CotacaoMoeda(BaseModel):
    codigo: str = Field(..., description="Código da moeda de destino, ex: BRL, PYG, ARS")
    nome: str = Field(..., description="Nome descritivo da moeda")
    simbolo: str = Field(..., description="Símbolo monetário (R$, ₲, $)")
    compra: float = Field(..., description="Preço de compra (Bid)")
    venda: float = Field(..., description="Preço de venda (Ask)")
    maxima: Optional[float] = Field(None, description="Cotação máxima do dia")
    minima: Optional[float] = Field(None, description="Cotação mínima do dia")
    variacao_pct: Optional[float] = Field(None, description="Variação percentual nas últimas 24h")
    data_hora: str = Field(..., description="Data e hora da cotação")


class CotacoesResponse(BaseModel):
    sucesso: bool = True
    base: str = Field("USD", description="Moeda base de referência")
    data_atualizacao: str = Field(..., description="Timestamp da última atualização das cotações")
    fonte: str = Field(..., description="Fonte dos dados (ex: AwesomeAPI ou Fallback)")
    cotacoes: Dict[str, CotacaoMoeda] = Field(..., description="Dicionário com as cotações por código de moeda")


class ConversaoItem(BaseModel):
    codigo: str = Field(..., description="Código da moeda")
    nome: str = Field(..., description="Nome da moeda")
    simbolo: str = Field(..., description="Símbolo monetário")
    taxa: float = Field(..., description="Taxa de câmbio utilizada")
    valor_convertido: float = Field(..., description="Valor calculado na moeda de destino")
    valor_formatado: str = Field(..., description="Valor com símbolo formatado para exibição")


class OrigemConversao(BaseModel):
    moeda: str
    nome: str
    simbolo: str
    valor: float
    valor_formatado: str


class ConversaoMultiplaResponse(BaseModel):
    sucesso: bool = True
    origem: OrigemConversao
    data_cotacao: str
    fonte: str
    conversoes: Dict[str, ConversaoItem]


class ConversaoResponse(BaseModel):
    sucesso: bool = True
    origem: OrigemConversao
    destino: ConversaoItem
    data_cotacao: str
    fonte: str

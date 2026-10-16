from typing import List, Literal

from pydantic import BaseModel, Field


class CryptoAnalysisRequest(BaseModel):
    coin: List[str] = Field(...,description="Provide the List of Coins to analyze")

class MarketFactor(BaseModel):
    factor:str
    impact:str

class CryptoInsights(BaseModel):
    prediction:str
    confidence:int = Field(...,le=100,ge=0)


class CoinMarketAnalysis(BaseModel):
    coin: str
    summary: str
    sentiment: Literal["bullish","neutral","bearish"]
    key_factors: List[MarketFactor]
    insights: List[ CryptoInsights]

class CryptoAnalysisResponse(BaseModel):
    analysis:List[CoinMarketAnalysis]


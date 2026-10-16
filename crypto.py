import json
import os
from json import JSONDecodeError
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI
import requests
from starlette.exceptions import HTTPException

from model import CryptoAnalysisRequest, CryptoAnalysisResponse

load_dotenv()

app = FastAPI()

OPENROUTER_KEY=os.getenv("OPENROUTER_KEY")
OPENROUTER_URL=os.getenv("OPENROUTER_URL")
COINGECKO_URL=os.getenv("COINGECKO_URL")

app = FastAPI( title="Crypto Analysis AI TOOL")

def get_crypto_insights(coin_list:List[str]):

    params = {
        "ids" :",".join(coin_list),
        "vs_currency":"USD",
    }
    resp = requests.get(COINGECKO_URL,params=params)

    return resp.json()



SYSTEM_PROMPT = """
Your a  "CryptoAnalyst AI" - a professional market analyst.

You will be given recent market for data for several crypto currencies (price,market cap,volume,24h change).

Your job is  to produce a structured analysis with a valid JSON schema

CRITICAL INSTRUCTIONS
- You must output only valid JSON*,not inside quotes ,not inside markdowns, not as a string.
- Do not include  ``` json or ``` anywhere 
- Do not add explanations,greetings, text before or after the JSON 
- The JSON must begin directly with { and end with }

Rules:
- Return one analysis per coin 
- Follow the exact JSON Scheme
{
"analysis":[
    {
    "coin": "<coin name>",
    "summary": "<2-3 line summery>",
    "sentiment": "<"bullish" | "neutral" | "bearish">",
    "key_factors": [
        {"factor" :"<factor_name>", "impact": "<impact details>" 
        }]
    "insights":[
        {
        "prediction": "<short-term prediction>"","confidence": "<0-100>",
    }]
}
- provide 3 key factors and 3 insights per coin.
- Base your reasoning's on given metrics (e.g,price change %,market cap trends).
- Always output only JSON - no Markdown, no explanation.
 """

def call_openrouter_api(market_data):

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",

    }

    body = {
        "model": "meta-llama/llama-3.3-70b-instruct",
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"Here is the market data for -  {json.dumps(market_data, indent=2)}",
            }
        ]
    }
    resp = requests.post(OPENROUTER_URL, headers=headers, json=body)
    llm_response = resp.json()
    json_str = llm_response["choices"][0]["message"]["content"]
    print(json_str)

    try:
        payload = json.loads(json_str)
    except JSONDecodeError as e:
        raise HTTPException(status_code=502, detail="LLM Did not return a valid JSON")
    try:
        return CryptoAnalysisResponse.model_validate(payload)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM JSON validation failed: {str(e)}")



@app.post("/crypto/analysis")
async def analysis(request: CryptoAnalysisRequest):

    crypto_data = get_crypto_insights(request.coin)
    market_data = [{
        "name": data["name"],
        "symbol": data["symbol"],
        "current_price": data["current_price"],
        "market_cap": data["market_cap"],
        "total_volume": data["total_volume"],
        "price_change_percentage_24h": data["price_change_percentage_24h"],

    } for data in crypto_data] #get the only needed data from the response

    return call_openrouter_api(market_data)






# if __name__ == "__main__":
#     get_crypto_insights(["bitcoin"])

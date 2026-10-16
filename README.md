# Crypto Analysis Tool

An AI-powered cryptocurrency market analysis API built with **FastAPI, Python, CoinGecko, and OpenRouter**. The application retrieves cryptocurrency market data and uses a large language model (LLM) to generate structured market insights.

## Features

- **Cryptocurrency market data:** Retrieve current prices, market capitalization, trading volume, and 24-hour price changes.
- **AI-powered analysis:** Generate market summaries and sentiment classifications.
- **Key market factors:** Identify factors that may influence cryptocurrency prices.
- **Predictive insights:** Generate AI-based predictions with confidence scores.
- **REST API:** Access the analysis through a FastAPI endpoint.
- **Data validation:** Validate AI-generated responses using Pydantic models.
- **Environment configuration:** Keep API credentials outside the source code.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API framework |
| Pydantic | Request and response validation |
| CoinGecko API | Cryptocurrency market data |
| OpenRouter API | Access to LLMs |
| Requests | HTTP communication |
| python-dotenv | Environment variable management |

## Project Structure

```text
Crypto-Analysis-tool/
├── main.py
├── model.py
├── crypto.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

*Your actual filenames may differ. Keep the structure section consistent with your repository.*

## Prerequisites

- Python 3.11 or later, compatible with your dependencies
- Git
- An OpenRouter API key
- Internet access to reach the APIs

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/AkilaKasun/Crypto-Analysis-tool.git
cd Crypto-Analysis-tool
```

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you have not created `requirements.txt` yet, install the main dependencies:

```bash
pip install fastapi uvicorn requests python-dotenv pydantic
```

Then save them:

```bash
pip freeze > requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using the configuration in `.env.example`.

```dotenv
OPENROUTER_KEY=your_openrouter_api_key
OPENROUTER_URL=https://openrouter.ai/api/v1/chat/completions
COINGECKO_URL=https://api.coingecko.com/api/v3/coins/markets
```

Replace `your_openrouter_api_key` with your own API key from [OpenRouter](https://openrouter.ai/).

**Never commit your real `.env` file to GitHub.**

### 5. Start the application

If your FastAPI instance is defined in `main.py` as `app`, run:

```bash
uvicorn main:app --reload
```

The API will be available at:

- API base URL: `http://127.0.0.1:8000`
- Interactive Swagger documentation: `http://127.0.0.1:8000/docs`
- ReDoc documentation: `http://127.0.0.1:8000/redoc`

If your FastAPI instance is in another Python file, adjust `main:app` accordingly.

## API Usage

### Analyze cryptocurrencies

**Endpoint:** `POST /crypto/analysis`

**Request body:**

```json
{
  "coin": ["bitcoin"]
}
```

Use CoinGecko coin IDs, such as `bitcoin`, `ethereum`, or `solana`.

**Example using cURL:**

```bash
curl -X POST "http://127.0.0.1:8000/crypto/analysis" \
  -H "Content-Type: application/json" \
  -d "{\"coin\":[\"bitcoin\"]}"
```

**Example response structure:**

```json
{
  "analysis": [
    {
      "coin": "bitcoin",
      "summery": "An AI-generated market summary.",
      "sentiment": "neutral",
      "key_factors": [
        {
          "factor": "Trading volume",
          "impact": "May influence short-term price movements."
        }
      ],
      "insights": [
        {
          "prediction": "An AI-generated market outlook.",
          "confidence": 70
        }
      ]
    }
  ]
}
```

The response above is an illustrative example, not live market data. The actual response depends on the market data and model output. The current Pydantic schema requires `sentiment` to be `bullish`, `neutral`, or `bearish`, and `confidence` to be between 0 and 100.

## Environment Variables

| Variable | Description |
|---|---|
| `OPENROUTER_KEY` | Your OpenRouter API key |
| `OPENROUTER_URL` | OpenRouter chat completions endpoint |
| `COINGECKO_URL` | CoinGecko market data endpoint |

## Error Handling

The application can return errors when external API requests fail, the LLM response is invalid JSON, or the generated response does not satisfy the Pydantic schema. Check the terminal logs and API response details when troubleshooting.

## Important Disclaimer

This tool provides AI-generated cryptocurrency market analysis for educational and informational purposes only. Predictions and confidence scores are not guarantees of future market performance and should not be treated as financial advice.

Always conduct independent research before making investment decisions.

## Future Improvements

- Add support for additional market indicators.
- Improve error handling and request timeouts.
- Add automated tests.
- Implement API rate limiting and logging.
- Build a frontend dashboard for visualizing cryptocurrency trends.

## Author

**Akila Kasun**

GitHub: [@AkilaKasun](https://github.com/AkilaKasun)

---

Built with Python, FastAPI, CoinGecko, and OpenRouter.

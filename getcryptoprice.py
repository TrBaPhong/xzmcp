import requests
from fastmcp import FastMCP
import logging

logger = logging.getLogger(__name__)

API_KEY = "3dbcc3e084e04a4ea3db50c579b6eff8"
CMC_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

# Create an MCP server
mcp = FastMCP("crypto_price")

@mcp.tool()
def crypto_price(symbol: str, currency: str = "USD") -> dict:
    """
    Fetch current crypto price from CoinMarketCap API.

    Args:
        symbol: crypto symbol, e.g. 'BTC', 'ETH'
        currency: fiat currency, default 'USD'

    Returns:
        JSON with price and market data.
    """
    try:
        params = {
            "symbol": symbol.upper(),
            "convert": currency.upper()
        }

        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": API_KEY
        }

        logger.info(f"Requesting CMC: {params}")

        response = requests.get(CMC_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if "data" not in data or symbol.upper() not in data["data"]:
            return {"success": False, "error": "Invalid symbol or API error", "raw": data}

        quote = data["data"][symbol.upper()]["quote"][currency.upper()]
        info = data["data"][symbol.upper()]

        return {
            "success": True,
            "symbol": symbol.upper(),
            "name": info["name"],
            "price": quote["price"],
            "percent_change_1h": quote.get("percent_change_1h"),
            "percent_change_24h": quote.get("percent_change_24h"),
            "percent_change_7d": quote.get("percent_change_7d"),
            "market_cap": quote.get("market_cap"),
            "volume_24h": quote.get("volume_24h"),
        }

    except Exception as e:
        return {"success": False, "error": str(e)}

# Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")
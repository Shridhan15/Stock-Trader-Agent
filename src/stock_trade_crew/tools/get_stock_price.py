import yfinance as yf
import pandas as pd
from crewai.tools import tool


@tool("Stock Technical Analysis Tool")
def get_stock_analysis(stock_symbol: str) -> str:
    """
    Provides technical analysis for a stock:
    - Current price
    - SMA20 & SMA50
    - Trend (Bullish/Bearish/Sideways)
    - Volatility
    - Volume signal
    """
    stock = yf.Ticker(stock_symbol)

    # Fetch last 6 months of daily data
    hist = stock.history(period="6mo", interval="1d")

    if hist.empty:
        return f"No historical data available for {stock_symbol}"

    close = hist["Close"]
    volume = hist["Volume"]

    # Indicators
    sma20 = close.rolling(20).mean()
    sma50 = close.rolling(50).mean()

    current_price = float(close.iloc[-1])
    sma20_last = float(sma20.iloc[-1])
    sma50_last = float(sma50.iloc[-1])

    # Simple trend logic
    if current_price > sma20_last > sma50_last:
        trend = "Bullish"
    elif current_price < sma20_last < sma50_last:
        trend = "Bearish"
    else:
        trend = "Sideways"

    # Volatility (risk proxy)
    volatility = float(close.pct_change().std() * 100)

    # Volume change (last day vs avg 20)
    avg_vol_20 = float(volume.rolling(20).mean().iloc[-1])
    vol_today = float(volume.iloc[-1])
    vol_signal = "High" if vol_today > avg_vol_20 else "Normal"

    return (
        f"Stock: {stock_symbol}\n"
        f"Current Price: {current_price:.2f}\n"
        f"SMA20: {sma20_last:.2f}\n"
        f"SMA50: {sma50_last:.2f}\n"
        f"Trend: {trend}\n"
        f"Volatility (std %): {volatility:.2f}\n"
        f"Volume Signal: {vol_signal}"
    )
 
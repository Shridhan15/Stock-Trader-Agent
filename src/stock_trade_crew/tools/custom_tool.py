import yfinance as yf
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class StockAnalysisInput(BaseModel):
    stock_symbol: str = Field(..., description="Stock ticker symbol (e.g., AAPL)")

class StockTechnicalAnalysisTool(BaseTool):
    name: str = Field(default="Stock Technical Analysis Tool", description="Tool name")
    description: str = Field(
        default="Provides technical analysis for a stock: price, SMAs, trend, volatility, volume.",
        description="Tool description"
    )
    args_schema: Type[BaseModel] = StockAnalysisInput

    def _run(self, stock_symbol: str) -> str:
        try:
            ticker = yf.Ticker(stock_symbol)
            hist = ticker.history(period="6mo")
            if hist.empty:
                return f"No data for {stock_symbol}"

            close = hist['Close']
            vol = hist['Volume']
            
            current = float(close.iloc[-1])
            sma20 = float(close.rolling(20).mean().iloc[-1])
            sma50 = float(close.rolling(50).mean().iloc[-1])
            
            trend = "Bullish" if current > sma20 > sma50 else "Bearish" if current < sma20 < sma50 else "Sideways"
            volatility = float(close.pct_change().std() * 100)
            vol_signal = "High" if vol.iloc[-1] > vol.rolling(20).mean().iloc[-1] * 1.2 else "Normal"
            
            return f"""Stock Analysis for {stock_symbol}:
Current Price: ${current:.2f}
SMA20: ${sma20:.2f} | SMA50: ${sma50:.2f}
Trend: {trend}
Volatility: {volatility:.1f}%
Volume: {vol_signal}"""
        except Exception as e:
            return f"Error: {str(e)}"

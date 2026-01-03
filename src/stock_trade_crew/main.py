#!/usr/bin/env python
import sys
import warnings

from datetime import datetime 
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

from stock_trade_crew.crew import StockTradeCrew

def run():
    """
    Run the crew
    
    """
    inputs={"stock_symbol": "AAPL"}
    try:
        StockTradeCrew().crew().kickoff(inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occured while running the crew {e}")

if __name__ == "__main__":
    run()

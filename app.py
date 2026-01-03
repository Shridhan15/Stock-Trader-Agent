import streamlit as st
from src.stock_trade_crew.crew import StockTradeCrew
from pathlib import Path

st.set_page_config(
    page_title="AI Stock Trade Predictor",
    layout="centered"
)

st.title("📈 AI Stock Trade Predictor")
st.caption("CrewAI-powered stock analysis & decision system")

# ---- Input ----
stock_symbol = st.text_input(
    "Enter Stock Symbol",
    placeholder="AAPL"
)

run_btn = st.button("Analyze Stock")

if run_btn:
    if not stock_symbol:
        st.warning("Please enter a stock symbol")
    else:
        with st.spinner("Running AI agents (Analyst → Trader)..."):
            crew = StockTradeCrew()
            final_output = crew.crew().kickoff(
                inputs={"stock_symbol": stock_symbol.upper()}
            )

        st.success("Analysis completed")

        # ---- Trader Decision ----
        st.subheader("🧠 Trader Decision")
        st.markdown(final_output)

        # ---- Analyst Report ----
        report_path = Path("reports/report.md")

        if report_path.exists():
            with st.expander("📊 View Full Analyst Report"):
                st.markdown(report_path.read_text())
        else:
            st.info("No detailed report found.")

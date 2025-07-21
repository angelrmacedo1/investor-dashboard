
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# ----------------------
# PAGE CONFIG
# ----------------------
st.set_page_config(page_title="Investor Insights - By Angel Macedo", layout="wide")

# ----------------------
# TITLE
# ----------------------
st.title("Investor Insights Dashboard")
st.markdown("Crafted by **Angel Macedo** — Get a fast, visual breakdown of any stock's valuation and performance. Perfect for retail investors, students, or aspiring analysts.")

# ----------------------
# USER INPUT
# ----------------------
ticker_input = st.text_input("Enter a stock ticker (e.g. AAPL, TSLA, MSFT)", "AAPL").upper()

# ----------------------
# FETCH DATA
# ----------------------
@st.cache_data
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="6mo")
    info = stock.info
    return stock, hist, info

# ----------------------
# MAIN DISPLAY
# ----------------------
if ticker_input:
    stock, hist, info = get_stock_data(ticker_input)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"{ticker_input} Price Trend")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist.index, y=hist["Close"], name="Close Price", line=dict(color="royalblue")))
        fig.update_layout(title=f"{ticker_input} - 6 Month Closing Price", xaxis_title="Date", yaxis_title="Price (USD)", margin=dict(l=10, r=10, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Key Financial Metrics")
        st.markdown(f"- **Market Cap:** ${info.get('marketCap', 'N/A'):,}")
        st.markdown(f"- **P/E Ratio:** {info.get('trailingPE', 'N/A')} *(Price-to-Earnings)*")
        st.markdown(f"- **EPS:** {info.get('trailingEps', 'N/A')} *(Earnings per Share)*")
        st.markdown(f"- **Dividend Yield:** {info.get('dividendYield', 'N/A')} *(Yield %)*")
        st.markdown(f"- **52 Week High:** ${info.get('fiftyTwoWeekHigh', 'N/A')}")
        st.markdown(f"- **52 Week Low:** ${info.get('fiftyTwoWeekLow', 'N/A')}")

    st.subheader("Risk Metrics")
    hist['Returns'] = hist['Close'].pct_change()
    volatility = np.std(hist['Returns']) * np.sqrt(252)
    sharpe_ratio = np.mean(hist['Returns']) / np.std(hist['Returns']) * np.sqrt(252)

    st.markdown(f"- **Volatility (Annualized):** {volatility:.2%} *(Price variation over time)*")
    st.markdown(f"- **Sharpe Ratio:** {sharpe_ratio:.2f} *(Risk-adjusted return)*")

    if ticker_input == "AAPL":
        st.info("Apple Inc. (AAPL) is known for its consistent performance, high market cap, and strong brand moat—great as a benchmark stock.")

    # Footer
    st.markdown("---")
    st.markdown("Created by Angel Macedo using Streamlit + Yahoo Finance | For educational and professional demo use")

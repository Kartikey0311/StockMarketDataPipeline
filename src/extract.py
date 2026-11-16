
import yfinance as yf

from config import TICKERS, PERIOD, INTERVAL


def extract_stock_data(ticker):

    print(f"Extracting data for {ticker}...")

    data = yf.download(
        ticker,
        period=PERIOD,
        interval=INTERVAL,
        auto_adjust=False,
        progress=False
    )

    return data

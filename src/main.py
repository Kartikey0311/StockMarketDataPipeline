
from extract import extract_stock_data
from config import TICKERS
from validate import validate_stock_data
from transform import transform_stock_data
import pandas as pd
import os

output_path = "data/processed/all_stocks.parquet"

# 1. Load existing data
if os.path.exists(output_path):
    existing_data = pd.read_parquet(output_path)

    if not existing_data.empty:
        latest_datas = existing_data.groupby("Ticker")["Date"].max()
    else:
        latest_datas = None

    print("Existing data loaded")
else:
    existing_data = pd.DataFrame()
    latest_datas = None
    print("No existing data found. Starting fresh.")

# 2. Extract, validate and transform
all_stocks = []

for ticker in TICKERS:
    data = extract_stock_data(ticker)

    filepath = f"data/raw/{ticker}.parquet"
    data.to_parquet(filepath)

    is_valid = validate_stock_data(data, ticker)

    if is_valid:
        print(f"{ticker}: Validation successful")

        transformed_data = transform_stock_data(data, ticker)

        # 3. Incremental filtering
        if latest_datas is not None and ticker in latest_datas.index:
            latest_date = latest_datas[ticker]

            filtered_data = transformed_data[
                transformed_data["Date"] > latest_date
            ]
        else:
            # First run or ticker not previously stored
            filtered_data = transformed_data

        all_stocks.append(filtered_data)

    else:
        print(f"{ticker}: Validation Failed")

print(f"\nNew records for {ticker}:")
print(filtered_data.head())
print("New records count:", len(filtered_data))

# 4. Combine new records
if all_stocks:
    new_records = pd.concat(all_stocks, axis=0, ignore_index=True)

    # 5. Combine old and new data
    updated_data = pd.concat(
        [existing_data, new_records],
        axis=0,
        ignore_index=True
    )

    # 6. Remove duplicates using Ticker + Date
    updated_data = updated_data.drop_duplicates(
        subset=["Ticker", "Date"],
        keep="last"
    )

    # 7. Save updated dataset
    updated_data.to_parquet(output_path, index=False)

    print("Pipeline completed successfully!")
    print(updated_data.groupby("Ticker").size())
else:
    print("No new records to process.")

print("\nFinal combined stock data:")
print(updated_data.groupby('Ticker').head(2))

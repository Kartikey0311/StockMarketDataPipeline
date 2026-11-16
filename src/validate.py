def validate_stock_data(data , ticker):
    validation_passed = True
    print(f"Validating {ticker}")
    duplicate_count = data.duplicated().sum()

    if duplicate_count > 0:
        validation_passed = False
        print("Duplicate rows:", duplicate_count)
        
    else:
        print("No duplicate rows found")

    # 2. Check for zero or negative closing prices
    close_prices = data["Close"][ticker]

    invalid_closing_prices = close_prices[close_prices <= 0]

    if invalid_closing_prices.count() > 0:
        validation_passed = False
        print("Invalid closing prices:")
        print(invalid_closing_prices)
        
    else:
        print("No zero or negative closing prices found")

    # 3. Find earliest and latest dates
    earliest_date = data.index.min()
    latest_date = data.index.max()

    print("Earliest date:", earliest_date)
    print("Latest date:", latest_date)

    #4.
    high_prices = data["High"][ticker]
    low_prices = data["Low"][ticker]

    invalid_high_low_prices = high_prices[high_prices < low_prices]
    if invalid_high_low_prices.count() > 0 :
        validation_passed = False
        print("invalid as high price cannot be low than low prices")
        print(invalid_high_low_prices)
    else:
        print("no invalid pricing")

    #5.
    volume = data["Volume"][ticker]
    invalid_volume = volume[volume < 0]

    if invalid_volume.count() > 0:
        validation_passed = False
        print('invalid volume record: ')
        print(invalid_volume)
    else:
        print('no negative volume found')

    return validation_passed
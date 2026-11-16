def transform_stock_data(data , ticker):
    copy_data = data.copy()
    data_reset = copy_data.reset_index()
    data_reset.columns = data_reset.columns.droplevel(1)
    # print(data_reset.head(5))
    print(data_reset.columns)
    data_reset["Ticker"] = ticker  
    return data_reset

import pandas as pd
maang_path = "C:/Users/Felice/Documents/projects/Capstone/Combined MAANG.csv"
market_path = "C:/Users/Felice/Documents/projects/Capstone/US Stock Market Data.csv"
df_maang = pd.read_csv(maang_path)
df_market = pd.read_csv(market_path)
print("Datasets loaded successfully!")
df_maang['Date'] = pd.to_datetime(df_maang['Date'])
df_market['Date'] = pd.to_datetime(df_market['Date'])
df_maang.dropna(inplace=True)
df_market.fillna(method='ffill', inplace=True)
print("Data cleaning completed!")

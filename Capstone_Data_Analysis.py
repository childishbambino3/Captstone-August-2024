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
df_maang = df_maang[(df_maang['Date'] >= '2020-01-01') & (df_maang['Date'] <= '2022-12-31')]
df_market = df_market[(df_market['Date'] >= '2020-01-01') & (df_market['Date'] <= '2022-12-31')]
print("Data filtered for 2020-2022!")
df_combined = pd.merge(df_maang, df_market, on='Date', how='inner')
print("Datasets merged successfully!")
correlation_matrix = df_combined.corr()
print("Stock Trend Summary:")
print(df_combined.describe())
print("Correlation matrix computed!")

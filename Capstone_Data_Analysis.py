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
import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(12,6))
plt.plot(df_combined['Date'], df_combined['Close'], label='Stock Close Price')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Stock Price Trends (2020-2022)')
plt.legend()
plt.show()

plt.figure(figsize=(10,8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Stock vs Market Factor Correlation')
plt.show()
pivot_table = df_combined.pivot_table(values='Close', index='Date', aggfunc='mean')
print("Pivot table created successfully!")
print(pivot_table.head())

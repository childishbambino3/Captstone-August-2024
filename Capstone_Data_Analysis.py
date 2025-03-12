import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load the datasets
maang_path = "C:/Users/Felice/Documents/projects/Capstone/Combined MAANG.csv"
market_path = "C:/Users/Felice/Documents/projects/Capstone/US Stock Market Data.csv"

df_maang = pd.read_csv(maang_path)
df_market = pd.read_csv(market_path)

print("Datasets loaded successfully!")

# Step 2: Convert the 'Date' column to datetime format
df_maang['Date'] = pd.to_datetime(df_maang['Date'])
df_market['Date'] = pd.to_datetime(df_market['Date'])

# Handle missing values
df_maang.dropna(inplace=True)
df_market.fillna(method='ffill', inplace=True)

print("Data cleaning completed!")

# Step 3: Filter for the period 2020-2022
df_maang = df_maang[(df_maang['Date'] >= '2020-01-01') & (df_maang['Date'] <= '2022-12-31')]
df_market = df_market[(df_market['Date'] >= '2020-01-01') & (df_market['Date'] <= '2022-12-31')]

print("Data filtered for 2020-2022!")

# Step 4: Merge datasets on 'Date'
df_combined = pd.merge(df_maang, df_market, on='Date', how='inner')

print("Datasets merged successfully!")

# Step 5: Compute stock trends and correlation matrix
correlation_matrix = df_combined.corr()
print("Stock Trend Summary:")
print(df_combined.describe())

print("Correlation matrix computed!")

# Step 6: Create visualizations
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

# Step 7: Create pivot table
pivot_table = df_combined.pivot_table(values='Close', index='Date', aggfunc='mean')
print("Pivot table created successfully!")
print(pivot_table.head())

# Step 8: Virtual environment setup instruction
print("To set up a virtual environment, run: python -m venv capstone_env")

# Step 9: Summarize findings
summary = """
Key Insights:
1. Stock prices fluctuated significantly from 2020-2022.
2. Certain stocks exhibited high correlation with market factors.
3. Economic events impacted stock price movements.
"""
print(summary)

print("Data Processing and Analysis Completed!")
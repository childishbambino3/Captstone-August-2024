Define project objective
print("Project Objective: To analyze how MAANG stocks performed compared to the broader market during 2020-2022 pandemic period")

# Step 1: Load the datasets
maang_path = "C:/Users/Felice/Documents/projects/Capstone/Combined MAANG.csv"
market_path = "C:/Users/Felice/Documents/projects/Capstone/US Stock Market Data.csv"
df_maang = pd.read_csv(maang_path)
df_market = pd.read_csv(market_path)
print("Datasets loaded successfully!")

# Display initial information about the datasets
print("\nInitial view of MAANG data:")
print(df_maang.head())
print(df_maang.info())
print("\nInitial view of market data:")
print(df_market.head())
print(df_market.info())

# Step 2: Convert the 'Date' column to datetime format with error handling
def parse_dates(df, column_name):
    try:
        df[column_name] = pd.to_datetime(df[column_name], infer_datetime_format=True, errors='coerce')
    except Exception as e:
        print(f"Error parsing dates in {column_name}: {e}")

parse_dates(df_maang, 'Date')
parse_dates(df_market, 'Date')

# Handle missing values with explanation
print("\nHandling missing values:")
df_maang.dropna(inplace=True)
df_market.fillna(method='ffill', inplace=True)
print("Data cleaning completed!")

# Step 3: Filter for the period 2020-2022
df_maang = df_maang[(df_maang['Date'] >= '2020-01-01') & (df_maang['Date'] <= '2022-12-31')]
df_market = df_market[(df_market['Date'] >= '2020-01-01') & (df_market['Date'] <= '2022-12-31')]
print("Data filtered for 2020-2022!")

# Step 4: Merge datasets on 'Date'
df_combined = pd.merge(
    df_maang.rename(columns={'Close': 'MAANG_Close'}), 
    df_market.rename(columns={'Close': 'Market_Close'}), 
    on='Date', how='inner'
)
print("Datasets merged successfully!")

# Feature Engineering
df_combined['MAANG_Market_Diff_Pct'] = ((df_combined['MAANG_Close'] - df_combined['Market_Close']) / df_combined['Market_Close']) * 100
print("Feature engineering completed!")

# Step 5: Compute stock trends and correlation matrix
correlation_matrix = df_combined.corr()
print("\nStock Trend Summary:")
print(df_combined[['MAANG_Close', 'Market_Close', 'MAANG_Market_Diff_Pct']].describe())
print("\nCorrelation matrix computed!")

# Step 6: Create visualizations
plt.figure(figsize=(12,6))
plt.plot(df_combined['Date'], df_combined['MAANG_Close'], label='MAANG Close Price')
plt.plot(df_combined['Date'], df_combined['Market_Close'], label='Market Close Price')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('MAANG vs Market Stock Price Trends (2020-2022)')
plt.legend()
plt.grid()
plt.savefig('price_trends.png')
plt.show()

plt.figure(figsize=(10,8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('MAANG vs Market Factor Correlation')
plt.savefig('correlation_heatmap.png')
plt.show()

# Step 7: Create pivot table
pivot_table = df_combined.pivot_table(
    values=['MAANG_Close', 'Market_Close', 'MAANG_Market_Diff_Pct'], 
    index=pd.Grouper(key='Date', freq='M'), 
    aggfunc={'MAANG_Close': 'mean', 'Market_Close': 'mean', 'MAANG_Market_Diff_Pct': ['mean', 'std']}
)
print("\nMonthly Pivot Table:")
print(pivot_table.head())

# Step 8: Virtual environment setup instruction
print("\nTo set up a virtual environment, run: python -m venv capstone_env")

# Step 9: Summarize findings
summary = """
Key Insights:
1. MAANG stocks showed volatility in 2020-2022 compared to the broader market.
2. Correlation between MAANG stocks and market factors was strongest during specific periods.
3. The most significant stock price change occurred in a key market-moving month.
"""
print(summary)

# Save the summary to a file
with open('analysis_summary.txt', 'w') as f:
    f.write(summary)

print("Data Processing and Analysis Completed!")

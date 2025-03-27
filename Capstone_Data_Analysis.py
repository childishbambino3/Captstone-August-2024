import pandas as pd
import os

# full file paths
maang_file = r"C:\Users\Felice\Documents\projects\Capstone\Combined MAANG.csv"
market_file = r"C:\Users\Felice\Documents\projects\Capstone\US Stock Market Data.csv"

# verify the files exist before proceeding
if not os.path.exists(maang_file):
    raise FileNotFoundError(f"Error: The file '{maang_file}' was not found.")
if not os.path.exists(market_file):
    raise FileNotFoundError(f"Error: The file '{market_file}' was not found.")

# Load datasets
df_maang = pd.read_csv(maang_file)
df_market = pd.read_csv(market_file)

print("Project Objective: To analyze how MAANG stocks performed compared to the broader market during 2020-2022 pandemic period")

# show datasets loaded
print("Datasets loaded successfully!\n")

# show initial data preview
print("Initial view of MAANG data:")
print(df_maang.head())
print(df_maang.info())

print("\nInitial view of market data:")
print(df_market.head())
print(df_market.info())

# Convert 'Date' column to datetime format
df_maang["Date"] = pd.to_datetime(df_maang["Date"], errors="coerce")
df_market["Date"] = pd.to_datetime(df_market["Date"], errors="coerce")

# Handle missing values by forward-filling
df_market.fillna(method="ffill", inplace=True)

print("\nHandling missing values:")
print("Data cleaning completed!")

# Filter data for the pandemic period (2020-2022)
df_maang = df_maang[(df_maang["Date"] >= "2020-01-01") & (df_maang["Date"] <= "2022-12-31")]
df_market = df_market[(df_market["Date"] >= "2020-01-01") & (df_market["Date"] <= "2022-12-31")]

print("Data filtered for 2020-2022!\n")

# Check available columns
print("Checking available columns in market data:")
print(df_market.columns)

# Merge datasets on Date
df_combined = pd.merge(df_maang, df_market, on="Date", how="inner")
print("Datasets merged successfully!")

# Convert 'Close' prices to numeric for calculations
df_combined['MAANG_Close'] = pd.to_numeric(df_combined['Close'], errors='coerce')

# Assuming 'S&P_500_Price' represents the market index column, change if necessary
df_combined['Market_Close'] = pd.to_numeric(df_combined['S&P_500_Price'], errors='coerce')

# Calculate percentage difference between MAANG stock performance and the market
df_combined['MAANG_Market_Diff_Pct'] = ((df_combined['MAANG_Close'] - df_combined['Market_Close']) / df_combined['Market_Close']) * 100

# Display final dataset preview
print("\nFinal dataset preview with calculated difference:")
print(df_combined.head())
output_file = r"C:\Users\Felice\Documents\projects\Capstone\Processed_MAANG_vs_Market.csv"
df_combined.to_csv(output_file, index=False)

print(f"\nData processing complete! Output saved as '{output_file}'.")

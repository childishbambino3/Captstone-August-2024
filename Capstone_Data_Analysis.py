import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go

def load_data():
    """
    Load MAANG and US Stock Market datasets with robust error handling
    """
    try:
        # Read CSV files with additional error handling
        df_maang = pd.read_csv("Combined MAANG.csv", thousands=',', decimal='.')
        df_market = pd.read_csv("US Stock Market Data.csv", thousands=',', decimal='.')
        
        print("Datasets loaded successfully!")
        return df_maang, df_market
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return None, None

def clean_and_merge_data(df_maang, df_market):
    """
    Clean datasets and merge them with robust date handling
    """
    required_maang_cols = ["Date", "Close"]
    required_market_cols = ["Date", "S&P_500_Price"]

    # Ensure required columns exist
    for col in required_maang_cols:
        if col not in df_maang.columns:
            raise ValueError(f"Missing required column {col} in MAANG dataset")
    
    for col in required_market_cols:
        if col not in df_market.columns:
            raise ValueError(f"Missing required column {col} in Market dataset")
    
    # Forward fill missing values
    df_maang = df_maang.ffill()
    df_market = df_market.ffill()
    
    # Convert Date columns to datetime (Removed deprecated infer_datetime_format)
    df_maang["Date"] = pd.to_datetime(df_maang["Date"], errors='coerce')
    df_market["Date"] = pd.to_datetime(df_market["Date"], errors='coerce')

    # Remove rows with NaT (invalid dates)
    df_maang = df_maang.dropna(subset=["Date"])
    df_market = df_market.dropna(subset=["Date"])

    # Convert numeric columns
    df_maang["Close"] = pd.to_numeric(df_maang["Close"], errors='coerce')
    df_market["S&P_500_Price"] = pd.to_numeric(df_market["S&P_500_Price"], errors='coerce')

    # Drop rows with NaN in numeric columns
    df_maang = df_maang.dropna(subset=["Close"])
    df_market = df_market.dropna(subset=["S&P_500_Price"])

    # Filter data for 2020-2022
    df_maang = df_maang[(df_maang["Date"] >= "2020-01-01") & (df_maang["Date"] <= "2022-12-31")]
    df_market = df_market[(df_market["Date"] >= "2020-01-01") & (df_market["Date"] <= "2022-12-31")]

    # Merge datasets on Date
    df_merged = pd.merge(df_maang, df_market, on="Date", how="inner")

    # Calculate percentage difference
    df_merged["MAANG_Market_Diff_Pct"] = ((df_merged["Close"] - df_merged["S&P_500_Price"]) / df_merged["S&P_500_Price"]) * 100
    
    return df_merged

def create_matplotlib_visualizations(df_merged):
    """
    Create matplotlib visualizations
    """
    try:
        # Plotting MAANG Stock Price vs S&P 500
        plt.figure(figsize=(12, 6))
        plt.plot(df_merged["Date"], df_merged["Close"], label="MAANG Stock")
        plt.plot(df_merged["Date"], df_merged["S&P_500_Price"], label="S&P 500")
        plt.title("MAANG Stock Price vs S&P 500 (2020-2022)")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("stock_price_comparison.png")
        plt.close()

        # Plotting Percentage Difference
        plt.figure(figsize=(12, 6))
        plt.plot(df_merged["Date"], df_merged["MAANG_Market_Diff_Pct"])
        plt.title("MAANG vs S&P 500 Percentage Difference (2020-2022)")
        plt.xlabel("Date")
        plt.ylabel("Percentage Difference")
        plt.axhline(y=0, color='r', linestyle='--')
        plt.tight_layout()
        plt.savefig("percentage_difference.png")
        plt.close()

    except Exception as e:
        print(f"Error creating matplotlib visualizations: {e}")

def create_plotly_dashboard(df_merged):
    """
    Create interactive Plotly dashboard
    """
    try:
        # Interactive line chart
        fig = px.line(df_merged, x="Date", y=["Close", "S&P_500_Price"], 
                      title="MAANG Stock vs S&P 500 Interactive Chart")
        fig.write_html("interactive_stock_chart.html")

        # Percentage difference area chart
        fig_diff = px.area(df_merged, x="Date", y="MAANG_Market_Diff_Pct", 
                           title="MAANG vs S&P 500 Percentage Difference")
        fig_diff.write_html("percentage_difference_chart.html")

    except Exception as e:
        print(f"Error creating Plotly dashboard: {e}")

def create_pivot_table(df_merged):
    """
    Create and save pivot table
    """
    try:
        pivot_monthly = df_merged.groupby(pd.Grouper(key="Date", freq="ME")).agg({
            "Close": "mean",
            "S&P_500_Price": "mean",
            "MAANG_Market_Diff_Pct": "mean"
        }).reset_index()
        
        pivot_monthly.to_csv("monthly_stock_comparison.csv", index=False)
        print("Pivot table created successfully!")

    except Exception as e:
        print(f"Error creating pivot table: {e}")

def main():
    """
    Main function to orchestrate data processing and visualization
    """
    df_maang, df_market = load_data()
    
    if df_maang is not None and df_market is not None:
        try:
            df_merged = clean_and_merge_data(df_maang, df_market)
            
            # Save processed data
            df_merged.to_csv("Processed_MAANG_vs_Market.csv", index=False)
            
            # Create visualizations
            create_matplotlib_visualizations(df_merged)
            create_plotly_dashboard(df_merged)
            
            # Create pivot table
            create_pivot_table(df_merged)
            
            print("Data processing completed successfully!")
        
        except Exception as e:
            print(f"An error occurred during data processing: {e}")

if __name__ == "__main__":
    main()

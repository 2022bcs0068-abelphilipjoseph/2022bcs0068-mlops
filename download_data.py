import pandas as pd
import os

def download_data():
    base_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/"
    red_wine_url = base_url + "winequality-red.csv"
    white_wine_url = base_url + "winequality-white.csv"

    print("Downloading red wine data...")
    red_df = pd.read_csv(red_wine_url, sep=';')
    
    print("Downloading white wine data...")
    white_df = pd.read_csv(white_wine_url, sep=';')

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    # Version 1: Just Red Wine
    print("Saving Version 1 (Red Wine only)...")
    red_df.to_csv("data/winequality.csv", index=False)
    
    # Store white wine separately for later use in v2
    white_df.to_csv("data/winequality-white-temp.csv", index=False)
    
    print("Data download and initial versioning setup complete.")

if __name__ == "__main__":
    download_data()

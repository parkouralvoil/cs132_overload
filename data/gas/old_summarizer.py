import pandas as pd
import glob
import os
import re

# python -m old_summarizer

def make_summary_table_csv(input_directory: str, output_csv_path: str):
    # Group rows into products (7 rows per product based on your example)
    products = [
        'Gasoline (RON97/100)',
        'Gasoline (RON95)',
        'Gasoline (RON91)',
        'Diesel',
        'Diesel Plus',
        'Kerosene'
    ]
    
    for filename in glob.glob(os.path.join(input_directory, "petro_ncr_*.csv")):
        output_filename = filename.removeprefix("doe_csvs\\old_format\\2023\\")
        output_path = os.path.join(f"doe_csvs\\{YEAR}", output_filename)
        df = pd.read_csv(filename) # Read the CSV file

        # Clean the data - replace '#N/A' with NaN
        df = df.replace('#N/A', pd.NA)
        df = df.replace('#VALUE!', pd.NA)
        df = df[df['City'] != 'Cities'].reset_index()

        # Calculate statistics for each product group
        results = []
        rows_per_city = 7  # Each product has 7 rows in the original data
        cities = df['City'].nunique()

        for p, product in enumerate(products):
            min_prices = []
            max_prices = []
            common_prices = []
            for c in range(cities):
                idx: int = p + (c * rows_per_city)
                if not idx in df.index:
                    print(idx, filename)
                    pd.set_option('display.max_rows', len(df))
                    print(df)
                    pd.reset_option('display.max_rows')
                    exit()
                min_price = df.at[idx, 'Min Price'] if not pd.isna(df.at[idx, 'Min Price']) else 999
                max_price = df.at[idx, 'Max Price'] if not pd.isna(df.at[idx, 'Max Price']) else -999
                common_price = df.at[idx, 'Common Price']
                if product == "Gasoline (RON97/100)":
                    next_idx: int = idx + 1
                    min_price = min_price if pd.isna(df.at[next_idx, 'Min Price']) else min(min_price, df.at[next_idx, 'Min Price'])
                    max_price = max_price if pd.isna(df.at[next_idx, 'Max Price']) else max(max_price, df.at[next_idx, 'Max Price'])
                    common_price = common_price if pd.isna(df.at[next_idx, 'Common Price']) else df.at[next_idx, 'Common Price']
                
                if min_price != 999: min_prices.append(min_price)
                if max_price != -999: max_prices.append(max_price)
                if not pd.isna(common_price): common_prices.append(common_price)

            results.append({
                'Product': product,
                'Overall Range Min': min(min_prices) if len(min_prices) > 0 else "#N/A",
                'Overall Range Max': min(max_prices) if len(max_prices) > 0 else "#N/A",
                'Common Price': round(sum(common_prices)/len(common_prices), 2) if len(common_prices) > 0 else "#N/A",
            })

        # Create the summary dataframe
        summary_df = pd.DataFrame(results)
        # Save to new CSV or print
        if os.path.exists(output_path):
            print(f"SKIP: already exists for {filename}")
            continue
        print(f"saved to {output_path}")
        summary_df.to_csv(output_path, index=False)

YEAR: str = "2023"

if __name__ == "__main__":
    dirs = "doe_csvs\\old_format"  # Replace with the actual directory containing your CSV files
    for dir in os.listdir(dirs):
        if dir != YEAR:
            continue
        year_folder = os.path.join(dirs, dir)
        output_filename = f"petro_ncr_{dir}.csv"
        make_summary_table_csv(year_folder, output_filename)
import pandas as pd
import glob
import os

# python -m compiler_all

# Define the desired product order
PRODUCT_ORDER = {
    'Gasoline (RON97/100)': 0,
    'Gasoline (RON95)': 1,
    'Gasoline (RON91)': 2,
    'Diesel': 3,
    'Diesel Plus': 4,
    'Kerosene': 5
}

if __name__ == "__main__":
    folder_path = 'compiled_csvs'
    file_pattern = os.path.join(folder_path, '*.csv')
    csv_files = glob.glob(file_pattern)
    all_data = []

    for file in csv_files:
        if file == "compiled_all.csv":
            continue
        df = pd.read_csv(file)
        all_data.append(df)

    combined_df = pd.concat(all_data, ignore_index=True)

    # Add a temporary 'product_rank' column for sorting
    combined_df['product_rank'] = combined_df['Product'].map(PRODUCT_ORDER)

    # Sort by date (descending) and product_rank (ascending)
    combined_df = combined_df.sort_values(
        by=['Date', 'product_rank'],
        ascending=[False, True]
    ).drop(columns=['product_rank'])  # Remove the temporary column

    # Save the sorted result
    combined_df.to_csv('compiled_csvs\\compiled_all.csv', index=False)

    print(f"Successfully combined all CSV files from '{folder_path}' into 'compiled_all.csv'")
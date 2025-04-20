import pandas as pd
import glob
import os

if __name__ == "__main__":
    folder_path = 'compiled_csvs'
    file_pattern = os.path.join(folder_path, '*.csv')
    csv_files = glob.glob(file_pattern)
    csv_files.reverse()
    all_data = []

    for file in csv_files:
        df = pd.read_csv(file)
        all_data.append(df)

    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df.to_csv('compiled_csvs\\compiled_all.csv', index=False)

    print(f"Successfully combined all CSV files from '{folder_path}' into 'compiled_all.csv'")
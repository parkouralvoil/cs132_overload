import pandas as pd
import glob
import os
import re

# python -m compiler_by_year

PRODUCT_ORDER = {
    'Gasoline (RON97/100)': 0,
    'Gasoline (RON95)': 1,
    'Gasoline (RON91)': 2,
    'Diesel': 3,
    'Diesel Plus': 4,
    'Kerosene': 5
}

def compile_csvs(directory: str, output_filename: str):
    """
    Compiles multiple CSV files into a single CSV with added Year, StartDate, and EndDate columns.

    Args:
        directory (str): The directory containing the CSV files.
        output_filename (str): The name of the output CSV file.
    """
    print(directory)
    all_data = []
    for filename in glob.glob(os.path.join(directory, "petro_ncr*.csv")):
        match = get_match(filename)
        if match:
            date_str = match.group(1)

            date_str = date_str.replace("_", "-")
            try:
                date_obj = pd.to_datetime(date_str)
                year = date_obj.year
                start_date = date_obj.strftime("%Y-%m-%d")

                df = pd.read_csv(filename)
                df["Year"] = year
                df["Date"] = start_date

                all_data.append(df)
            except ValueError:
                print(date_str)
                print(f"Error parsing date from filename: {filename}")
        else:
            print(f"Filename does not match expected pattern: {filename}")

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df = combined_df[["Year", "Date", "Product", "Overall Range Min", "Overall Range Max", "Common Price"]]

        # Add a temporary 'product_rank' column for sorting
        combined_df['product_rank'] = combined_df['Product'].map(PRODUCT_ORDER)

        # Sort by date (descending) and product_rank (ascending)
        combined_df = combined_df.sort_values(
            by=['Date', 'product_rank'],
            ascending=[False, True]
        ).drop(columns=['product_rank'])  # Remove the temporary column

        combined_df.to_csv(output_filename, index=False, mode='w')
        print(f"Successfully compiled CSVs into {output_filename}")
    else:
        print("No matching CSV files found.")

def get_match(filename: str):
    # New pattern for petro_ncr-YYYY-mon-DD.csv
    match = re.search(r"petro_ncr-(\d{4}-[a-zA-Z]{3}-\d{1,2})\.csv", filename)
    if not match:
        # 1. Pattern for petro_ncr_YYYY_month_DD_digit.csv (full month name)
        match = re.search(r"petro_ncr_(\d{4}-[a-zA-Z]+-\d{1,2})(_\d+)?\.csv", filename)
    if not match:
        # 2. Pattern for petro_ncr_YYYY_month_DD.csv (full month name)
        match = re.search(r"petro_ncr_(\d{4}-[a-zA-Z]+-\d{1,2})\.csv", filename)
    if not match:
        # 3. Original patterns (unchanged, fallback)
        match = re.search(r"petro_ncr_(\d{4}_\w+_\d{1,2})_(\d+)\.csv", filename)
    if not match:
        match = re.search(r"petro_ncr_(\d{4}_\w+_\d{1,2})\.csv", filename)
    if not match:
        match = re.search(r"petro_ncr_(\d{4}-\w{3}-\d{1,2})_(\d+)\.csv", filename)
    if not match:
        match = re.search(r"petro_ncr_(\d{4}-\w{3}-\d{1,2})\.csv", filename)
    if not match:
        match = re.search(r"petro_ncr_(\d{4}_\w{3}_\d{1,2})\.csv", filename)
    if not match:
        match = re.search(r"petro_ncr_(\d{4}-\d{2}-\d{2})\.csv", filename)
    if not match:
        match = re.search(r"petro_ncr_(\d{4}[_-]\w{3}-\d{1,2})(-.+)?\.csv", filename)
    if not match:
        match = re.search(r"petro_ncr_(\d{4}-\w{3}-\d{1,2})(_\d+)?\.csv", filename)
    if not match:
        match = re.search(r"petro_ncr_(\d{4}_\w{3}-\d{1,2})(_\d+)?\.csv", filename)
    return match


if __name__ == "__main__":
    dirs = "doe_csvs"  # Replace with the actual directory containing your CSV files
    for dir in os.listdir(dirs):
        if dir != "2021":
            continue
        year_folder = os.path.join(dirs, dir)
        output_filename = f"compiled_csvs\\compiled_petrol_data_{dir}.csv"
        compile_csvs(year_folder, output_filename)
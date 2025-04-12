import pandas as pd
import glob
import os
import re

def compile_csvs(directory: str, output_filename: str):
    """
    Compiles multiple CSV files into a single CSV with added Year, StartDate, and EndDate columns.

    Args:
        directory (str): The directory containing the CSV files.
        output_filename (str): The name of the output CSV file.
    """
    print(directory)
    all_data = []
    for filename in glob.glob(os.path.join(directory, "petro_ncr_*.csv")):
        match = get_match(filename)
        if match:
            date_str = match.group(1)
            end_date = match.group(2)

            date_str = date_str.replace("_", "-")
            try:
                date_obj = pd.to_datetime(date_str)
                year = date_obj.year
                start_date = date_obj.strftime("%Y-%m-%d")
                end_date_obj: pd.Timestamp = date_obj + pd.Timedelta(days=6)
                end_date = end_date_obj.strftime("%Y-%m-%d") # Assuming the date is the same for start and end for simplicity

                df = pd.read_csv(filename)
                df["Year"] = year
                df["StartDate"] = start_date
                df["EndDate"] = end_date

                all_data.append(df)
            except ValueError:
                print(date_str)
                print(f"Error parsing date from filename: {filename}")
        else:
            print(f"Filename does not match expected pattern: {filename}")

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df = combined_df[["Year", "StartDate", "EndDate", "Product", "Overall Range Min", "Overall Range Max", "Common Price"]]
        combined_df.to_csv(output_filename, index=False)
        print(f"Successfully compiled CSVs into {output_filename}")
    else:
        print("No matching CSV files found.")

def get_match(filename: str):
    match = re.search(r"petro_ncr_(\d{4}-\w{3}-\d{1,2})-(\d{1,2})(_\d+)?\.csv", filename)
    if not match:
        match = re.search(r"petro_ncr_(\d{4}-\w{3}-\d{1,2})-(\w{3}-\d{1,2})(_\d+)?\.csv", filename)
    if not match:
        match = re.search(r"petro_ncr_(\d{4}-\w{3}-\d{1,2})(_\d+)?\.csv", filename)
    
    if not match:
        match = re.search(r"petro_ncr_(\d{4}_\w{3}-\d{1,2})-(\d{1,2})(_\d+)?\.csv", filename)
    if not match:
        match = re.search(r"petro_ncr_(\d{4}_\w{3}-\d{1,2})-(\w{3}-\d{1,2})(_\d+)?\.csv", filename)
    if not match:
        match = re.search(r"petro_ncr_(\d{4}_\w{3}-\d{1,2})(_\d+)?\.csv", filename)


    return match


if __name__ == "__main__":
    dirs = "doe_csvs"  # Replace with the actual directory containing your CSV files
    for dir in os.listdir(dirs):
        if dir != "2023":
            continue
        year_folder = os.path.join(dirs, dir)
        output_filename = f"compiled_csvs\\compiled_petrol_data_{dir}.csv"
        compile_csvs(year_folder, output_filename)
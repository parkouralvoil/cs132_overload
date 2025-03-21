import tabula
import pandas as pd
import os

# cd .\data\gas\
# python -m NCR_pump_prices_convert

yrs = ["2019", "2020", "2021", "2022", "2023", "2024", "2025"]

def extract_petroleum_table(pdf_path: str, pdf_name: str):
    """
    Extracts the petroleum price table from the PDF and saves it as a CSV.
    """
    try:
        # Read tables from PDF - Adjust parameters as needed
        tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True, lattice=True)

        target_table = None

        # Iterate through tables and find the one with the correct header structure
        for table in tables:
            if isinstance(table, pd.DataFrame):
                # Normalize column names for comparison (case-insensitive, remove extra spaces)
                cols = [str(col).lower().strip() for col in table.columns]

                if 'prevailing retail prices of petroleum products ncr' in cols[0]:
                    target_table = table
                    break  # Found the table
                print(cols)

        if target_table is None:
            #if not isinstance(first_table, pd.DataFrame): ## 2020 to 2023
            print("no tables found")
            return
            # print("Summary price table NOT found in the PDF.")
            #  # Rename columns for consistency
            # first_table.columns = ['cities', 'product', 'petron',
            #                         'shell', 'caltex', 'phoenix', 
            #                         'total', 'flying v', 'unioil', 
            #                         'seaoil', 'ptt', 'independent', 
            #                         'overall range', 'common price']
            # first_table = first_table.drop(0)
            # #shortened_table = first_table.iloc[:, :2].join(first_table.iloc[:, 12:])
            # print(first_table)
        else: ## 2024 to 2025
            print("Summary price table found in the PDF.")

            # Rename columns for consistency
            target_table.columns = ['Product', 'Overall Range Min', 'Overall Range Max', 'Common Price']
            target_table = target_table.drop(0)

            # Save to CSV
            save_to_csv(target_table, pdf_name)


    except Exception as e:
        print(f"An error occurred: {e}")

def save_to_csv(table: pd.DataFrame, pdf_name: str) -> None:
    year = ""
    for yr in yrs:
        if yr in pdf_name:
            year = yr
            break
    output_csv_path: str = f"doe_csvs\\{year}\\{pdf_name.replace(".pdf", ".csv")}"
    table.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
    print(f"Petroleum price table extracted and saved to '{output_csv_path}'")

# Example Usage
raw_data = "doe_pdfs"
for folder in os.listdir(raw_data):
    year_folder = os.path.join(raw_data, folder)
    if not ("2023" in year_folder): ## choose specific year
        continue
    for filename in os.listdir(year_folder):
        pdf_file =  os.path.join(year_folder, filename)
        if not ("ncr" in filename): ## only convert NCR data
            continue
        if os.path.exists(pdf_file):
            extract_petroleum_table(pdf_file, filename)
        else:
            print(f"Error: PDF file '{pdf_file}' not found.")
Meralco data from Typical Consumption Level PDFs (2010-2020.04)

# Notes
- only generation data available for 2009
- data needing manual intervention (see scraper):
    - `2020-5`
- manually encoded data:
    - `2010-5` (Data in pdf is image instead of text)
- missing data:
    - `2013-9`
    - `2013-10`
    - `2013-11`
    - `2017-1`
    - `2017-7` (Typical Consumption Level data is duplicate of Generation Data)
    - `2023-10`
    - `2023-11`

# How to use
To Fetch Meralco data:
1. Run `./ meralco_rates-archives_list.sh`
2. Ensure that all files were downloaded properly
    - check terminal for errors
    - check for empty (HTML) files
3. Run `python3 meralco_rates-archives_download.py`
4. Ensure that all files were downloaded properly
    - check for empty (PDF) files

For this project, only the data in `<month>-<year>_Typical Consumption Level.pdf` files are needed

To export data as one CSV file:
1. Run `python3 scraper-Typical Consumption Level.py`
    - At the end of the run, a summary of missing files will be printed. In such cases, similar data can be computed from the corresponding `<month>-<year>_Summary Schedule of Rates.pdf` file
    - If new files are listed as having changes in Header/meaning of columns, add new entry in the `headers` dict
    - If file cannot be parsed, check if PDF contains text (instead of image) and is in the expected format for the script. In the worst case scenario, you must use OCR or manually encode the values
2. Run `python3 merge_meralco_csv.py` to get final consolidated csv

# Misc
- Generally, values enclosed in parenthese `()` are discount values. This is how negative values are formatted in Accounting
- The "For Lifeline Customer" field is True when the Lifeline Discount is applied
- `Supply Cust Charge` = `Supply Cust Charge per cust/mo` / `kWh Consumption`
    - similar for `Metering Cust Charge`
- `Lifeline Discount` = `Lifeline Discount %` * (`Generation Charge + Transmission Charge + System Loss Charge + Distribution Charge + Supply Charge + Supply Cust Charge + Metering Charge + Metering Cust Charge`)
- `Universal Charge` = `UC-ME + UC-EC + UC-SCC`
- `Energy Tax` = `<first 650 kWh>*0` + `<next 350 kWh> * 0.10>` + `<next 500 kWh>*0.20` + `<remaining kWh>*0.35`



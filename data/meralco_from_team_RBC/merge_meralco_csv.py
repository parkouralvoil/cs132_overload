import csv

# NOTE: Implicit fields
all_columns = [
    "Year",
    "Month",
    "For Lifeline Customers",
]

# NOTE: actual fields, taken from headers["2024-1"] in Typical Consumption Level data scraper
all_columns.extend([
    "kWh Consumption",
    "Generation Charge",
    "Previous Months Adjustment on Generation Cost",
    "Previous Years Adjustment",
    "Power Act Reduction",
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Distribution Rate True-UP",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    "Reset Cost Adj",
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",
    "Cross Subsidy Charge",
    "CERA Refund",
    "Current RPT",
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "FIT-All Renewable",
    "Total Bill"
])

def normalize_val(val):
    val = val.strip()
    if (val == "-"):
        val = ""

    return val

missing = []
final_csv = "meralco_data_2010-2024.csv"
with open(final_csv, "w") as finalcsvfile:
    csvwriter = csv.DictWriter(finalcsvfile, fieldnames=all_columns)
    print("FIELDS", csvwriter.fieldnames)
    csvwriter.writeheader()
    for year in range(2010, 2024+1):
        for month in range(1, 12+1):
            filename = f"{year}-{month}.csv"
            try:
                csvfile = open(filename, "r")
            except FileNotFoundError:
                print("MISSING", filename)
                missing.append(f"{year}-{month}")

                continue

            for row in csv.DictReader(csvfile):
                row = {header: normalize_val(data) for (header, data) in row.items()}
                row.update({"Year": year, "Month": month})

                csvwriter.writerow(row)


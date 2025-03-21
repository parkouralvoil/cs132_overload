import os
import traceback
import csv

from PyPDF2 import PdfReader
months = [
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december"
]

def normalize_num(raw_num):
    num = str(raw_num)

    if num.startswith("(") != num.endswith(")"):
        raise ValueError(f"'{num}' contains mismatched paren")

    num = num.strip("(").rstrip(")")

    return num

def normalize_val(val):
    val = val.strip()
    # if (val == "-"):
    #     val = ""

    return val

# Headers manually listed based on header changes as detected below
# for non-listed year-month combos, use last applicable header
# e.g. 2010-2 is not in dict, use 2010-1
# NOTE: look at comments to see adjacent changes to headers
headers = {
"2010-1":
[
    "kWh Consumption",
    "Generation Charge",
    "Previous Months Adjustment on Generation Cost",
    "Previous Years Adjustment",
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Cross Subsidy Charge",
    "CERA Refund",
    "Power Act Reduction",
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "Total Bill"
],
"2010-12":
[
    "kWh Consumption",
    "Generation Charge",
    "Previous Months Adjustment on Generation Cost",
    # "Previous Years Adjustment",    #-REMOVED
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Cross Subsidy Charge",
    # "CERA Refund",                  #-REMOVED
    "Power Act Reduction",
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "Total Bill"
],
"2011-1":
[
    "kWh Consumption",
    "Generation Charge",
    "Previous Months Adjustment on Generation Cost",
    "Previous Years Adjustment",      #+READDED
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Cross Subsidy Charge",
    "CERA Refund",                    #+READDED
    "Power Act Reduction",
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "Total Bill"
],
"2011-2":
[
    "kWh Consumption",
    "Generation Charge",
    "Previous Months Adjustment on Generation Cost",
    "Previous Years Adjustment",
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Cross Subsidy Charge",
    "CERA Refund",
    "Power Act Reduction",
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Snr. Citizen Subsidy",           #+ADDED
    "Universal Charge",
    "Total Bill"
],
"2011-7":
[
    "kWh Consumption",
    "Generation Charge",
    "Previous Months Adjustment on Generation Cost",
    # "Previous Years Adjustment",    #-REMOVED
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Cross Subsidy Charge",
    # "CERA Refund",                  #-REMOVED
    "Power Act Reduction",
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Snr. Citizen Subsidy",
    "Universal Charge",
    "Total Bill"
],
"2012-3":
[
    "kWh Consumption",
    "Generation Charge",
    "Previous Months Adjustment on Generation Cost",
    # "Previous Years Adjustment",    #NOCHANGE
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",           #*MOVED
    "Cross Subsidy Charge",
    # "CERA Refund",                  #NOCHANGE
    "Power Act Reduction",
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "Total Bill"
],
# NOTE: No actual change, just stray 6 on start of PDF text
"2012-4":
[
    "kWh Consumption",
    "Generation Charge",
    "Previous Months Adjustment on Generation Cost",
    # "Previous Years Adjustment",    #NOCHANGE
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",           #NOCHANGE
    "Cross Subsidy Charge",
    # "CERA Refund",                  #NOCHANGE
    "Power Act Reduction",
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "Total Bill"
],
"2013-6":
[
    "kWh Consumption",
    "Generation Charge",
    "Previous Months Adjustment on Generation Cost",
    # "Previous Years Adjustment",    #NOCHANGE
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",
    # "Cross Subsidy Charge",         #-REMOVED
    # "CERA Refund",                  #NOCHANGE
    "Power Act Reduction",
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "Total Bill"
],
"2013-8":
[
    "kWh Consumption",
    "Generation Charge",
    "Previous Months Adjustment on Generation Cost",
    # "Previous Years Adjustment",    #NOCHANGE
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",
    # "Cross Subsidy Charge",         #NOCHANGE
    # "CERA Refund",                  #NOCHANGE
    # "Power Act Reduction",          #-REMOVED
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "Total Bill"
],
"2014-5":
[
    "kWh Consumption",
    "Generation Charge",
    # "Previous Months Adjustment on Generation Cost",    #-REMOVED
    # "Previous Years Adjustment",    #NOCHANGE
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",
    # "Cross Subsidy Charge",         #NOCHANGE
    # "CERA Refund",                  #NOCHANGE
    # "Power Act Reduction",          #NOCHANGE
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "Total Bill"
],
"2014-6":
[
    "kWh Consumption",
    "Generation Charge",
    "Previous Months Adjustment on Generation Cost",    #+READDED
    # "Previous Years Adjustment",    #NOCHANGE
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",
    # "Cross Subsidy Charge",         #NOCHANGE
    # "CERA Refund",                  #NOCHANGE
    # "Power Act Reduction",          #NOCHANGE
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "Total Bill"
],
"2014-7":
[
    "kWh Consumption",
    "Generation Charge",
    # "Previous Months Adjustment on Generation Cost",    #-REMOVED
    # "Previous Years Adjustment",    #NOCHANGE
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",
    # "Cross Subsidy Charge",         #NOCHANGE
    # "CERA Refund",                  #NOCHANGE
    # "Power Act Reduction",          #NOCHANGE
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "Total Bill"
],
"2015-2":
[
    "kWh Consumption",
    "Generation Charge",
    # "Previous Months Adjustment on Generation Cost",    #NOCHANGE
    # "Previous Years Adjustment",    #NOCHANGE
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",
    # "Cross Subsidy Charge",         #NOCHANGE
    # "CERA Refund",                  #NOCHANGE
    # "Power Act Reduction",          #NOCHANGE
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "FIT-All Renewable",              #+ADDED
    "Total Bill"
],
"2019-7":
[
    "kWh Consumption",
    "Generation Charge",
    # "Previous Months Adjustment on Generation Cost",    #NOCHANGE
    # "Previous Years Adjustment",    #NOCHANGE
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    "Reset Cost Adj",                 #+ADDED
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",
    # "Cross Subsidy Charge",         #NOCHANGE
    # "CERA Refund",                  #NOCHANGE
    # "Power Act Reduction",          #NOCHANGE
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "FIT-All Renewable",
    "Total Bill"
],
"2019-9":
[
    "kWh Consumption",
    "Generation Charge",
    # "Previous Months Adjustment on Generation Cost",    #NOCHANGE
    # "Previous Years Adjustment",    #NOCHANGE
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    # "Reset Cost Adj",               #-REMOVED
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",
    # "Cross Subsidy Charge",         #NOCHANGE
    # "CERA Refund",                  #NOCHANGE
    # "Power Act Reduction",          #NOCHANGE
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "FIT-All Renewable",
    "Total Bill"
],
"2019-10":
[
    "kWh Consumption",
    "Generation Charge",
    "Previous Months Adjustment on Generation Cost",    #+READDED
    # "Previous Years Adjustment",    #NOCHANGE
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    # "Reset Cost Adj",               #NOCHANGE
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",
    # "Cross Subsidy Charge",         #NOCHANGE
    # "CERA Refund",                  #NOCHANGE
    # "Power Act Reduction",          #NOCHANGE
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "FIT-All Renewable",
    "Total Bill"
],
"2020-7":
[
    "kWh Consumption",
    "Generation Charge",
    # "Previous Months Adjustment on Generation Cost",    #-REMOVED
    # "Previous Years Adjustment",    #NOCHANGE
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    # "Reset Cost Adj",               #NOCHANGE
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",
    # "Cross Subsidy Charge",         #NOCHANGE
    # "CERA Refund",                  #NOCHANGE
    # "Power Act Reduction",          #NOCHANGE
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "FIT-All Renewable",
    "Total Bill"
],
"2021-3":
[
    "kWh Consumption",
    "Generation Charge",
    # "Previous Months Adjustment on Generation Cost",    #NOCHANGE
    # "Previous Years Adjustment",    #NOCHANGE
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Distribution Rate True-UP",      #+ADDED
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    # "Reset Cost Adj",               #NOCHANGE
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",
    # "Cross Subsidy Charge",         #NOCHANGE
    # "CERA Refund",                  #NOCHANGE
    # "Power Act Reduction",          #NOCHANGE
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "FIT-All Renewable",
    "Total Bill"
],
"2021-5":
[
    "kWh Consumption",
    "Generation Charge",
    # "Previous Months Adjustment on Generation Cost",    #NOCHANGE
    # "Previous Years Adjustment",    #NOCHANGE
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Distribution Rate True-UP",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    # "Reset Cost Adj",               #NOCHANGE
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",
    # "Cross Subsidy Charge",         #NOCHANGE
    # "CERA Refund",                  #NOCHANGE
    # "Power Act Reduction",          #NOCHANGE
    "Current RPT",                    #+ADDED; merged Header with Local Franchise Tax
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "FIT-All Renewable",
    "Total Bill"
],
"2021-8":
[
    "kWh Consumption",
    "Generation Charge",
    # "Previous Months Adjustment on Generation Cost",    #NOCHANGE
    # "Previous Years Adjustment",    #NOCHANGE
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    "Distribution Rate True-UP",      #*MOVED; | between Metering|Distribution Rate
    # "Reset Cost Adj",               #NOCHANGE
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",
    # "Cross Subsidy Charge",         #NOCHANGE
    # "CERA Refund",                  #NOCHANGE
    # "Power Act Reduction",          #NOCHANGE
    "Current RPT",
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "FIT-All Renewable",
    "Total Bill"
],
"2021-12":
[
    "kWh Consumption",
    "Generation Charge",
    # "Previous Months Adjustment on Generation Cost",    #NOCHANGE
    # "Previous Years Adjustment",    #NOCHANGE
    "Power Act Reduction",            #+READDED *MOVED
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    "Distribution Rate True-UP",
    # "Reset Cost Adj",               #NOCHANGE
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",
    # "Cross Subsidy Charge",         #NOCHANGE
    # "CERA Refund",                  #NOCHANGE
    "Current RPT",
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "FIT-All Renewable",
    "Total Bill"
],
# NOTE: No actual change, just merge/unmerge of header cells
"2022-12":
[
    "kWh Consumption",
    "Generation Charge",
    # "Previous Months Adjustment on Generation Cost",    #NOCHANGE
    # "Previous Years Adjustment",    #NOCHANGE
    # "Power Act Reduction",          #NOCHANGE
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",                  #NOCHANGE
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    "Distribution Rate True-UP",      #NOCHANGE; full divider replaced with |
    # "Reset Cost Adj",               #NOCHANGE
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",           #NOCHANGE
    # "Cross Subsidy Charge",         #NOCHANGE
    # "CERA Refund",                  #NOCHANGE
    "Current RPT",                    #NOCHANGE; Header REmerged
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "FIT-All Renewable",              #NOCHANGE
    "Total Bill"
],
"2023-2":
[
    "kWh Consumption",
    "Generation Charge",
    # "Previous Months Adjustment on Generation Cost",    #NOCHANGE
    # "Previous Years Adjustment",    #NOCHANGE
    "Power Act Reduction",            #+READDED
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    "Distribution Rate True-UP",
    # "Reset Cost Adj",               #NOCHANGE
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",
    # "Cross Subsidy Charge",         #NOCHANGE
    # "CERA Refund",                  #NOCHANGE
    "Current RPT",
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "FIT-All Renewable",
    "Total Bill"
],
"2023-3":
[
    "kWh Consumption",
    "Generation Charge",
    # "Previous Months Adjustment on Generation Cost",    #NOCHANGE
    # "Previous Years Adjustment",    #NOCHANGE
    # "Power Act Reduction",          #-REMOVED
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    "Distribution Rate True-UP",
    # "Reset Cost Adj",               #NOCHANGE
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",
    # "Cross Subsidy Charge",         #NOCHANGE
    # "CERA Refund",                  #NOCHANGE
    "Current RPT",
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "FIT-All Renewable",
    "Total Bill"
],
"2023-6":
[
    "kWh Consumption",
    "Generation Charge",
    # "Previous Months Adjustment on Generation Cost",    #NOCHANGE
    # "Previous Years Adjustment",    #NOCHANGE
    # "Power Act Reduction",          #NOCHANGE
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Distribution Rate True-UP",      #*MOVED
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    # "Reset Cost Adj",               #NOCHANGE
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",
    # "Cross Subsidy Charge",         #NOCHANGE
    # "CERA Refund",                  #NOCHANGE
    "Current RPT",
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "FIT-All Renewable",
    "Total Bill"
],
"2023-7":
[
    "kWh Consumption",
    "Generation Charge",
    # "Previous Months Adjustment on Generation Cost",    #NOCHANGE
    # "Previous Years Adjustment",    #NOCHANGE
    # "Power Act Reduction",          #NOCHANGE
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    # "Distribution Rate True-UP",    #-REMOVED
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    # "Reset Cost Adj",               #NOCHANGE
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",
    # "Cross Subsidy Charge",         #NOCHANGE
    # "CERA Refund",                  #NOCHANGE
    "Current RPT",
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "FIT-All Renewable",
    "Total Bill"
],
"2023-12":
[
    "kWh Consumption",
    "Generation Charge",
    # "Previous Months Adjustment on Generation Cost",    #NOCHANGE
    # "Previous Years Adjustment",    #NOCHANGE
    # "Power Act Reduction",          #NOCHANGE
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    "Distribution Rate True-UP",      #+READDED
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    # "Reset Cost Adj",               #NOCHANGE
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",
    # "Cross Subsidy Charge",         #NOCHANGE
    # "CERA Refund",                  #NOCHANGE
    "Current RPT",
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "FIT-All Renewable",
    "Total Bill"
],
"2024-1":
[
    "kWh Consumption",
    "Generation Charge",
    # "Previous Months Adjustment on Generation Cost",    #NOCHANGE
    # "Previous Years Adjustment",    #NOCHANGE
    # "Power Act Reduction",          #NOCHANGE
    "Transmission Charge",
    "System Loss Charge",
    "Distribution Charge",
    # "Distribution Rate True-UP",    #-REMOVED
    "Supply Charge",
    "Supply Cust Charge",
    "Metering Charge",
    "Metering Cust Charge",
    # "Reset Cost Adj",               #NOCHANGE
    "Lifeline Discount",
    "Lifeline Rate Subsidy",
    "Snr. Citizen Subsidy",
    # "Cross Subsidy Charge",         #NOCHANGE
    # "CERA Refund",                  #NOCHANGE
    "Current RPT",
    "Local Franchise Tax",
    "VAT",
    "Energy Tax",
    "Universal Charge",
    "FIT-All Renewable",
    "Total Bill"
],
}

all_columns = ["year", "month"] + headers["2024-1"]

# Columns which are known to have empty values
# (as in not even a placeholder "-", just blank which is lost in extract_text() )
columns_with_empty = {
    # NOTE: These two are mutually exclusive
    "Lifeline Discount",
    "Lifeline Rate Subsidy",

    "Energy Tax",   # Usually empty from 50kWh to 600kWh
    "Snr. Citizen Subsidy", # Usually empty from 50kWh to 100kWh
}

# NOTE: generally, columns whose values are enclosed in () are discounts,
#       i.e. they are subtracted from the total bill instead of added
discount_columns = {
    "Lifeline Discount",
    "Previous Years Adjustment",
    "CERA Refund",
    "Power Act Reduction",
    "Reset Cost Adj",
    "Distribution Rate True-UP",
}

# NOTE: No Typical Consumption Level Data for 2009
missing = []
header_changes = []
cannot_parse = []
has_multiple_skippable = []

prev_header = None
header_cols = None
# prev_header = "PreviousMonthsSystemLifelineLocalkWhGenerationAdjustmentonTransmissionLossDistributionSupplySupplyCustMeteringMeteringLifelineRateSnr.CitizenFranchiseEnergyUniversalFIT-AllTotalConsumptionChargeGenerationCostChargeChargeChargeChargeChargeChargeCustChargeDiscountSubsidySubsidyTaxVATTax"
# header_cols = headers["2019-10"]


header_delim = "\n50 "   # first data row starts with 50kWh Consumption
last_row_delim = "\n5000"
lifeline_delim = "For Lifeline Customers"
nonlifeline_delim = "For Non-Lifeline Customers"
filename_format = "{year}/{month}-{year}_Typical Consumption Level.pdf"
for year in range(2009, 2024+1):
    for month in range(1, 12+1):
# for year in range(2020, 2020+1):
#     for month in range(5, 5+1):
        filename = filename_format.format(year=year, month=month)
        print(f"====================================\nPROCESSING {filename}")

        csvfile = None
        try:
            pdf = PdfReader(filename)
        except FileNotFoundError:
            print("MISSING", filename)
            missing.append(f"{year}-{month}")
            continue

        text = pdf.pages[0].extract_text()


        # HACK: for 2020-5, the data is missing \n for each data row start
        #        but since each actual data starts with 4.3848 (Generation Charge), we can "fix" it
        if year == 2020 and month == 5:
            print("HACK for 2020-5")
            fragments = text.split("4.3848")
            # each fragment now ends with the kWh consumption number, we just need to add "\n" prefix to each
            # Special case: 1st fragment also contains 1st table (raw numbers not per kWh). also add \n to 50 here
            frag = fragments[0]
            tbl1_start = frag.find("50")
            tbl2_start = frag.rfind("50")
            frag = (frag[:tbl1_start] + "\n50 " + frag[tbl1_start + len("50"):tbl2_start]
                    + "\n50 " + frag[tbl2_start + len("50"):])
            fragments[0] = frag

            for (i, frag) in enumerate(fragments[1:], start=1):
                row_start = frag.rfind(" ")

                if (row_start == -1):
                    raise ValueError("Faulty 2020-5 hack")

                row_start += 1
                fragments[i] = frag[:row_start] + "\n" + frag[row_start:] + " "

            # reconstruct text by adding back the 4.3848
            text = "4.3848".join(fragments)

        try:
            # Get table header
            # NOTE: Table header is mangled since it is multi-line
            #       can't be used directly without manual fixing anyway
            header_end = text.find(header_delim)
            if (header_end == -1):
                raise ValueError("Header delim not found")

            header = text[:header_end]

            # chop off last part (<month> '<year>  Bill)
            header = header[:header.rfind("Charge")]

            # sanitize header a bit; remove spaces which might be variable
            header = "".join(word.strip() for word in header.split())

            if header != prev_header or (prev_header is None):
                print(f"Header changed ON {filename}.\n")
                header_changes.append(filename)

                # update column header names
                header_cols = headers[f"{year}-{month}"]
                # print(header, rows[0], sep="\n")
                print(header)

            prev_header = header

            lifeline_delim_start = text.find(lifeline_delim, header_end+1)
            is_lifeline_customer = False
            # Get Rate per kWh data
            data_start = text.find(header_delim, header_end+1)
            if (lifeline_delim_start != -1):
                # NOTE: tdelimeter rows for "For Lifeline Customers" and "For Non-Lifeline Customers"
                #       which means there will be 4 data starts marked with \50n. Hence, we adjust data_start
                data_start = text.find(header_delim, data_start+1)
                is_lifeline_customer = True

            csvfile = open(f"{year}-{month}.csv", "w")
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([lifeline_delim] +  header_cols)

            if data_start == -1:
                raise ValueError("2nd Header delim for data start not found")
            data_start += 1     # do not include "\n" prefix character
            last_row_start = text.find(last_row_delim, data_start)
            data_end_raw = text.find("\n", last_row_start+1)

            # NOTE: some of the PDFs are malformed where there are text after the last data
            #       hence, we manually find the end of data to be where the first non numeric/paren/dash char occurs
            data_end = last_row_start+1
            while (data_end < data_end_raw):
                char = text[data_end]
                if not (char.isnumeric() or char in '(-.)' or char.isspace()):
                    break
                else:
                    data_end += 1
            data = text[data_start:data_end]

            # print("DATA: ", data, data_start, data_end)
            rows = tuple(row.split() for row in data.split("\n"))
            print("RAW ROWS", *rows, sep="\n")

            # if max(len(row) for row in rows) > len(header_cols):
            #     raise ValueError("There are more data than header columns. Aborting")

            # Process each row of data
            # NOTE: For empty cells, we:
            #       a) check if next cols are Lifeline {Discount|Rate Subsidy} and if value is enclosed in ()
            #       b) if there are N missing values, skip the last N skippable columns in columns_with_empty
            #          can lead to trouble since we may have multiple choices of which header to skip, marking as HACK
            skippable_cols = []
            for header_col in columns_with_empty:
                try:
                    idx = header_cols.index(header_col)
                    skippable_cols.append(idx)
                except ValueError:
                    # header_col not skippable, next
                    continue
            skippable_cols.sort()

            lifelinedisc_idx = header_cols.index("Lifeline Discount")
            lifelinerate_idx = header_cols.index("Lifeline Rate Subsidy")

            # print(len(header_cols), "LIFELINE", lifelinedisc_idx, skippable_cols)
            if (lifelinedisc_idx != lifelinerate_idx-1):
                raise ValueError("Lifeline columns not adjacent. Aborting")
            if (skippable_cols[0] != lifelinedisc_idx):
                raise ValueError("Lifeline not the first the first skippable column, can lead to wrong parse. Aborting")

            output = []
            multiple_skips = False
            for row in rows:
                getrawletters = lambda string: "".join(word.strip().lower() for word in string)
                if getrawletters(row) == getrawletters(nonlifeline_delim):
                    is_lifeline_customer = False;
                    print("NON LIFELINE")
                    continue

                row = list(normalize_val(val) for val in row)


                print("ROW ", row)
                # if the number of headers and data are exactly the same, just copy them over
                if (len(header_cols) == len(row)):
                    out_row = row
                else:
                    num_skippable_cols = len(skippable_cols)
                    out_row = []
                    # print("DIT", {header_cols[i]: row[i] for i in range(lifelinedisc_idx)})
                    # output.append({header_cols[i]: row[i] for i in range(lifelinedisc_idx)})

                    # Data before lifelinedisc_idx are OK to map as is
                    out_row.extend(row[:lifelinedisc_idx])

                    # Handle mutually exclusive lifeline columns (accounts for 1 missing val)
                    # If lifeline column is enclosed in (), it is discount
                    lifeline_values = (row[lifelinedisc_idx], "")
                    if (lifeline_values[0].startswith("(")):
                        # value is discount, add as is
                        out_row.extend(lifeline_values)
                        is_lifeline_customer = True
                    else:
                        # value is subsidy, discount should be empty
                        out_row.extend(reversed(lifeline_values))
                        is_lifeline_customer = False

                    num_skippable_cols -= 2     # 2 skippable lifeline columns already handled

                    val_idx = lifelinedisc_idx+1

                    num_skipped_cols = 0
                    num_missing_vals = (len(header_cols) - (lifelinerate_idx+1)) - (len(row) - (lifelinedisc_idx+1))
                    for header_idx in range(lifelinerate_idx+1, len(header_cols)):
                        # print("VAL_IDX", val_idx, "/", len(row), header_cols[header_idx])
                        is_energy_tax = header_cols[header_idx] == "Energy Tax"
                        skippable_headers = tuple(header_cols[i] for i in skippable_cols[2:])
                        if num_missing_vals > 0 and header_idx in skippable_cols:
                            if (num_skippable_cols <= 0):
                                print("ROW ", row)
                                print("OUT_ROW ", out_row)
                                raise ValueError("Ran out of skippable rows.")

                            if (len(skippable_headers) == 2 and num_missing_vals == 1 and ("Energy Tax" in skippable_headers) and (not is_energy_tax)):
                                # HACK: most of data has 4 skippable cols: the 2 lifeline cols, 1 Energy Tax, + 1 other col
                                #       in such cases, usually the Energy tax column should be skipped first
                                # FALLTHROUGH: let current skippable header consume value
                                pass
                            else:
                                num_missing_vals -= 1
                                num_skippable_cols -= 1
                                num_skipped_cols += 1
                                if (num_skipped_cols >= 1 and len(skippable_cols) > 3 and not is_energy_tax):
                                    multiple_skips = True
                                out_row.append("")
                                continue

                        if (val_idx >= len(row)):
                            print("ROW ", row)
                            print("OUT_ROW ", out_row)
                            print("COLUMNS ", header_cols)
                            print("HEADER ", header_idx, header_cols[header_idx])
                            input()
                            raise ValueError("Ran out of data (probably failed to skip a row)")

                        out_row.append(row[val_idx])
                        val_idx += 1

                    if val_idx != len(row):
                        print("ROW", row)
                        print("OUT_ROW", out_row)
                        print("VAL_IDX")
                        raise ValueError("Not all values in row consumed (probably skipped too much).")
                    # print(out_row)


                csvwriter.writerow([is_lifeline_customer] + out_row)
                # input()
            csvfile.close()

            if (multiple_skips):
                has_multiple_skippable.append((filename, skippable_cols))

            #
            # # For the rest, process sequentially
            # for i, row in enumerate(rows):
            #     # rint(i, row, len(row))
            #     # input()
            #     num_missing_vals = len(header_cols) - len(row)
            #     num_skippable_cols = len(skippable_cols)
            #
            #     # Handle mutually exclusive lifeline columns (accounts for 1 missing val)
            #     # If lifeline column is enclosed in (), it is discount
            #     lifeline_header = "Lifeline Discount" if row[lifelinedisc_idx].startswith("(") else "Lifeline Rate Subsidy"
            #     output[i][lifeline_header] = row[lifelinedisc_idx]
            #     num_missing_vals -= 1
            #     num_skippable_cols -= 2
            #
            #     row_idx = lifelinedisc_idx+1
            #     for j in range(lifelinerate_idx+1, len(header_cols)):
            #         print("ROW", i, j, f"{row_idx}/{len(row)}", skippable_cols, num_skippable_cols, num_missing_vals, row[row_idx])
            #         # input()
            #         # if (len(header_cols)-j) > (len(row)-row_idx) and j in skippable_cols:
            #         if num_skippable_cols == num_missing_vals and j in skippable_cols:
            #             print(f"ROW {i} SKIPPED Column {j}({header_cols[j]}) VAL: {row[row_idx]}")
            #             num_missing_vals -= 1
            #             num_skippable_cols -= 1
            #             continue
            #
            #         output[i]
            #         header_cols[j]
            #         row[row_idx]
            #         output[i][header_cols[j]] = row[row_idx]
            #         row_idx += 1
            #
            #     # at end of row processing, ALL values must be consumed
            #     assert(row_idx == len(row))
            #     # print(output[i], sep="\n")
            #     # input()
            #
            # print(output)

        except ValueError as err:
            # Mainly relies on failing str.index() in try block above which throws ValueError
            print(f"Cannot Parse {filename}.\n")
            cannot_parse.append(filename)

            traceback.print_exc();

            if csvfile is not None:
                csvfile.close()
            # input()
            continue

print()
print("Data files for the following year-month combos were not found:")
print(*missing, sep="\n")

print()
print("The following files could not be parsed (probably image in PDF instead of text, or wrong table)")
print(*cannot_parse, sep="\n")

print()
print("Check the following files for changes in Header/meaning of columns:")
print(*header_changes, sep="\n")

print()
print("Check the following files with multiple skippable columns (prone to parsing errors):")
print(*has_multiple_skippable, sep="\n")




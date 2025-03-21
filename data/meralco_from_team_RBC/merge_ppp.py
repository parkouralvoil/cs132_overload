import csv

months = [
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec"
]

ppp_label = "Purchasing Power of Peso"
# Process Purchasing Power of Peso (PPP) data
ppp_out = ([], [])
files = ("csv/2M4ACPI8.csv",    # 2009-2021 (2012=100); Taken from https://openstat.psa.gov.ph/Metadata/2M4ACPI8
         "csv/2M4ACP11.csv", )  # 2018-2024 (2018=100); Taken from https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__2M__PI__CPI__2018/0012M4ACP11.px/?rxid=3004aad9-714b-481e-9028-dae96552d58d
for (j, file) in enumerate(files):
    with open(file) as csvfile:
        csvreader = csv.reader(csvfile)
        # Get rid of unneeded first two rows (no data)
        next(csvreader)
        next(csvreader)

        # Get column labels. First two columns are just non-data
        year_month = next(csvreader)[2:]
        # Get correponding data
        ppp = next(csvreader)[2:]

        # Data is a flatlist with column label of form YYYY-Month
        # Transform to rows with Year, Month, PPP (numerical) fields
        for (i, label) in enumerate(year_month):
            year, month = map(lambda s: s.lower().strip(), label.split())
            year = int(year)

            # Skip entries for yearly average
            if (month == "ave"):
                continue
            month = months.index(month) + 1

            data = ppp[i].strip()
            if (data in ("", "..")):
                print("NOTE: Skipping empty data for", year, month, f"({data})")
                continue

            ppp_out[j].append({
                "Year": year,
                "Month": month,
                ppp_label: data
            })

ppp2012, ppp2018 = ppp_out
print("PPP 2009-2010 (2012=100):", *ppp2012, sep="\n")
print()
print("PPP 2018-2024 (2018=100):", *ppp2018, sep="\n")

# NOTE: For 2018=100, the PPP for 2018 Jul (2018-7) is 1
#       For 2012=100, the PPP for 2018 Jul (2018-7) is 0.85
#       Hence, we use PPP_2012 == (PPP_2018)*0.85 for conversion
# NOTE: This conversion results to off-by-one errors (+-0.01) since original values are truncated
#       Nevertheless, this is the best value we can get without having actual non-truncated conversion factor
ppp2018_to2012 = [
    {
        "Year": entry["Year"],
        "Month": entry["Month"],
        ppp_label: round(float(entry[ppp_label])*0.85, 2)
    }
    for entry in ppp2018
]

# Add converted to ppp2012
# NOTE: Always prefer value in ppp2012, so we remove overlap months in ppp2018
ppp2012_months = {(e["Year"], e["Month"]) for e in ppp2012}
ppp2018_months = {(e["Year"], e["Month"]) for e in ppp2018}
overlap_months = ppp2012_months & ppp2018_months
ppp2018_to2012 = [entry for entry in ppp2018_to2012 if (entry["Year"], entry["Month"]) not in overlap_months]

ppp2012.extend(ppp2018_to2012)

# Verify that we are not missing data
final_months = {(e["Year"], e["Month"]) for e in ppp2012}
for year in range(2009, 2024+1):
    for month in range(1, 12+1):
        if year == 2024 and month > 3:
            continue

        assert((year, month) in final_months or print(f"ERROR {year}-{month}"))


# Write data to csv
with open("purchasing_power_peso.csv", "w") as finalcsvfile:
    fields = tuple(ppp2012[0].keys())
    csvwriter = csv.DictWriter(finalcsvfile, fieldnames=fields)
    print("FIELDS", csvwriter.fieldnames)
    csvwriter.writeheader()

    for entry in ppp2012:
        csvwriter.writerow(entry)



#
# NOTE: Code below is not used anymore; 0.85 conversion factor results to LESS errors than mean conversion factor
#       This might be needed in data exploration, so keeping as a comment for now
# # Convert 2018-2024 data to 2012 baseline
# # NOTE: For 2018=100, the PPP for 2018 Jul (2020-7) is 1
# #       For 2012=100, the PPP for 2018 Jul (2020-7) is 0.85
# #       Ideally, we should use PPP_2012 == (PPP_2018)*0.85 for conversion
# #       BUT the values are truncated so it can be off by 0.01
# #       e.g. for 2018 Sep, PPP_2012 = 0.84 and PPP_2018 = 0.98
# #            but PPP_2018*0.85 = 0.98*0.85 = 0.833 != 0.84 (PPP_2012)
#
# # HACK: We instead use the mean of the conversion factors for the overlap months (2018 to 2021)
# # First, convert data to easy lookup table
# ppp2012_tbl = {(e["Year"], e["Month"]): float(e[ppp_label]) for e in ppp2012}
# ppp2018_tbl = {(e["Year"], e["Month"]): float(e[ppp_label]) for e in ppp2018}
#
# # Next, get conversion factors; PPP_2012 = x*PPP_2018  =>  x = PPP_2012/PPP_2018)
# overlap_months = set(ppp2012_tbl.keys()) & set(ppp2018_tbl.keys())
# conv_factors = tuple(ppp2012_tbl[month] / ppp2018_tbl[month] for month in overlap_months)
# print("Conversion factors (2018-2021)", conv_factors)
#
# # Compute mean conversion factor; verify accuracy by comparing with PPP_2012
# mean_convf = sum(conv_factors) / len(conv_factors)
# for month in overlap_months:
#     # NOTE: use 2 decimal places just like original data
#     orig2012 = round(ppp2012_tbl[month], 2)
#     conv2018 = round(ppp2018_tbl[month]*mean_convf, 2)
#     if conv2018 != orig2012:
#         print(f"Mean Conversion factor {mean_convf} does not work for {month} PPP_2012={orig2012} PPP_2018={conv2018}")
#
#

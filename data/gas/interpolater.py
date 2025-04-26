import pandas as pd

"""
this is for
petro_ncr_2020_aug_27
and
petro_ncr_2020_may_14

"""

# python -m interpolater

# Function to check for gaps > 10 days between consecutive dates for each product
def check_date_gaps(df, max_gap_days=10):
    gaps_found = []
    
    for product in df['Product'].unique():
        product_data = df[df['Product'] == product].sort_values('Date')
        dates = product_data['Date']
        
        for i in range(1, len(dates)):
            gap = (dates.iloc[i] - dates.iloc[i-1]).days
            print(gap)
            if gap > max_gap_days:
                gaps_found.append({
                    'Product': product,
                    'Previous Date': dates.iloc[i-1],
                    'Next Date': dates.iloc[i],
                    'Gap (days)': gap
                })
    
    return pd.DataFrame(gaps_found)



if __name__ == "__main__":
    data = pd.read_csv('compiled_csvs\\compiled_all.csv', parse_dates=['Date'])

    # Sort by Product and Date to ensure correct order
    data = data.sort_values(['Product', 'Date'])

    filtered_data = data[data['Product'] == 'Gasoline (RON95)'].sort_values('Date')
    # Check for gaps
    gap_results = check_date_gaps(filtered_data)

    if not gap_results.empty:
        print("Gaps longer than 10 days found:")
        print(gap_results)
    else:
        print("No gaps longer than 10 days found in the data.")
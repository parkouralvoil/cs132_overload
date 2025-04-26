import pandas as pd
from datetime import timedelta

"""
this is for
petro_ncr_2020_aug_27
and
petro_ncr_2020_may_14

"""

# python -m interpolater

PRODUCT_ORDER = {
    'Gasoline (RON97/100)': 0,
    'Gasoline (RON95)': 1,
    'Gasoline (RON91)': 2,
    'Diesel': 3,
    'Diesel Plus': 4,
    'Kerosene': 5
}

# Function to check for gaps > 10 days between consecutive dates for each product
def check_date_gaps(df, max_gap_days=10):
    gaps_found = []
    
    for product in df['Product'].unique():
        product_data = df[df['Product'] == product].sort_values('Date')
        dates = product_data['Date']
        
        for i in range(1, len(dates)):
            gap = (dates.iloc[i] - dates.iloc[i-1]).days
            #print(gap)
            if gap > max_gap_days:
                gaps_found.append({
                    'Product': product,
                    'Previous Date': dates.iloc[i-1],
                    'Next Date': dates.iloc[i],
                    'Gap (days)': gap
                })
    
    return pd.DataFrame(gaps_found)

def interpolate_data(df, max_gap_days):
    # Make a copy of the original dataframe to avoid modifying it directly
    new_df = df.copy()
    
    # Convert Date column to datetime if not already
    new_df['Date'] = pd.to_datetime(new_df['Date'])
    
    # Sort by Product (using the defined order) and Date
    new_df['Product_Order'] = new_df['Product'].map(PRODUCT_ORDER)
    new_df = new_df.sort_values(['Product_Order', 'Date'])
    
    # We'll collect all new rows to add here
    new_rows = []
    
    for product in new_df['Product'].unique():
        product_data = new_df[new_df['Product'] == product].sort_values('Date', ascending=False)  # Sort dates descending
        dates = product_data['Date']
        
        for i in range(1, len(dates)):
            gap = (dates.iloc[i-1] - dates.iloc[i]).days  # Note reversed order for descending dates
            
            if gap > max_gap_days:
                # Calculate midpoint date
                midpoint_date = dates.iloc[i-1] - timedelta(days=gap // 2)
                prev_row = product_data.iloc[i-1]  # More recent date
                next_row = product_data.iloc[i]   # Older date
                
                # Interpolate the values (50% between the two)
                new_min = (prev_row['Overall Range Min'] + next_row['Overall Range Min']) / 2
                new_max = (prev_row['Overall Range Max'] + next_row['Overall Range Max']) / 2
                new_common = (prev_row['Common Price'] + next_row['Common Price']) / 2
                
                # Create new row
                new_row = {
                    'Year': midpoint_date.year,
                    'Date': midpoint_date,
                    'Product': product,
                    'Overall Range Min': round(new_min, 2),
                    'Overall Range Max': round(new_max, 2),
                    'Common Price': round(new_common, 2),
                    'Product_Order': PRODUCT_ORDER[product]
                }
                
                new_rows.append(new_row)
    
    # Add all new rows to the dataframe
    if new_rows:
        new_rows_df = pd.DataFrame(new_rows)
        new_df = pd.concat([new_df, new_rows_df], ignore_index=True)
        
        # Re-sort the dataframe
        new_df['Product_Order'] = new_df['Product'].map(PRODUCT_ORDER)
        new_df = new_df.sort_values(
            by=['Date', 'Product_Order'],
            ascending=[False, True]
        ).drop(columns=['Product_Order'])
    
    return new_df

def check_run(check_raw: bool):
    if check_raw:
        data = pd.read_csv('compiled_csvs\\compiled_all.csv', parse_dates=['Date'])
    else:
        data = pd.read_csv('compiled_csvs\\compiled_all_interpolated.csv', parse_dates=['Date'])

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

def modify_run():
    data = pd.read_csv('compiled_csvs\\compiled_all.csv', parse_dates=['Date'])
    
    # Sort by Product and Date to ensure correct order
    
    # Interpolate data where gaps are found
    interpolated_data = interpolate_data(data, max_gap_days=10)
    
    # Save or use the interpolated data
    interpolated_data.to_csv('compiled_csvs\\compiled_all_interpolated.csv', index=False)
    print("Interpolation complete. Data saved to compiled_all_interpolated.csv")

if __name__ == "__main__":
    # modify_run()
    check_run(check_raw=True)
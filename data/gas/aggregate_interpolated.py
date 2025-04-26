import pandas as pd

# python -m aggregate_interpolated

PRODUCT_ORDER = {
    'Gasoline (RON97/100)': 0,
    'Gasoline (RON95)': 1,
    'Gasoline (RON91)': 2,
    'Diesel': 3,
    'Diesel Plus': 4,
    'Kerosene': 5
}

def aggregate_to_monthly(input_csv, output_csv):
    # Read the CSV file
    df = pd.read_csv(input_csv, parse_dates=['Date'])
    
    # Extract year and month for grouping
    df['YearMonth'] = df['Date'].dt.to_period('M')
    
    # Add product order for sorting
    df['Product_Order'] = df['Product'].map(PRODUCT_ORDER)
    
    # Group by YearMonth and Product, then calculate averages
    monthly_agg = df.groupby(['YearMonth', 'Product', 'Product_Order']).agg({
        'Overall Range Min': 'mean',
        'Overall Range Max': 'mean',
        'Common Price': 'mean'
    }).reset_index()
    
    # Round the values to 2 decimal places
    monthly_agg['Overall Range Min'] = monthly_agg['Overall Range Min'].round(2)
    monthly_agg['Overall Range Max'] = monthly_agg['Overall Range Max'].round(2)
    monthly_agg['Common Price'] = monthly_agg['Common Price'].round(2)
    
    # Create a proper date column (first day of each month)
    monthly_agg['Date'] = monthly_agg['YearMonth'].dt.to_timestamp()
    monthly_agg['Year'] = monthly_agg['Date'].dt.year
    
    # Sort by Date (descending) then by Product_Order (ascending)
    monthly_agg = monthly_agg.sort_values(['Date', 'Product_Order'], ascending=[False, True])
    
    # Select and reorder columns to match original format
    final_output = monthly_agg[[
        'Year', 'Date', 'Product', 
        'Overall Range Min', 'Overall Range Max', 'Common Price'
    ]]
    
    # Save to CSV
    final_output.to_csv(output_csv, index=False)
    print(f"Monthly aggregated data saved to {output_csv}")

if __name__ == "__main__":
    input_file = 'compiled_csvs/compiled_all_interpolated.csv'
    output_file = 'compiled_csvs/monthly_aggregated.csv'
    aggregate_to_monthly(input_file, output_file)
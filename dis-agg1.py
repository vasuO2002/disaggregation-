import pandas as pd
import glob

# List of modified CSV files
modified_files = [
    '8169574_modified.csv',
    '8169576_modified.csv',
    '8169577_modified.csv',
    '8169573_modified.csv',
    '8169575_modified.csv'
]

# Initialize a list to hold data from all files
all_data = []

# Process each modified CSV file
for file in modified_files:
    df = pd.read_csv(file)
    
    # Extract required columns and add sku_code from filename
    df['sku_code'] = file.split('_')[0]  # Assuming SKU code is part of the filename before the first underscore
    all_data.append(df[['sku_code', 'Ratio', 'Date & Time']].rename(columns={'Date & Time': 'order_date', 'Ratio': 'ratio'}))

# Combine all data into a single DataFrame
combined_df = pd.concat(all_data)

# Sort the combined DataFrame by order_date
combined_df = combined_df.sort_values(by='order_date')

# Save the sorted data to a new CSV file
combined_df.to_csv('combined_data1.csv', index=False)

print("Combined CSV file created successfully.")

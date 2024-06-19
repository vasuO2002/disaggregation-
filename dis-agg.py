import pandas as pd
import glob

# List of Excel files
file_list = [
    '8169574.xlsx',
    '8169576.xlsx',
    '8169577.xlsx',
    '8169573.xlsx',
    '8169575.xlsx'
]

# Initialize a dictionary to hold aggregated data
aggregate_data = {}

# Step 1: Process each Excel file
for file in file_list:
    df = pd.read_excel(file, sheet_name='Active Historical Data')
    
    # Convert 'Date & Time' to datetime
    df['Date & Time'] = pd.to_datetime(df['Date & Time'])
    
    # Group by date and sum 'Actual Data'
    daily_sum = df.groupby(df['Date & Time'].dt.date)['Actual Data'].sum().reset_index()
    
    # Add to aggregate_data
    for index, row in daily_sum.iterrows():
        date = row['Date & Time']
        actual_data = row['Actual Data']
        if date in aggregate_data:
            aggregate_data[date] += actual_data
        else:
            aggregate_data[date] = actual_data

# Convert aggregate_data to a DataFrame
aggregate_df = pd.DataFrame(list(aggregate_data.items()), columns=['Date', 'Total Actual Data'])

# Step 2: Process each Excel file again to compute the ratio and save modified CSV files
for file in file_list:
    df = pd.read_excel(file, sheet_name='Active Historical Data')
    
    # Convert 'Date & Time' to datetime
    df['Date & Time'] = pd.to_datetime(df['Date & Time'])
    
    # Compute the ratio
    df['Date'] = df['Date & Time'].dt.date
    df = df.merge(aggregate_df, how='left', on='Date')
    df['Ratio'] = df['Actual Data'] / df['Total Actual Data']
    
    # Save the modified DataFrame to a new CSV file
    output_file = file.replace('.xlsx', '_modified.csv')
    df.to_csv(output_file, index=False)
    
# Step 3: Save the aggregate data to a new CSV file
aggregate_df.to_csv('aggregate_data1.csv', index=False)

import os
import pandas as pd
from datetime import datetime

# Directory path where the CSV files are stored
csv_dir = "C:\\Program Files\\OpenHardwareMonitor"  # Change this according to the actual location

# Get the current date in YYYY-MM-DD format
today_date = datetime.now().strftime("%Y-%m-%d")

# Construct the expected CSV filename
csv_filename = f"OpenHardwareMonitorLog-{today_date}.csv"
csv_path = os.path.join(csv_dir, csv_filename)

# Check if the expected CSV file exists; if not, find the most recent available file
if not os.path.exists(csv_path):
    csv_files = [f for f in os.listdir(csv_dir) if f.startswith("OpenHardwareMonitorLog-") and f.endswith(".csv")]
    
    if csv_files:
        csv_files.sort(reverse=True)  # Sort by filename (assumed to be date-based)
        csv_filename = csv_files[0]  # Select the most recent file
        csv_path = os.path.join(csv_dir, csv_filename)

# If a valid CSV file is found, process it
if os.path.exists(csv_path):
    try:
        # Load the CSV into a DataFrame
        df = pd.read_csv(csv_path, low_memory=False)

        # Use the first row as the actual header and remove the first two rows
        df.columns = df.iloc[0]  # Assign first row as column names
        df = df[1:].reset_index(drop=True)  # Remove the duplicate header row

        # Find all column indices containing "CPU Package"
        cpu_package_indices = [i for i, col in enumerate(df.columns) if "CPU Package" in str(col)]
        
        # Ensure at least two "CPU Package" occurrences exist
        if len(cpu_package_indices) >= 2:
            cpu_package_index = cpu_package_indices[1]  # Select the second occurrence
            
            # Extract the column based on the identified index
            cpu_temp_values = df.iloc[:, cpu_package_index]

            # Convert values to numeric, handling conversion errors
            cpu_temp_values = pd.to_numeric(cpu_temp_values, errors='coerce')

            # Get the last valid temperature value
            cpu_temp = cpu_temp_values.dropna().iloc[-1]

            # Print only the numeric value (for integration with Zabbix)
            print(cpu_temp)
        else:
            print("0")  # Return 0 if the second "CPU Package" column is not found

    except Exception as e:
        print("0")  # Return 0 in case of processing errors
else:
    print("0")  # Return 0 if no valid CSV file is found

import pandas as pd
import json

def find_duplicates(file_name):
    # Load the JSON file
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: The file '{file_name}' is not a valid JSON file.")
        return
    
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(data)
    
    # Check if the DataFrame is empty
    if df.empty:
        print("The data is empty.")
        return
    
    # Check the column names to ensure 'pid' exists
    print("Columns in DataFrame:")
    print(df.columns.tolist())
    
    # Ensure the DataFrame contains the 'pid' column
    if 'pid' not in df.columns:
        print("Error: 'pid' column not found in the data.")
        return
    
    # Display the first few rows of the DataFrame
    print("Data preview:")
    print(df.head())
    
    # Check for duplicates based on 'pid'
    duplicates = df[df.duplicated(subset=['pid'], keep=False)]
    
    if duplicates.empty:
        print("No duplicates found based on 'pid'.")
    else:
        print("Duplicates found based on 'pid':")
        print(duplicates)
        
    # Additional: Group by 'pid' to see counts and details
    print("\nDetailed counts of 'pid':")
    pid_counts = df.groupby('pid').size().reset_index(name='count')
    pid_counts = pid_counts[pid_counts['count'] > 1]  # Filter to show only 'pid' with more than one occurrence
    
    if pid_counts.empty:
        print("No 'pid' has duplicates.")
    else:
        print(pid_counts)

if __name__ == "__main__":
    file_name = input("Enter the name of the JSON file to check for duplicates: ")
    find_duplicates(file_name)

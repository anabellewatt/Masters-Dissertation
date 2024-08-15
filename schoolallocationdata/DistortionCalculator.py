import pandas as pd

# Define file paths
input_file_path = r"C:\Users\anabe\OneDrive\Graduate School\Dissertation\schoolallocationdata\project_students-ug4-s8.txt"
output_file_path = r"C:\Users\anabe\OneDrive\Graduate School\Dissertation\schoolallocationdata\project_students_cleaned.csv"

# Read the text file with a delimiter and skip unnecessary rows
data = pd.read_csv(input_file_path, delimiter=r' \| ', engine='python', skipinitialspace=True)

# Display the first few rows of the dataframe to check the data
print("First few rows of the data:")
print(data.head())

# Strip any leading/trailing spaces from column names
data.columns = data.columns.str.strip()

# Save the cleaned data to a new CSV file
data.to_csv(output_file_path, index=False)

print(f"Cleaned data saved to: {output_file_path}")

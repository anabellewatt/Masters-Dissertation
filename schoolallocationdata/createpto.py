import pandas as pd

# Define input CSV file paths
mentor_project_csv = 'schoolallocationdata/supervisorproject18-19.csv'  # CSV file containing mentor ID and project ID
project_capacity_csv = 'projects_data18-19.csv'  # CSV file containing project ID and capacity

# Read CSV files into DataFrames
mentor_project_df = pd.read_csv(mentor_project_csv)
project_capacity_df = pd.read_csv(project_capacity_csv)

# Rename columns to have a common key for merging
project_capacity_df.rename(columns={'id': 'project_id', 'max_students': 'capacity'}, inplace=True)

# Merge data from project_capacity_df into mentor_project_df based on the common column 'project_id'
merged_df = pd.merge(mentor_project_df, project_capacity_df, on='project_id', how='left')

# Select only the required columns: 'project_id', 'person_id', and 'capacity'
selected_columns_df = merged_df[['project_id', 'person_id', 'capacity']]

# Write the selected columns to a new CSV file
output_csv = 'mentor_project_capacity18-19.csv'
selected_columns_df.to_csv(output_csv, index=False)

print(f"Combined data with selected columns has been successfully written to {output_csv}")

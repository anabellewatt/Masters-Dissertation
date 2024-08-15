import pandas as pd

# Define input CSV file paths
project_data_csv = 'projects_data18-19.csv'  # CSV file containing project data with id and owner_id
roles_csv = 'roles18-19.csv'  # CSV file containing roles with person_id and role_id (e.g., student)

# Read CSV files into DataFrames
project_data_df = pd.read_csv(project_data_csv)
roles_df = pd.read_csv(roles_csv)

# Convert relevant columns to strings to avoid data type mismatches during merge
project_data_df['owner_person_id'] = project_data_df['owner_person_id'].astype(str)
roles_df['person_id'] = roles_df['person_id'].astype(str)

# Filter roles DataFrame to only include students
students_df = roles_df[roles_df['role_id'] == 'student']

# Merge project data with students to find which projects were proposed by students
merged_df = pd.merge(project_data_df, students_df, left_on='owner_person_id', right_on='person_id', how='inner')

# Select the required columns: 'id' (project_id) and 'owner_id' (person_id)
student_proposals_df = merged_df[['id', 'owner_person_id']].copy()

# Rename columns for clarity
student_proposals_df.rename(columns={'id': 'project_id', 'owner_person_id': 'person_id'}, inplace=True)

# Write the student proposals data to a new CSV file
output_csv = 'student_proposals18-19.csv'
student_proposals_df.to_csv(output_csv, index=False)

print(f"Student proposals data has been successfully written to {output_csv}")

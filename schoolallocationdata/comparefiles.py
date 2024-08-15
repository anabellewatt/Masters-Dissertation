import pandas as pd

# Read data from CSV file
input_csv = 'mentor_project_capacity18-19.csv'
df = pd.read_csv(input_csv)

# Group by Supervisor and aggregate data
result = df.groupby('Supervisor').agg(
    Project_Count=('project', 'count'),
    Max_Students_Sum=('max_students', 'sum')
).reset_index()

# Export the result to a new CSV file
output_csv = 'supervisor_summary18-19.csv'
result.to_csv(output_csv, index=False)

print(f"Summary data has been exported to {output_csv}")

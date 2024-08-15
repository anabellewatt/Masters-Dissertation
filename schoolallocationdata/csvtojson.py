import pandas as pd
import json

# Define input CSV file paths
projects_students_clean_csv = './schoolallocationdata/student_data18-19.csv'
mentor_max_load_csv = 'supervisor_summary18-19.csv'
mentor_project_capacity_csv = 'mentor_project_capacity18-19.csv'
#dont need this for my allocation was used for school allocation
#student_proposals_csv = 'student_proposals18-19.csv'

# Read CSV files into DataFrames
projects_students_clean_df = pd.read_csv(projects_students_clean_csv)
mentor_max_load_df = pd.read_csv(mentor_max_load_csv)
mentor_project_capacity_df = pd.read_csv(mentor_project_capacity_csv)
#student_proposals_df = pd.read_csv(student_proposals_csv)

# Function to safely convert columns to integers
def safe_convert_to_int(df, columns):
    for column in columns:
        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0).astype(int)

# Convert relevant columns to integers
safe_convert_to_int(projects_students_clean_df, ['sid', 'pid', 'rank'])
safe_convert_to_int(mentor_max_load_df, ['person_id', 'max_load'])
safe_convert_to_int(mentor_project_capacity_df, ['project_id', 'person_id', 'capacity'])
#safe_convert_to_int(student_proposals_df, ['project_id', 'person_id'])

# Create "spr" list of dictionaries with only pid, sid, and rank
spr_list = projects_students_clean_df[['sid', 'pid', 'rank']].rename(columns={
    'sid': 'sid',
    'pid': 'pid'
}).to_dict(orient='records')

# Ensure all values in "spr" are integers
for entry in spr_list:
    entry['sid'] = int(entry['sid'])
    entry['pid'] = int(entry['pid'])
    entry['rank'] = int(entry['rank'])

# Create "tl" list of dictionaries with only mid and load
tl_list = mentor_max_load_df[['person_id', 'max_load']].rename(columns={
    'person_id': 'mid',
    'max_load': 'load'
}).to_dict(orient='records')

# Ensure all values in "tl" are integers
for entry in tl_list:
    entry['mid'] = int(entry['mid'])
    entry['load'] = int(entry['load'])

# Create "pto" list of dictionaries with only pid, mid, and instance
pto_list = mentor_project_capacity_df[['project_id', 'person_id', 'capacity']].rename(columns={
    'project_id': 'pid',
    'person_id': 'mid',
    'capacity': 'inst'
}).to_dict(orient='records')

# Ensure all values in "pto" are integers
for entry in pto_list:
    entry['pid'] = int(entry['pid'])
    entry['mid'] = int(entry['mid'])
    entry['inst'] = int(entry['inst'])

# # Create "gp" list of dictionaries with only sid and pid
# gp_list = student_proposals_df[['project_id', 'person_id']].rename(columns={
#     'project_id': 'pid',
#     'person_id': 'sid'
# }).to_dict(orient='records')

# # Ensure all values in "gp" are integers
# for entry in gp_list:
#     entry['pid'] = int(entry['pid'])
#     entry['sid'] = int(entry['sid'])

# Construct the final JSON structure
final_json = {
    "spr": spr_list,
    "tl": tl_list,
    "pto": pto_list,
    #"gp": gp_list
}

# Define output JSON file path
output_json_file = 'output.json'

# Save the JSON object to a file
with open(output_json_file, 'w') as json_file:
    json.dump(final_json, json_file, indent=4)

print(f"JSON data has been successfully written to {output_json_file}")

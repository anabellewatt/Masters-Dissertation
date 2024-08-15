import os
import json
import csv
import random

# Function to generate a random 4-digit student ID
def generate_student_id():
    return random.randint(1000, 9999)

# Read the CSV file to create a dictionary mapping project names to project IDs
project_name_to_id = {}
with open('Project-ids.csv', 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    
    # Print out the column headers to debug
    headers = reader.fieldnames
    print(f"CSV Headers: {headers}")
    
    # Check if 'title' and 'id' are in headers
    if 'ptitle' not in headers or 'pid' not in headers:
        raise KeyError("CSV file does not contain required 'title' and 'id' columns.")
    
    for row in reader:
        project_name_to_id[row['ptitle']] = int(row['pid'])

# Define directories
input_dir = './Student_Data'
output_dir = 'Input_Json/SurveyInput'

# Initialize data structures for aggregation
checked_data = []
group_data = []
ranked_data = []
score_data = []

# Process each student's JSON file
for filename in os.listdir(input_dir):
    if filename.endswith('.json'):
        with open(os.path.join(input_dir, filename), 'r') as file:
            student_data = json.load(file)
        
        student_id = generate_student_id()

        # Extract and transform data for checked projects
        for status, projects in student_data['checkedProjects']['M'].items():
            check_status = "Yes" if status == "approved" else "No"
            for project in projects['L']:
                project_name = project['S']
                project_id = project_name_to_id.get(project_name)
                if project_id:
                    checked_data.append({
                        "sid": student_id,
                        "pid": project_id,
                        "check": check_status
                    })

        # Extract and transform data for group projects
        group_mapping = {
            "really-want": "A",
            "okay-with": "B",
            "dont-want": "C",
            "not-qualified": "D"
        }
        for category, projects in student_data['groupProjects']['M'].items():
            group_status = group_mapping.get(category, "Unknown")
            for project in projects['L']:
                project_name = project['S']
                project_id = project_name_to_id.get(project_name)
                if project_id:
                    group_data.append({
                        "sid": student_id,
                        "pid": project_id,
                        "group": group_status
                    })

        # Extract and transform data for ranked projects
        for rank, project in enumerate(student_data['rankedProjects']['L'], start=1):
            project_name = project['S']
            project_id = project_name_to_id.get(project_name)
            if project_id:
                ranked_data.append({
                    "sid": student_id,
                    "pid": project_id,
                    "rank": rank
                })

        # Extract and transform data for score projects
        for rank, project in enumerate(student_data['scoreProjects']['L'], start = 1):
            project_name = project['M']['name']['S']
            score = int(project['M']['score']['N'])
            project_id = project_name_to_id.get(project_name)
            if project_id:
                score_data.append({
                    "sid": student_id,
                    "pid": project_id,
                    "rank": rank,
                    "score": score
                })

# Write the aggregated data to JSON files
with open(os.path.join(output_dir, 'checked.json'), 'w') as file:
    json.dump(checked_data, file, indent=4)

with open(os.path.join(output_dir, 'group.json'), 'w') as file:
    json.dump(group_data, file, indent=4)

with open(os.path.join(output_dir, 'ranked.json'), 'w') as file:
    json.dump(ranked_data, file, indent=4)

with open(os.path.join(output_dir, 'score.json'), 'w') as file:
    json.dump(score_data, file, indent=4)

import json
from collections import Counter

# Load the JSON file
with open('output.json', 'r') as file:
    data = json.load(file)

# Extract spr and pto lists
spr = data.get('spr', [])
pto = data.get('pto', [])

# Create a dictionary of project IDs to mentor IDs in pto
pto_project_to_mentor = {entry['pid']: entry['mid'] for entry in pto}

# Create a set of project IDs in pto
pto_project_ids = set(pto_project_to_mentor.keys())

# Create a set of project IDs ranked by students in spr
spr_project_ids = {entry['pid'] for entry in spr}

# Validate the projects ranked by students
invalid_entries = []

for entry in spr:
    sid = entry['sid']
    pid = entry['pid']
    rank = entry['rank']
    
    if pid not in pto_project_ids:
        invalid_entries.append(entry)

# Find projects in pto that no one ranked in spr
unranked_projects = pto_project_ids - spr_project_ids

# Check for duplicate project IDs in pto
pto_project_counts = Counter(entry['pid'] for entry in pto)
duplicate_projects = [pid for pid, count in pto_project_counts.items() if count > 1]

# Output the results
if invalid_entries:
    print(f"Found {len(invalid_entries)} invalid entries in spr:")
    for entry in invalid_entries:
        print(f"Student ID: {entry['sid']}, Project ID: {entry['pid']}, Rank: {entry['rank']}")
else:
    print("All projects ranked by students in spr are valid.")

if unranked_projects:
    print(f"\nFound {len(unranked_projects)} projects in pto that no one ranked in spr:")
    for pid in unranked_projects:
        print(f"Project ID: {pid}, Mentor ID: {pto_project_to_mentor[pid]}")
else:
    print("All projects in pto are ranked by at least one student in spr.")

if duplicate_projects:
    print(f"\nFound {len(duplicate_projects)} duplicate project IDs in pto:")
    for pid in duplicate_projects:
        print(f"Project ID: {pid}, Mentor ID: {pto_project_to_mentor[pid]}, Count: {pto_project_counts[pid]}")
else:
    print("No duplicate project IDs found in pto.")

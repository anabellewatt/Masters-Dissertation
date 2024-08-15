import json

# Load the JSON file
with open('output.json', 'r') as json_file:
    data = json.load(json_file)

# Extract data
spr = data.get('spr', [])
tl = data.get('tl', [])
pto = data.get('pto', [])
gp = data.get('gp', [])

# Extract unique project IDs and mentor IDs
spr_pids = set(item['pid'] for item in spr)
pto_pids = set(item['pid'] for item in pto)
tl_mids = set(item['mid'] for item in tl)
pto_mids = set(item['mid'] for item in pto)

# Check for missing projects in pto
missing_pids = spr_pids - pto_pids
if missing_pids:
    print(f"Missing project IDs in pto: {missing_pids}")

# Check for missing mentors in tl
missing_mids = pto_mids - tl_mids
if missing_mids:
    print(f"Missing mentor IDs in tl: {missing_mids}")

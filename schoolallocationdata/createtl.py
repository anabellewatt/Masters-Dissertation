import csv
# Initialize list to hold the data
data = []

# Read the text file
with open('schoolallocationdata/student_rankings.txt', 'r') as file:
    lines = file.readlines()

current_sid = None

for line in lines:
    line = line.strip()
    if line.startswith("Student ID:"):
        current_sid = line.split(":")[1].strip()
    elif line.startswith("Project ID:"):
        parts = line.split(',')
        pid = parts[0].split(":")[1].strip()
        rank = parts[1].split(":")[1].strip()
        data.append({'sid': current_sid, 'pid': pid, 'rank': rank})

# Write to CSV file
with open('output.csv', 'w', newline='') as csvfile:
    fieldnames = ['sid', 'pid', 'rank']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in data:
        writer.writerow(row)

print("Data has been written to output.csv")

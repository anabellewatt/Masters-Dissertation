import csv

input_file_path = 'schoolallocationdata/person_role-ug4-s8.txt'
output_file_path = 'roles.csv'

# Read the text file and process it
with open(input_file_path, 'r') as infile:
    lines = infile.readlines()

# Open the output CSV file
with open(output_file_path, 'w', newline='') as outfile:
    writer = csv.writer(outfile)

    # Process each line
    header_found = False
    for line in lines:
        # Remove unwanted characters and whitespace
        line = line.strip()
        if '|' in line:
            # Skip the header and separator lines
            if '-----------' in line:
                continue
            if not header_found:
                header = [col.strip() for col in line.split('|')]
                writer.writerow(header)
                header_found = True
            else:
                row = [col.strip() for col in line.split('|')]
                writer.writerow(row)

print(f"CSV file created at {output_file_path}")

import csv

# Function to parse the text data
def parse_text_to_csv(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Extract the header and data rows
    header = ["project_id", "tenant_id", "academic_session_id", "person_id", "state", "interest_type", "register_timestamp"]
    data_rows = []

    for line in lines:
        if line.startswith('-------'):
            continue
        columns = line.split('|')
        if len(columns) == 7:
            # Remove leading/trailing whitespaces
            row = [col.strip() for col in columns]
            data_rows.append(row)
    
    # Write to CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(data_rows)

    print(f"Data has been successfully written to {output_file}")

# Input and output file paths
input_file = './18-19/project_staff-ug4-s6.txt'
output_file = 'supervisorproject18-19.csv'

# Parse the text file and create a CSV file
parse_text_to_csv(input_file, output_file)

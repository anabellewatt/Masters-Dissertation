import re
import csv

def parse_student_data(file_path, output_csv):
    student_data = []

    # Regular expression to match each line of the data
    line_pattern = re.compile(
        r'\s*(\d+)\s*\|\s*'  # project_id
        r'\w+\s*\|\s*'       # tenant_id
        r'\d+\s*\|\s*'       # academic_session_id
        r'(\d+)\s*\|\s*'     # person_id
        r'(\d+)\s*\|'        # rank
    )

    with open(file_path, 'r') as file:
        for line in file:
            match = line_pattern.match(line)
            if match:
                project_id = match.group(1)
                person_id = match.group(2)
                rank = match.group(3)
                student_data.append((project_id, person_id, rank))

    # Write the extracted data to a CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Project ID', 'Student ID', 'Rank'])  # Write header
        csvwriter.writerows(student_data)

# Example usage:
file_path = './18-19/project_students-ug4-s6.txt'
output_csv = 'student_data18-19.csv'
parse_student_data(file_path, output_csv)

print(f'Data has been successfully written to {output_csv}')

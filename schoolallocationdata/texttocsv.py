import re
import csv

def clean_text(text):
    # Replace problematic character sequences with their correct equivalents
    text = text.replace('â€™', "'").replace('â€œ', '"').replace('â€', '"').replace('â€“', '–').replace('â€”', '—')
    text = text.replace('Â', '')  # Remove unnecessary characters
    return text

def clean_and_parse(file_path):
    cleaned_data = []
    
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        for line in file:
            line = clean_text(line)
            
            # Split the line by '|' character
            parts = [part.strip() for part in line.split('|')]
            
            # Ensure we have exactly 14 parts (even if some are blank)
            parts += [''] * (14 - len(parts))
            
            if len(parts) == 14:
                row = {
                    'id': clean_text(parts[0]),
                    'title': clean_text(parts[1]),
                    'tenant_id': clean_text(parts[2]),
                    'owner_person_id': clean_text(parts[3]),
                    'creation_timestamp': clean_text(parts[4]),
                    'state': clean_text(parts[5]),
                    'description': clean_text(parts[6]),  # HTML tags are preserved
                    'goal': clean_text(parts[7]),
                    'max_students': clean_text(parts[8]),
                    'difficulty': clean_text(parts[9]),
                    'completion_criteria': clean_text(parts[10]),
                    'academic_session_id': clean_text(parts[11]),
                    'project_type': clean_text(parts[12]),
                    'tag_asg': clean_text(parts[13])
                }
                
                cleaned_data.append(row)
    
    return cleaned_data

# Usage
file_path = "./schoolallocationdata/18-19/projects-ug4-s6.txt"
cleaned_data = clean_and_parse(file_path)

# Write to CSV
output_file = 'projects_data18-19.csv'
fieldnames = ['id', 'title', 'tenant_id', 'owner_person_id', 'creation_timestamp', 'state', 
              'description', 'goal', 'max_students', 'difficulty', 'completion_criteria', 
              'academic_session_id', 'project_type', 'tag_asg']

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
    writer.writeheader()
    for row in cleaned_data:
        writer.writerow(row)

print(f"Cleaned data has been written to {output_file}")

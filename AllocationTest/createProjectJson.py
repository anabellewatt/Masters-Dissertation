import pandas as pd
import json

def transform_project_data(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Extract the relevant columns and transform the data
    project_data = []
    for _, row in df.iterrows():
        project_data.append({
            "pid": int(row['id']),
            "mid": int(row['owner_person_id']),
            "inst": int(row['max_students'])

        })
    
    # Write the transformed data to a JSON file
    with open(output_file, 'w') as file:
        json.dump(project_data, file, indent=4)
    print(f"Project data saved to {output_file}")

def main():
    # Define input and output files
    input_file = 'cleaned.csv'  # Replace with the path to your CSV file
    output_file = 'schoolprojects.json'
    
    # Transform the project data and save to JSON
    transform_project_data(input_file, output_file)

if __name__ == "__main__":
    main()

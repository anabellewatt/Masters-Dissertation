import pandas as pd
import json

def calculate_supervisor_load(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Create a dictionary to store the supervisor load
    supervisor_load = {}
    
    for _, row in df.iterrows():
        supervisor_id = int(row['owner_person_id'])
        capacity = int(row['max_students'])
        
        if supervisor_id in supervisor_load:
            supervisor_load[supervisor_id] += capacity
        else:
            supervisor_load[supervisor_id] = capacity
    
    # Create a list of dictionaries with supervisor load data
    supervisor_data = []
    for supervisor_id, load in supervisor_load.items():
        max_load = min(load, 7)  # Max load is the minimum of actual load or 10
        supervisor_data.append({
            "mid": supervisor_id,
            "load": max_load
        })
    
    # Write the supervisor load data to a JSON file
    with open(output_file, 'w') as file:
        json.dump(supervisor_data, file, indent=4)
    print(f"Supervisor load data saved to {output_file}")

def main():
    # Define input and output files
    input_file = 'cleaned.csv'  # Replace with the path to your CSV file
    output_file = 'schoolsupervisor.json'
    
    # Calculate the supervisor load and save to JSON
    calculate_supervisor_load(input_file, output_file)

if __name__ == "__main__":
    main()

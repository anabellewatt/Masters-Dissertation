import json
import random
import os

def load_student_rankings(file_path):
    """Load student rankings from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        # Ensure the data format is correct
        if not isinstance(data, list) or not data or data[0] != "rank":
            print(f"Error: The file '{file_path}' does not contain the expected format.")
            return []
        return data[1:]  # Skip the "rank" key
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' could not be parsed.")
        return []
    
def generate_rank(student_rankings):
    ranked_data =[]
    for entry in student_rankings:
        sid = entry['sid']
        pid = entry['pid']
        rank = entry['rank']
        ranked_data.append({"sid": sid, "pid": pid, "rank": rank+1})
    return ranked_data

def generate_scores(student_rankings):
    """Generate scores for each project ranking based on the rank."""
    scored_data = []
    current_student_id = None
    previous_score = None

    for entry in student_rankings:
        sid = entry['sid']
        pid = entry['pid']
        rank = entry['rank']
        
        if sid != current_student_id:
            current_student_id = sid
            previous_score = 10  # Starting score for the first ranked project

        # Determine the score range and variability
        max_score = previous_score
        min_score = max(1, previous_score - 3)
        score = random.randint(min_score, max_score)

        # Update previous_score to ensure it decreases or stays the same
        previous_score = score

        scored_data.append({"sid": sid, "pid": pid, "rank": rank+1, "score": score})

    return scored_data

def assign_groups(student_rankings):
    """Assign groups based on ranking, considering the number of rankings."""
    grouped_data = []
    student_projects = {}

    for entry in student_rankings:
        sid = entry['sid']
        pid = entry['pid']
        rank = entry['rank']
        
        if sid not in student_projects:
            student_projects[sid] = []

        # Store the project with its rank for later processing
        student_projects[sid].append(entry)

    for sid, projects in student_projects.items():
        total_projects = len(projects)
        # Calculate the number of projects for each group
        num_group_a = max(1, total_projects // 3)
        num_group_b = max(1, (total_projects - num_group_a) // 2)
        num_group_c = total_projects - num_group_a - num_group_b

        # Sort projects by rank
        projects_sorted = sorted(projects, key=lambda x: x['rank'])

        for i, project in enumerate(projects_sorted):
            pid = project['pid']
            rank = project['rank']

            if i < num_group_a:
                group = "A"
            elif i < num_group_a + num_group_b:
                group = "B"
            else:
                group = "C"

            grouped_data.append({"sid": sid, "pid": pid, "group": group})

    return grouped_data

def assign_yes_no(student_rankings):
    """Assign 'Yes' or 'No' check based on ranking, considering the number of rankings."""
    yes_no_data = []
    student_projects = {}

    for entry in student_rankings:
        sid = entry['sid']
        pid = entry['pid']
        rank = entry['rank']
        
        if sid not in student_projects:
            student_projects[sid] = []

        # Store the project with its rank for later processing
        student_projects[sid].append(entry)

    for sid, projects in student_projects.items():
        total_projects = len(projects)
        # Sort projects by rank
        projects_sorted = sorted(projects, key=lambda x: x['rank'])

        # Determine the thresholds for 'Yes' and 'No'
        # For simplicity, we divide the projects into three parts: A, B, and C
        num_group_a = max(1, total_projects // 3)
        num_group_b = max(1, (total_projects - num_group_a) // 2)

        for i, project in enumerate(projects_sorted):
            pid = project['pid']
            rank = project['rank']

            if i == total_projects - 1:
                check = "No"  # Ensure the last-ranked project is 'No'
            else:
                # Assign 'Yes' or 'No' based on project rank
                if i < num_group_a:
                    check = "Yes"  # Top third
                elif i < num_group_a + num_group_b:
                    check = "Yes" if random.random() < 0.5 else "No"  # Middle third with some randomness
                else:
                    check = "No"  # Bottom third

            yes_no_data.append({"sid": sid, "pid": pid, "check": check})

    return yes_no_data

def main():
    ranking_file = '20-21data/20_21_rank.json'  # Path to the input JSON fil

    # Load student ranking data
    student_rankings = load_student_rankings(ranking_file)

    if not student_rankings:
        print("No data to process.")
        return

    ranked_data = generate_rank(student_rankings)
    # Generate scored data
    scored_data = generate_scores(student_rankings)

    # Assign groups
    grouped_data = assign_groups(student_rankings)

    # Assign Yes/No checks
    yes_no_data = assign_yes_no(student_rankings)

    with open('ranked_data_20_21.json', 'w') as f:
        json.dump(ranked_data, f, indent=4)
    # Save the data to JSON files
    with open('scored_data_20_21.json', 'w') as f:
        json.dump(scored_data, f, indent=4)

    with open('grouped_data_20_21.json','w') as f:
        json.dump(grouped_data, f, indent=4)

    with open('yes_no_data_20_21.json', 'w') as f:
        json.dump(yes_no_data, f, indent=4)

    print(f"Data processing complete. Files saved to Input Json'.")

if __name__ == "__main__":
    main()

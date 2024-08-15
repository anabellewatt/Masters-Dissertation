import pandas as pd
import random
import json

def load_projects_from_csv(csv_file):
    try:
        df = pd.read_csv(csv_file)
        return df['pid'].tolist()  # Return a list of project IDs
    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' was not found.")
        return []
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{csv_file}' is empty.")
        return []
    except pd.errors.ParserError:
        print(f"Error: The file '{csv_file}' could not be parsed.")
        return []

def sample_projects(project_ids, num_samples):
    if len(project_ids) <= num_samples:
        return project_ids  # Return all if there are fewer projects than requested samples
    return random.sample(project_ids, num_samples)  # Sample without replacement

def generate_student_data(student_rankings):
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

def generate_student_yes_no_data(student_rankings):
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

            yes_no_data.append({"sid": sid, "pid": pid, "rank": rank, "check": check})

    return yes_no_data

def generate_student_ranked_data(num_students, sampled_project_ids, projects_per_student=10):
    data = []
    data2 = []

    for student_id in range(1, num_students + 1):
        # Each student selects 10 projects from the sampled 100
        desired_projects = random.sample(sampled_project_ids, projects_per_student)
        ranked_projects = random.sample(desired_projects, len(desired_projects))  # Shuffle for random ranking
        for rank, project_id in enumerate(ranked_projects, start=1):
            entry = {
                "sid": student_id,
                "pid": project_id,
                "rank": rank
            }
            #generate data for the school allocation since they do it based on 0-4
            entry2 = {
                "sid": student_id,
                "pid": project_id,
                "rank": rank -1
            }
            data.append(entry)
            data2.append(entry2)

    return data, data2

def add_scores_to_ranked_data(ranked_data):
    """Generate scores for each project ranking based on the rank."""
    scored_data = []
    current_student_id = None
    previous_score = None

    for entry in ranked_data:
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

        scored_data.append({"sid": sid, "pid": pid, "rank": rank, "score": score})

    return scored_data

def main():
    project_csv_file = 'project-ids.csv'  # Path to your CSV file
    num_students = 100  # Number of students
    num_sampled_projects = 100  # Fixed number of projects to sample from CSV
    projects_per_student = 5 # Number of projects each student desires

    # Load project IDs from CSV file
    project_ids = load_projects_from_csv(project_csv_file)

    if not project_ids:
        print("No projects to generate data for.")
        return

    # Sample a fixed subset of projects to be available to all students
    sampled_project_ids = sample_projects(project_ids, num_sampled_projects)

    # Generate data
   

    student_ranked_data, student_ranked_data2 = generate_student_ranked_data(num_students, sampled_project_ids, projects_per_student)
    student_ranked_data_with_scores = add_scores_to_ranked_data(student_ranked_data)
    student_data = generate_student_data(student_ranked_data)

    student_yes_no_data = generate_student_yes_no_data(student_ranked_data)

    # Save the ranked data with scores to a JSON file
    with open('generated_scores_data3.json', 'w') as f:
        json.dump(student_ranked_data_with_scores, f, indent=4)
    
    with open('generated_rank2_data3.json', 'w') as f:
        json.dump(student_ranked_data2, f, indent=4)

    # Save to a JSON file
    with open('generated_group_data3.json', 'w') as f:
        json.dump(student_data, f, indent=4)

    with open('generated_check_data3.json', 'w') as f:
        json.dump(student_yes_no_data, f, indent=4)
    
    with open('generated_ranked_data3.json', 'w') as f:
        json.dump(student_ranked_data, f, indent=4)

    print(f"Generated {len(student_data)} records with {len(sampled_project_ids)} projects sampled and saved to 'generated_student_data.json'")

if __name__ == "__main__":
    main()

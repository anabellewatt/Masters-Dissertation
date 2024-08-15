import json

# Function to read JSON data from a file
def read_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Function to calculate the optimal welfare, social welfare, distortion, and percentage of students assigned to "Yes" projects
def calculate_metrics_with_check(preferences_file, output_file):
    # Load the data
    preferences = read_json(preferences_file)
    output = read_json(output_file)

    # Create a dictionary to look up project "Yes"/"No" check
    # {sid: {pid: {'check': check}}}
    pref_dict = {}

    for pref in preferences:
        sid = pref['sid']
        pid = pref['pid']
        check = pref['check']

        if sid not in pref_dict:
            pref_dict[sid] = {}
        pref_dict[sid][pid] = {'check': check}

    # Calculate optimal welfare and social welfare
    optimal_welfare = 0
    social_welfare = 0
    total_students = len(pref_dict)
    top_choice_count = 0
    assigned_yes_projects = 0

    optimal_welfare = total_students

    for alloc in output:
        sid = alloc['sid']
        pid = alloc['pid']
        # Find the check status of the assigned project
        assigned_check = pref_dict[sid].get(pid, {}).get('check', 'No')

        # Calculate social welfare as the number of "Yes" projects assigned
        if assigned_check == "Yes":
            social_welfare += 1

        # Check if the assigned project is a "Yes" project for the student
        if assigned_check == "Yes":
            assigned_yes_projects += 1

    # Calculate distortion as the ratio of optimal welfare to social welfare
    if social_welfare != 0:
        distortion = optimal_welfare / social_welfare
    else:
        distortion = float('inf')  # or some appropriate value like `None` or an error message

    # Calculate percentage of students assigned to "Yes" projects
    if total_students > 0:
        yes_percentage = (assigned_yes_projects / total_students) * 100
    else:
        yes_percentage = 0  # Handle edge case if no students

    return {
        'optimal_welfare': optimal_welfare,
        'social_welfare': social_welfare,
        'distortion': distortion,
        'yes_percentage': yes_percentage
    }

# Example usage
preferences_file = './Input_Json/yes_no_data_18_19.json'
output_file = './results/allocation_check_results18-19.json'
metrics = calculate_metrics_with_check(preferences_file, output_file)

print("Optimal Welfare:", metrics['optimal_welfare'])
print("Social Welfare:", metrics['social_welfare'])
print("Distortion:", metrics['distortion'])
print("Percentage of Students Assigned to 'Yes' Projects:", metrics['yes_percentage'], "%")

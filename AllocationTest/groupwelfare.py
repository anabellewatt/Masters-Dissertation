import json

# Function to read JSON data from a file
def read_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Function to calculate the optimal welfare, social welfare, distortion, and % of top choice including groups
def calculate_metrics_with_groups(preferences_file, output_file):
    # Load the data
    preferences = read_json(preferences_file)
    output = read_json(output_file)

    # Group rankings
    group_ranks = {"A": 1, "B": 2, "C": 3}

    # Create a dictionary of preferences for easier lookup
    # {sid: {pid: {'group': group, 'group_rank': group_rank}}}
    pref_dict = {}

    for pref in preferences:
        sid = pref['sid']
        pid = pref['pid']
        group = pref['group']
        group_rank = group_ranks[group]

        if sid not in pref_dict:
            pref_dict[sid] = {}
        pref_dict[sid][pid] = {'group': group, 'group_rank': group_rank}

    # Calculate optimal welfare and top choice counts
    optimal_welfare = 0
    total_students = len(pref_dict)
    top_choice_count = 0
    top_group_count = 0

    for sid, prefs in pref_dict.items():
        # Top choice is the one with the highest group priority (lowest group_rank number)
        top_choice_group_rank = min(prefs[pid]['group_rank'] for pid in prefs)
        optimal_welfare += top_choice_group_rank

    # Calculate social welfare
    social_welfare = 0

    for alloc in output:
        sid = alloc['sid']
        pid = alloc['pid']

        if sid in pref_dict and pid in pref_dict[sid]:
            assigned_group_rank = pref_dict[sid][pid]['group_rank']
            social_welfare += assigned_group_rank

            # Check if it's the top choice (best group rank)
            if assigned_group_rank == min(pref_dict[sid][p]['group_rank'] for p in pref_dict[sid]):
                top_choice_count += 1
            
            # Check if the assigned project is in Group A
            if pref_dict[sid][pid]['group'] == 'A':
                top_group_count += 1
    actual = social_welfare - optimal_welfare
    social_welfare = optimal_welfare-actual
    # Calculate distortion as the ratio of optimal welfare to social welfare
    if social_welfare != 0:
        distortion = optimal_welfare / social_welfare
    else:
        distortion = float('inf')  # or some appropriate value like `None` or an error message

    # Calculate percentage of students who got their top choice (best group) or were assigned to Group A
    top_choice_percentage = (top_choice_count / total_students) * 100
    top_group_percentage = (top_group_count / total_students) * 100

    return {
        'optimal_welfare': optimal_welfare,
        'social_welfare': social_welfare,
        'distortion': distortion,
        'top_choice_percentage': top_choice_percentage,
        'top_group_percentage': top_group_percentage
    }

# Example usage
preferences_file = './Input_Json/grouped_data_20_21.json'
output_file = 'allocation_group_results20-21.json'
metrics = calculate_metrics_with_groups(preferences_file, output_file)

print("Optimal Welfare:", metrics['optimal_welfare'])
print("Social Welfare:", metrics['social_welfare'])
print("Distortion:", metrics['distortion'])
print("Percentage of Students Who Got Their Top Choice:", metrics['top_choice_percentage'], "%")
print("Percentage of Students Assigned to Group A:", metrics['top_group_percentage'], "%")

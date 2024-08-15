import json

# Function to read JSON data from a file
def read_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Function to calculate optimal welfare, social welfare, and distortion
def calculate_metrics_with_ranks(preferences_file, output_file):
    # Load the data
    preferences = read_json(preferences_file)
    output = read_json(output_file)

    # Create a dictionary to look up project ranks
    # {sid: {pid: {'rank': rank}}}
    pref_dict = {}

    for pref in preferences:
        sid = pref['sid']
        pid = pref['pid']
        rank = pref['rank']

        if sid not in pref_dict:
            pref_dict[sid] = {}
        pref_dict[sid][pid] = {'rank': rank}

    # Calculate optimal welfare and social welfare
    optimal_welfare = 0
    social_welfare = 0
    total_students = len(pref_dict)
    top_choice_count = 0

    # Compute optimal welfare: Sum of the best (lowest rank) project each student could ideally get
    optimal_welfare = total_students

    # Compute social welfare: Use the rank directly
    for alloc in output:
        sid = alloc['sid']
        pid = alloc['pid']
        # Find the rank of the assigned project
        assigned_rank = pref_dict[sid].get(pid, {}).get('rank', float('inf'))
        social_welfare += assigned_rank

        # Check if the assigned project is the top choice (lowest rank number)
        if assigned_rank == min(pref_dict[sid][p]['rank'] for p in pref_dict[sid]):
            top_choice_count += 1

    actual = social_welfare - optimal_welfare 
    social_welfare = optimal_welfare-actual
    # Calculate distortion as the ratio of optimal welfare to social welfare
    if social_welfare != 0:
        distortion = optimal_welfare / social_welfare
    else:
        distortion = float('inf')  # or some appropriate value like `None` or an error message

    # Calculate percentage of students who got their top choice
    top_choice_percentage = (top_choice_count / total_students) * 100

    return {
        'optimal_welfare': optimal_welfare,
        'social_welfare': social_welfare,
        'distortion': distortion,
        'top_choice_percentage': top_choice_percentage
    }
# Example usage
preferences_file = './Input_Json/ranked_data_18_19.json'
output_file = 'allocation_rank_results18-19.json'
metrics = calculate_metrics_with_ranks(preferences_file, output_file)

print("Optimal Welfare:", metrics['optimal_welfare'])
print("Social Welfare:", metrics['social_welfare'])
print("Distortion:", metrics['distortion'])
print("Percentage of Students Who Got Their Top Choice:", metrics['top_choice_percentage'], "%")

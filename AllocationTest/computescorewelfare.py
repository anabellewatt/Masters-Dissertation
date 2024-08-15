import json

# Function to read JSON data from a file
def read_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Function to calculate the optimal welfare, social welfare, distortion, and % of top choice
def calculate_metrics_with_weights(preferences_file, output_file):
    # Load the data
    preferences = read_json(preferences_file)
    output = read_json(output_file)

    # Create a dictionary of preferences for easier lookup
    # {sid: {pid: {'rank': rank, 'score': score, 'weight': weight}}}
    pref_dict = {}
    max_rank = max(pref['rank'] for pref in preferences)

    for pref in preferences:
        sid = pref['sid']
        pid = pref['pid']
        rank = pref['rank']
        score = pref['score']
        inverted_rank = max_rank + 1 - rank
        weight = score + inverted_rank

        if sid not in pref_dict:
            pref_dict[sid] = {}
        pref_dict[sid][pid] = {'rank': rank, 'score': score, 'weight': weight}

    # Calculate optimal welfare and top choice counts
    optimal_welfare = 0
    total_students = len(pref_dict)
    top_choice_count = 0

    for sid, prefs in pref_dict.items():
        # Top choice is the one with the highest weight
        top_choice_weight = max(prefs[pid]['weight'] for pid in prefs)
        optimal_welfare += top_choice_weight

    # Calculate social welfare
    social_welfare = 0

    for alloc in output:
        sid = alloc['sid']
        pid = alloc['pid']
        assigned_weight = pref_dict[sid][pid]['weight']
        social_welfare += assigned_weight
        # Check if it's the top choice
        if assigned_weight == max(pref_dict[sid][p]['weight'] for p in pref_dict[sid]):
            top_choice_count += 1

    # Calculate distortion as the ratio of optimal welfare to social welfare
    # If social_welfare is zero, we should handle it to avoid division by zero
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
preferences_file = './Input_Json/scored_data_20_21.json'
output_file = 'allocation_score_results20-21.json'
metrics = calculate_metrics_with_weights(preferences_file, output_file)

print("Optimal Welfare:", metrics['optimal_welfare'])
print("Social Welfare:", metrics['social_welfare'])
print("Distortion:", metrics['distortion'])
print("Percentage of Students Who Got Their Top Choice:", metrics['top_choice_percentage'], "%")

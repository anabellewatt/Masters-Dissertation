import json
import csv

# Load original preference data for each elicitation device
# with open('./Input_Json/20_21_rank.json') as f:
#     original_ranked_data = json.load(f)

#with open('./Input_Json/generated_rank2_data.json') as f:
    #school_ranked_data = json.load(f)

# with open('./Input_Json/scored_data_20_21.json') as f:
#     original_scores_data = json.load(f)

with open('./Input_Json/grouped_data_20_21.json') as f:
    original_group_data = json.load(f)

# with open('./Input_Json/yes_no_data_20_21.json') as f:
#     original_check_data = json.load(f)

# Load results data for each elicitation device
# with open('allocation_rank_results.json') as f:
#     results_ranked_data = json.load(f)

#with open('school_rank_result.json') as f:
    #school_ranked_results = json.load(f)

# with open('allocation_score_results.json') as f:
#     results_scores_data = json.load(f)

with open('allocation_group_results.json') as f:
    results_group_data = json.load(f)

# with open('allocation_check_results.json') as f:
#     results_check_data = json.load(f)

def create_summary(original_data, results_data, key_name):
    original_dict = {(entry['sid'], entry['pid']): entry for entry in original_data if isinstance(entry, dict)}
    
    results_dict = {(entry['student'], entry['project']): entry for entry in results_data if isinstance(entry, dict)}
    
    # Summarize comparison
    summary = []
    for (student, project), original_entry in original_dict.items():
        result_entry = results_dict.get((student, project))
        summary.append({
            'student': student,
            'project': project,
            'original_value': original_entry.get(key_name) if original_entry else None,
            'result_value': result_entry.get('project') if result_entry else None
        })
    
    return summary

def write_summary_to_csv(summary, filename, key_field):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['sid', 'pid', 'original', 'result']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for entry in summary:
            writer.writerow({
                'sid': entry['student'],
                'pid': entry['project'],
                'original': entry['original_value'],
                'result': entry['result_value'],
            })

# Create summaries for each elicitation device
#ranked_summary = create_summary(original_ranked_data, results_ranked_data, 'rank')
#school_summary = create_summary(school_ranked_data,school_ranked_results, 'rank')
#score_summary = create_summary(original_scores_data, results_scores_data, 'rank')
group_summary = create_summary(original_group_data, results_group_data, 'group')
#yes_no_summary = create_summary(original_check_data, results_check_data, 'check')

# Write summaries to CSV files
#write_summary_to_csv(ranked_summary, 'ranked_summary.csv', 'rank')
#write_summary_to_csv(school_summary, 'school_summary.csv', 'rank')
#write_summary_to_csv(score_summary, 'score_summary.csv', 'rank')
write_summary_to_csv(group_summary, 'group_summary.csv', 'group')
#write_summary_to_csv(yes_no_summary, 'yes_no_summary.csv', 'check')

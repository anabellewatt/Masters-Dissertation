import json
import pandas as pd
from pulp import LpProblem, LpVariable, LpMaximize, LpBinary, lpSum, value, LpStatus

#allocation algorithm to test different elicitation devices
#Linear Programming because gale-shapely doesnt work with weights
#Doesnt account for self proposed project
#To handle input from student survey to see which elicitation device is better
#Will need project.json, supervisor.json to give project capacity, supervisor capacity, and which supervisor is assigned to which project

from ProcessJson import process_data

def processfiles(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)

    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
        return None

    except json.JSONDecodeError:
        print(f"Error: The file '{file_name}' is not a valid JSON file.")
        return None
    
    return data


def convert_to_int(results):
    # Convert numpy types to native Python types
    if isinstance(results, dict):
        return {key: convert_to_int(value) for key, value in results.items()}
    elif isinstance(results, list):
        return [convert_to_int(item) for item in results]
    elif isinstance(results, (int, float, str)):
        return results
    elif hasattr(results, 'item'):
        return results.item()  # Convert numpy types
    return results



def allocationAlgorithm(elicitation, df):
    #load the mentor and projects data files, change as needed
    #CHECK THESE FILES FOR THE CORRECT YEAR!
    supervisor_df = processfiles("supervisor20_21.json")
    projects_df = processfiles("projects20_21.json")

    #check files for no input
    if supervisor_df is None:
        print(f"Error with mentor_df being None: {supervisor_df}")
        return None
        
    elif projects_df is None:
        print(f"Error with projects_df being None: {projects_df}")
        return None
    
    #change mentor and projects to Dataframe to use in lp algorithm
    supervisor_df = pd.DataFrame(supervisor_df)
    projects_df = pd.DataFrame(projects_df)

    prob = LpProblem("Project Allocation: ", LpMaximize) 
    
    #get students
    sid = df['sid'].unique()
    count = len(sid)

    #get projects
    pid = df['pid'].unique()

    #decision variables x[i][j] == 1 if student i is allocated project j
    x = LpVariable.dicts("Allocate", (sid,pid), cat=LpBinary)

    #Objective function based on elicitation device
    if elicitation == 'rank':
        prob += lpSum(
            (1 / df.loc[(df['sid'] == i) & (df['pid'] == j), 'rank'].fillna(float('inf')).values[0]) * x[i][j]
            for i in sid for j in pid
            if not df.loc[(df['sid'] == i) & (df['pid'] == j)].empty
        ), "Total_Rank"

    elif elicitation == 'score':
        prob += lpSum(
            df.loc[(df['sid'] == i) & (df['pid'] == j), 'weight'].fillna(0).values[0] * x[i][j]
            for i in sid for j in pid
            if not df.loc[(df['sid'] == i) & (df['pid'] == j)].empty
        ), "Total_Score"

    elif elicitation == 'group':
        group_weight = {"A": 3, "B": 2, "C": 1}
        prob += lpSum(
            group_weight.get(df.loc[(df['sid'] == i) & (df['pid'] == j), 'group'].values[0], 0) * x[i][j]
            for i in sid for j in pid
            if not df.loc[(df['sid'] == i) & (df['pid'] == j)].empty
        ), "Total_Group"

    elif elicitation == 'check':
        prob += lpSum(
            # Handling empty DataFrame cases
            df.loc[(df['sid'] == i) & (df['pid'] == j), 'check'].fillna(0).values[0] * x[i][j]
            for i in sid for j in pid
            if not df.loc[(df['sid'] == i) & (df['pid'] == j)].empty
        ), "Total_Check"


    #Constraints
    #Student Constraints, each student is given one project
    # Constraints
    for i in sid:
        prob += lpSum(x[i][j] for j in pid) == 1, f"Student_{i}_Allocation"

    for j in pid:
        project_capacity = projects_df[projects_df['pid'] == j]['capacity']
        if not project_capacity.empty:
            prob += lpSum(x[i][j] for i in sid) <= project_capacity.values[0], f"Project_{j}_Capacity"
        else:
            print(f"Warning: Project {j} not found in the project data.")

    for supervisor in supervisor_df['supervisor_id']:
        assigned_projects = projects_df[projects_df['supervisor_id'] == supervisor]['pid']
        max_load = supervisor_df[supervisor_df['supervisor_id'] == supervisor]['max_load']
        
        # Debugging output
        print(f"Supervisor {supervisor} has max load {max_load.values[0]} and handles projects {assigned_projects.tolist()}")
        
        if not max_load.empty:
            if not assigned_projects.empty:
                # Ensure all projects in assigned_projects are included in x
                prob += lpSum(x[i][j] for i in sid for j in assigned_projects if j in pid) <= max_load.values[0], f"Supervisor_{supervisor}_Capacity"
            else:
                print(f"Warning: Supervisor {supervisor} has no assigned projects.")
        else:
            print(f"Warning: Supervisor {supervisor} not found in the Supervisor data.")
    
    # if elicitation == 'score':
    #     zero_weight_df = df[df['weight'] == 0]
    #     for student in zero_weight_df['sid'].unique():
    #         student_projects = zero_weight_df[zero_weight_df['sid'] == student]['pid'].tolist()
    #         prob += lpSum(x[student][project] for project in student_projects) >= 1, f"Ensure_Student_{student}_Gets_Zero_Weight_Project"

    prob.solve()

    results = []

    prob.writeLP("allocation_model.lp")
    print(f"Status: {LpStatus[prob.status]}")

    for i in sid:
        for j in pid:
            if value(x[i][j]) == 1:
                supervisor_id = projects_df[projects_df['pid'] == j]['supervisor_id'].values[0]
                print(f"Student {i} is allocated to Project {j} with Supervisor {supervisor_id}")
                #mid is supervisor and sid is student id
                results.append({
                    "sid": i,
                    "pid": j,
                    "mid": supervisor_id
                })

    
    results = convert_to_int(results)
    print(count)
    return results


def main():
     
    file_name = input("Enter the name of the allocation file(JSON): ")

    elicitation, df = process_data(file_name)

    if df is not None:
        result = allocationAlgorithm(elicitation, df)
    else:
        print(f"Error: df is none from process_data from allocation file {file_name}")
        return
    
    if elicitation == 'rank':
        with open('results/allocation_rank_results.json', 'w') as f:
            json.dump(result, f, indent=4)
        print(f"Results written to allocation_rank_results.json")

    elif elicitation == 'score':
        with open('results/allocation_score_results1.json', 'w') as f:
            json.dump(result, f, indent=4)
        print(f"Results written to allocation_score_results.json")

    elif elicitation == 'group':
        with open('results/allocation_group_results1.json', 'w') as f:
            json.dump(result, f, indent=4)
        print(f"Results written to allocation_group_results.json")

    elif elicitation == 'check':
        with open('results/allocation_check_results1.json', 'w') as f:
            json.dump(result, f, indent=4)
        print(f"Results written to allocation_check_results.json")


if __name__=="__main__":
     main()
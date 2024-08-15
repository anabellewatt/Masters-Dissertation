#Process the input from survey:
import json
import pandas as pd

def process_data(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)

    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
        return

    except json.JSONDecodeError:
        print(f"Error: The file '{file_name}' is not a valid JSON file.")
        return
    
    elicitation = data[0]
    df = pd.DataFrame(data[1:])

    print(f"Elicitation Device: {elicitation}")
    print(f"Data: {data[1:]}")

    #Convert rankings to 1-20
    if elicitation == 'rank':
        df_sorted = df.sort_values(by=['rank']).reset_index(drop=True)
        

    #convert score and ranking to weight
    elif elicitation == 'score':
        max_rank = df['rank'].max()
        df['inverted_rank'] = max_rank + 1 - df['rank']
        df['weight'] = df['score'] + df['inverted_rank']
        df_sorted = df.sort_values(by=['weight']).reset_index(drop=True)


    #convert groups to 1-3 and take out not qualifed group, and randomize projects in each group
    elif elicitation == 'group':
        group_priority = {"A":1, "B": 2, "C":3}

        df['group_priority'] = df['group'].map(group_priority).fillna(4)

        df = df[df['group_priority']<4]

        df_sorted = df.sort_values(by=['group_priority']).drop(columns=['group_priority'])



    #convert checks approved to 1 and take out no 
    elif elicitation == 'check':
        df_approved = df[df["check"] == "Yes"].copy()
        df_disapproved = df[df["check"] == "No"].copy()
    
        # Convert 'Yes' to 1
        if not df_approved.empty:
            df_approved['check'] = 1
        
        # Convert 'No' to 0
        if not df_disapproved.empty:
            df_disapproved['check'] = 0
        
        # Combine both approved and disapproved DataFrames
        df_sorted = pd.concat([df_approved, df_disapproved]).reset_index(drop=True)

    return elicitation, df_sorted


# file_name = input("Enter the name of the JSON file: ")
# elicitation, df = process_data(file_name)
# print(f"Elicitation Device: {elicitation}")
# print(f"Data: {df}")

# How Good is the Project Assignment? The Effect of Preference Information on the Quality of Assignment Outcomes.
# Belle Watt

This project investigates how preference aggregation protocols impact the allocation outcome. This project consisted of deploying an online survey platform, developing a simple
integer linear allocation program, data processing, and running tests on the allocated result from the school algorithm and the developed ILP. School algorithm was not allowed
to be included in this file, rules set by the school.

## Table of Contents
1. [Survey Implementation](#Survey)
2. [Integer Linear Program](#ILP)
3. [Data Processing](#Data)
4. [Allocation Tests](#AllocationTests)
5. [Fairness Criteria Input](#Fairness)
6. [Efficiency Data](#Efficiency)

## Survey

The implemented survey is in the folder labeled anabellewatt.github.io. You will need to download nodejs. You can run the Survey on a localhost with node server.js. For some reason the data is sent to the data folder in the folder SurveyWebsite so I have included that as well.

This website is still deployed on GitHub if you want to see what the pages look like https://anabellewatt.github.io . The code can also be found at 
https://github.com/anabellewatt/anabellewatt.github.io

The results from the survey are in the Student_Data file in the folder AllocationTest.

## ILP

The school has expressed I am not allowed to submit their code and algorithm with my code, so this will not be in this README file or in the project code.

The developed integer linear allocation program is in the AllocationTest folder. The file is called allocationAlgorithm.py. The file needed to process the JSON files called in this allocation algorithm is called ProcessJson.py. This can be ran by python3 allocationAlgorithm.py, and you will need a valid input json, as you will be asked for the input json running the allocation algorithm. 

Make sure before you run the input for the given year you have the correct supervisor and project json files for it to reference. These can be found in the (#Data) section below. If you don't have the correct Json files you will receive an error. 

The json needs to say the protocol at top as a string: "rank", "score", "group", "check", if you are getting an error saying "local variable 'df_sorted' referenced before assignment" this means you need to add the protocol string at the top of the file. The algorithm will put the results into a corresponding json file given the protocol: "rank", "score", "group", "check". The input jsons used in this research is in the folder Input_Json and the results are in the file results.

Input should look like: 
["check",
    {
        "sid": 4879,
        "pid": 2708,
        "check": "Yes"
    },
    {
        "sid": 4879,
        "pid": 2676,
        "check": "Yes"
    },...
]

Output will look like:
[
    {
        "sid": 4879,
        "pid": 2677,
        "mid": 3842
    },
    {
        "sid": 4929,
        "pid": 2754,
        "mid": 1335
    },...
]

Output files can be set in the main() function in allocationAlgorithm.py

## Data

The data collected from the school was 4 text files for each year. The projects text file includes the project information, the role file has the ids with wither supervisor, superviosr, or student associated to the id. The projects staff file includes details about which supervisor is assigned to which project. The students file includes which projects each students ranked and the ranking they gave for each project. There was a lot of data processing to generate the needed data for the allocation algorithms input jsons. All the necessary .csv files can be found in this project folder. But if you want to recreate them, the process can be found below.

Process to get Input from Survey Results:
    - These files have already been created in the folder AllocationTest/Input_Json/SurveyInput
    - the student feedback from the survey is in multiple files in the folder Student_Data in the folder AllocationTest
    - run the processSurveyResults.py file
    - the files will be outputed to the folder SurveyInput in the folder Input_Json as rank.json, score,json, group.json, check.json
    - the supervisor and supervisor files for this are the same for the year 2020-2021 jsons to use in the allocation.

Process to get the Project Capacity:
    - These files have already been created as projects18-19.json and projects20_21.json in AllocationTest.
    - To get the necessary data you will need to run texttocsv which goes through the project text file and creates a csv of this information.
    - From this you will need to run getprojectmentor.py which from the project_staff text file will create csv file with projects and the assigned supervisors.
    - Then you can run createpto to get the mentor project capacity csv file for the csvtojson.py file described below.

Process to get the Supervisor Capacity:
    - These files have already been created as supervisor18-19.json and supervisor20_21.json in AllocationTest 
    - From the above csv of project mentor you can run comparefiles.py to generate the supervisor summary csv file. I maxed out the max_load for supervisors at 10 but you can decide when to max this out. 
    - You then have the supervisor summary file for the csvtojson.py file decribed below.

Process to get the Student Rankings:
    - These have already been created in the AllocationTest/Input_Json file.
    - If you want to recreate this file, youll need access to the project_student text file.
    - By using the program gatherstudentranks.py you can create a csv file for student rankings of projects that will be used in csvtojson.py to create the entire file needed.

Process to get Input Jsons from Output.json:
    - After succesfully running csvtojson.py with all the files above you'll have an output.json file.
    - This file will contain an array labeled spr, you can copy the objects in that array and create a json file of ranking.json to use with generate_data_20_21.py mentioned below.
    - The next array will be called tl, you can copy the objects of that array and create a json file for supervisor loads for the program . You will need to change the names of "mid" to "supervisor_id" and "load" to  "max_load" in the json file to fit with my allocation algorithm. This tl was designed to fit the school allocation.
    - The next array will be called pto, you can copy the objects of that array and create a json file for projects capacity for the program. You will need to change the naemes of "mid" to "supervisor_id" and "inst" to "capacity". Again this csv to json was to run for the schools algorithm and thats why copy and paste is needed for mine.
    - After this youll have three files to use for the allocation algorithm. You will need to run the rankings.json file through generate_data_20_21.py mentioned below to create the best data for my program.

Process to Generate Data from Rankings:
    - These have already been created in the AllocationTest/Input_Json, the input file used is in the designated file for the specific year as the ranking.json.
    - If you want to recreate these you can use the program generate_data_20_21.py in AllocationTest/Input_Json file.
    - The input file will need to be the studentranking.json file you created above from the school data.
    - When running the allocation with this data make sure you use the new ranking file created as this shifts the rank from 0 to start with rank 1 as my program does not handle rank:0. It doesnt alter the data just shifts the ranks up by 1.

## AllocationTests

Each protocol has its own welfare calculator that will calculate the social welfare, optimal welfare, distortion and the total amount of students who didn't get their first choice of allocated project. 

    - For rank this is the computwelfare.py program in AllocationTest folder. 
    - For Score it is computescorewelfare.py program in AllocationTest folder. 
    - For group it is the groupwelfare.py in AllocationTest folder. 
    - For check it is the computecheckwelfare.py in AllocationTest folder. 

The reason to separate these is they all accept an input and output json file for each protocol. Make sure before running it that the input json does not have the string of the protocol at the top. Only need the string at the top for the ILP program. You can run each of these programs by python3 "" --replace "" with the name of the welfare calculator program. 

NOTE: Double check the input and output files. The input file should be the input file you used to get the output file. When using this to calculate the distortion for the school this output file is in the results folder. These are labeled as school results. You can use the rank input files as these are the same as the ones used for the school allocation program. I was not able to provide the code from the school, so unfortunately can't reproduce the results.

These will not output to a file. The information will be found in the terminal.

## Fairness

The input Jsons used to test for the Fairness criteria for each protocol is in the folder Fairness in the AllocationTest folder. Below describes what each input does and tests for, to determine which criteria it meets, you will need to analyze the output it provides. You can run these inputs on the developed ILP to determine the fairness criteria it meets.

Fairness for Rank: 
    - rank1.json is everyone has different preferences.
    - rank2.json everyone agrees on some ranks but not all ranks.
    - rank3.json everyone prefers project 4361 over project 4362.
    - rank4.json preference between Project 4361 and Project 4362 should remain consistent despite the ranking of other projects.
    - rank5.json the ranking should be transitive.

Fairness for Score: 
    - score1.json all students have different project preferences and scores.
    - score2.json share similar preferences and scores, but not all ranks and scores.
    - score3.json all students strongly prefer certain projects over others.
    - score4.json ranking between Project 4361 and Project 4362 should remain consistent regardless of the scores assigned to other projects.
    - score5.json score assignments should respect transitivity in preferences.

Fairness for Group:
    - group1.json students have varied preferences, covering all groups (A, B, C, D).
    - group2.json students have overlapping preferences, but not all groups.
    - group3.json students strongly prefer specific projects, and all others are less desired.
    - group4.json student preferences between two projects remain stable, regardless of other options.
    - group5.json preference ordering should respect transitivity.

Fairness for Check: 
    - check1.json students have varied preferences, covering all groups (Yes, No).
    - check2.json share similar preferences, but not all checks.
    - check3.json students strongly prefer specific projects, and all others are not desired.
    - check4.json student preferences between two projects remain stable, regardless of other options.
    - check5.json preference ordering should respect transitivity.

These will output to whatever file you have set for the output file but also it will be in the terminal.

## Efficiency

This data was collected from the times to complete each preference aggregation protocol from the Survey completed by student volunteers. These times and other survey feedback can be found in the StudentInterviewSummary.doc and also the Student_Data folder in the allocationTest folder with each student JSON file.
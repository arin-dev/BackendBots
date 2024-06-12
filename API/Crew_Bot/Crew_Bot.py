from typing import TypedDict, List, Annotated
from CrewGraph import CrewGraph
import sqlite3

class State(TypedDict):
    num_steps : int
    project_detail_from_customer : str
    detailed_desc : str
    roleJobTitles : List[str]
    crew_requirements : List[dict]
    queries : List[str]
    selected_crews : List[dict]

project_detail_from_customer = "A short film to be shot in Delhi with only 2 actors and 1 camera man and 1 director and 1 make up artist, no extra crew needed"


output = CrewGraph(State, project_detail_from_customer)

def get_crew_member_details(UserId, db):
    dbname = db.split('/')[-1].split('.')[0]
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(f"SELECT * FROM \'{dbname}\' WHERE UserId = \'{UserId}\'")
    raw_user_details = c.fetchall()
    conn.close()
    user_details = {
        "name": raw_user_details[0][0],
        "userid": raw_user_details[0][1],
        "crewType": raw_user_details[0][2],
        "roleJobTitle": raw_user_details[0][3],
        "services": raw_user_details[0][4].split(', '),
        "tags": raw_user_details[0][5].split(', '),
        "expertise": raw_user_details[0][6].split(', '),
        "yoe": raw_user_details[0][7],
        "minRatePerDay": raw_user_details[0][8],
        "maxRatePerDay": raw_user_details[0][9],
        "location": raw_user_details[0][10]
    }
    return user_details

print("WORKING ON FRONTEND PART FROM HERE:\n")
for crew in output:
    for role, details in crew.items():
        UserId = details['UserId']
        user_details = get_crew_member_details(UserId, './DEMO_DB/crewdata.db')
        details.update({'user_details': user_details})

print(output)
import json
with open('./Example_Output/output.json', 'w') as f:
    json.dump(output, f, indent=4)


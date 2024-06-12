import os
from dotenv import load_dotenv
import sqlite3
import json
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from crew.models import CrewMember, Project, CrewRequirement, SelectedCrew

from .apikey import OPENAI_API_KEY

# For LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0.2, api_key=OPENAI_API_KEY)
# For LLM that returns json
llm_json = ChatOpenAI(model="gpt-4o", temperature=0.2, api_key=OPENAI_API_KEY).bind(response_format={"type": "json_object"})


def get_detailed_desc(desc):
    prompt_detailed_desc = "You are the production advisor and primary contract for the customer. The customer will come to you and describe their project. You need to make the necessary changes so that project details are completely described and even new members can understand the need. It should be such that everyone can get the overview of the project at a glance. The description should try to contain the following in a paragraph : a descriptive overview of the project, locations that will be involved and task at each location, and whether the same team will travel to different locations or if customer will require different teams at different locations. No formatting should be applied to the output, for better clearity and understanding."
    messages = [
        ("system", prompt_detailed_desc),
        ("user", f"This is the project details from user : {desc}"),
    ]
    response = llm.invoke(messages)
    detailed_desc = response.content
    return detailed_desc


def filter_crew_members(roleJobTitle, location):
    raw_user_details = CrewMember.objects.filter(roleJobTitle=roleJobTitle, location=location)
    filtered_data = []
    for raw_user_detail in raw_user_details:
        filtered_data.append({
        "name": raw_user_detail.name,
        "userid": raw_user_detail.userid,
        "crewType": raw_user_detail.crewType,
        "roleJobTitle": raw_user_detail.roleJobTitle,
        "services": raw_user_detail.services.split(', '),
        "tags": raw_user_detail.tags.split(', '),
        "expertise": raw_user_detail.expertise.split(', '),
        "yoe": raw_user_detail.yoe,
        "minRatePerDay": raw_user_detail.minRatePerDay,
        "maxRatePerDay": raw_user_detail.maxRatePerDay,
        "location": raw_user_detail.location
    })
    # print(filtered_data)
    return filtered_data


def get_unique_roles(db):
    roleJobTitles = CrewMember.objects.values_list('roleJobTitle', flat=True).distinct()
    return list(roleJobTitles)


def get_crew_requirements(detailed_desc, roleJobTitle):
    prompt_crew_requirement_getter = f"You are an experienced film production assistant and an expert in planning and organizing film crews. Your task is to provide comprehensive list of crew members required to complete a film production project based on the details provided by the user. This includes identifying all essential crew roles, detailing their primary responsibilities, and specifying the number of individuals needed for each specific role. Also, consider any specialized roles required for the specific requirements of the project. Make sure that all roles chose must only be from these : {roleJobTitle}. Note that if project is to be done in multiple locations we might need crew at multiple location or we might travel, understand the requirement and give output accordingly. Now if two camera operator are required one at location1 and other at location2 then output them separately like one camera operator at location1 and one camera operator at locatin2. but if both camera operator are required at location1 then output them together like camera operator at location1 and number_needed is 2. Output must be in JSON format and should contain only following fields :[roleJobTitle, responsibilty_in_project, number_needed, location]"
    messages = [
        ("system", prompt_crew_requirement_getter),
        ("user", f"This is the project details from user : {detailed_desc}"),
    ]
    response = llm_json.invoke(messages)
    crew_requirements = json.loads(response.content)
    try : 
        crew_requirements = crew_requirements["crew"]
    except : 
        crew_requirements = crew_requirements
    return crew_requirements


def get_queries(crew_requirements):
    prompt_query_generator = "You are the database manager at my film production management company, a client will contact you with the crew requirement and then you need to define queries to database to get the data for that particular role. Queries should be for a SQL DB and should filter data out based on, role and location. Output should be in JSON format as list of query. You are a man of words your responses are upto the point and no unnecessary blaberring and words are mentioned, only JSON is outputted, take point location can only be a country."
    messages = [
        ("system", prompt_query_generator),
        ("user", f"Following is the requirement of the customer : {crew_requirements}"),
    ]
    response = llm_json.invoke(messages)
    queries = json.loads(response.content)
    
    try : 
        queries = queries["queries"]
    except : 
        queries = queries

    return queries


def get_selected_crews(filtered_crew, number_needed, hiring_role, detailed_desc):
    
    # print("\n\n\n ############## THIS IS REAL FILTERED CREW \n\n\n\n")
    # print("number_needed", number_needed)
    # print("filtered_crews", filtered_crew)
    # print("\n\n\n ############## \n\n\n\n")

    prompt_crew_selection = "You are a HR in my firm and you have to select the best possible crew. Your subordinates will provide you with the project detail, the crew that match the criteria for that particular job title, and the number of the crew we need to hire for that project. Now you need to select the best possible crews for that particular role and the reason why you preferred those particular person.Make sure provided number of crews are selected. Remember, year of experience should not be the only factor. Make sure preferred member can work well in the project. Output should be in JSON format which should follow this: { {'userid' , 'preferred_because', 'location'} }."
    messages = [
        ("system", prompt_crew_selection),
        ("user", f"Following is the list of available members for the project: {filtered_crew}, you need to hire {number_needed} members, for the role of {hiring_role} for this project: {detailed_desc}"),
    ]

    response = llm_json.invoke(messages)
    selected_crews = json.loads(response.content)
    # print("\n\n\n ############## THIS IS REAL SELECTED CREW \n\n\n\n")
    # print("selected_crews", selected_crews)
    # print("\n\n\n ############## \n\n\n\n")
    try : 
        selected_crews = selected_crews["selected_crew"]
    except : 
        selected_crews = selected_crews
    return selected_crews

def get_selected_crew_details(filtered_data):
    selected_crews = {}
    for dictionary in filtered_data:
        for key, val in dictionary.items():
            user = val
            user_details = CrewMember.objects.filter(userid=user['UserId']).first()
            if user_details:
                role = key
                if role not in selected_crews:
                    selected_crews[role] = []
                selected_crews[role].append({
                    "name": user_details.name,
                    "userid": user_details.userid,
                    "preferred_because": user['Preferred_because'],
                    "roleJobTitle": user_details.roleJobTitle,
                    "yoe": user_details.yoe,
                    "minRatePerDay": user_details.minRatePerDay,
                    "maxRatePerDay": user_details.maxRatePerDay,
                        "location": user_details.location
                    })
    # print(selected_crews)
    return selected_crews

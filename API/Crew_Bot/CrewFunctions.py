import json
from crew.models import CrewMember
from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


# For LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0.2, api_key=OPENAI_API_KEY)
# For LLM that returns json
llm_json = ChatOpenAI(model="gpt-4o", temperature=0.2, api_key=OPENAI_API_KEY).bind(response_format={"type": "json_object"})

def filter_crew_members(role, location):
    try:
        raw_user_details = CrewMember.objects.filter(role=role, location=location)
    except CrewMember.DoesNotExist:
        return None

    filtered_data = []
    for raw_user_detail in raw_user_details:
        filtered_data.append({
        "name": raw_user_detail.name,
        "userid": raw_user_detail.userid,
        "crewType": raw_user_detail.crewType,
        "role": raw_user_detail.role,
        "services": raw_user_detail.services.split(', '),
        "tags": raw_user_detail.tags.split(', '),
        "expertise": raw_user_detail.expertise.split(', '),
        "yoe": raw_user_detail.yoe,
        "minRatePerDay": raw_user_detail.minRatePerDay,
        "maxRatePerDay": raw_user_detail.maxRatePerDay,
        "location": raw_user_detail.location
    })
    # print("\n\n Filteered Data \n",filtered_data)
    return filtered_data


def get_unique_roles():
    roles = CrewMember.objects.values_list('role', flat=True).distinct()
    return list(roles)


def  get_crew_requirements(project_name, description, unique_roles, content_type, additional_details, locations, ai_suggestions, budget, user_crew_requirements):
    # print("\n\n ######## CREW_REQUIREMENT ######   \n\n")
    # print(user_crew_requirements)
    # print("ai suggestion: ", ai_suggestions)
    # print("\n\n")
    if ai_suggestions:
        prompt_crew_requirement_getter = f"You are an experienced film production assistant and an expert in planning and organizing film crews. Your task is to provide comprehensive list of crew members required to complete a film production project based on the details provided by the user. This includes identifying all essential crew roles, detailing their primary responsibilities, and specifying the number of individuals needed for each specific role. Also, consider any specialized roles required for the specific requirements of the project. Make sure that all roles chosen must only be from these : {unique_roles}. Note that if project is to be done in multiple locations we might need crew at multiple location or we might travel, understand the requirement and give output accordingly. Now if two camera operator are required one at location1 and other at location2 then output them separately like one camera operator at location1 and one camera operator at locatin2. but if both camera operator are required at location1 then output them together like camera operator at location1 and number_needed is 2. Output must be in JSON format and should contain only following fields :" + " { crew_requirements : [role, number_needed, location] }"
        messages = [
            ("system", prompt_crew_requirement_getter),
            ("user", f"This is the project details from user : project name : {project_name}, description : {description}, content_type : {content_type}, additional_details : {additional_details}, locations : {locations} budget : {budget}"),
        ]
        response = llm_json.invoke(messages)
        crew_requirements = json.loads(response.content)

        # print("crew_requirements from GPT : ",crew_requirements)
        try : 
            crew_requirements = crew_requirements["crew_requirements"]
        except : 
            crew_requirements = crew_requirements

        # TO MANUALLY FIX ANY INCOREECT BUNDLING
        grouped_data = {}
        for item in crew_requirements:
            key = (item["role"], item["location"])  # Group by role and location
            if key in grouped_data:
                grouped_data[key]["number_needed"] += item["number_needed"]
            else:
                grouped_data[key] = item
        # grouped_data = list(grouped_data.values())

        return grouped_data
    
    else:
        prompt_crew_requirement_getter = f"You are an experienced film production assistant and an expert in planning and organizing film crews. Your task is to study user needs based on the crew requirements provided by user, and divide them based on locations the user wants to do the project. Make sure that all roles chosen must only be from these : {unique_roles}. Note that if project is to be done in multiple locations we might need crew at multiple location or we might travel, understand the requirement and give output accordingly. Now if two camera operator are required one at location1 and other at location2 then output them separately like one camera operator at location1 and one camera operator at locatin2. but if both camera operator are required at location1 then output them together like camera operator at location1 and number_needed is 2. Generate crew requirements for each individual roles. Output must be in JSON format and should contain only following fields :" + " { crew_requirements : [role, number_needed, location] }"
        messages = [
            ("system", prompt_crew_requirement_getter),
            ("user", f"This is the project details from user : project name : {project_name}, description : {description}, content_type : {content_type}, additional_details : {additional_details}, locations : {locations} budget : {budget}, crew_requirements : {user_crew_requirements}"),
        ]
        response = llm_json.invoke(messages)
        crew_requirements = json.loads(response.content)
        # print("crew_requirements from GPT : ",crew_requirements)
        try : 
            crew_requirements = crew_requirements["crew_requirements"]
        except : 
            crew_requirements = crew_requirements
            
        # print("\n\n ######## FINAL_CREW_REQUIREMENT ######   \n\n")
        # print(crew_requirements)
        # print("\n\n")  
        
        # TO MANUALLY FIX ANY INCOREECT BUNDLING
        grouped_data = {}
        for item in crew_requirements:
            key = (item["role"], item["location"])  # Group by role and location
            if key in grouped_data:
                grouped_data[key]["number_needed"] += item["number_needed"]
            else:
                grouped_data[key] = item
        grouped_data = list(grouped_data.values())

        return grouped_data


def get_selected_crews(filtered_crew, number_needed, hiring_role, project_name, content_type, description, additional_details, budget):
    
    # print("\n\n\n ############## THIS IS REAL FILTERED CREW \n\n\n\n")
    # print("number_needed", number_needed)
    # print("filtered_crews", filtered_crew)
    # print("\n\n\n ############## \n\n\n\n")

    prompt_crew_selection = "You are a HR in my firm and you have to select the best possible crew. Your subordinates will provide you with the project detail, the crew that matches the criteria for that particular role, and the number of the crew we need to hire for that project. Now you need to select the best possible crews for that particular role and the reason why you preferred those particular people. Make sure provided number of crews are selected. Remember, year of experience should not be the only factor, the preferred_because entry should be written in such a way that it can be used as a summary/bio also. Make sure preferred member can work well in the project. Also make sure that crew cost is less than the budget provided by the client. Output should be in JSON format which should follow this: { {'userid' , 'preferred_because', 'location'} }."
    messages = [
        ("system", prompt_crew_selection),
        ("user", f"Following is the list of available members for the project: {filtered_crew}, you need to hire {number_needed} members, for the role of {hiring_role} for this project: project name : {project_name}, content_type : {content_type}, description : {description}, additional_details : {additional_details}, budget : {budget}"),
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
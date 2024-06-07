import os
from dotenv import load_dotenv


def import_env_var(var_name):
    load_dotenv()
    env_var = os.getenv(var_name)
    if env_var is None:
        raise ValueError(f"{var_name} not found. Please check your .env file.")
    else:
        return env_var


OPENAI_API_KEY = import_env_var("OPENAI_API_KEY")

import sqlite3
import json


def filter_crew_members(roleJobTitle, location, db):
    dbname = db.split('.')[0]
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(
        f"SELECT * FROM \'{dbname}\' WHERE roleJobTitle = \'{roleJobTitle}\' AND location = \'{location}\'"
    )
    filtered_data = c.fetchall()
    conn.close()
    return filtered_data


# print(filter_crew_members('Camera Operator', 'Dubai', 'crewdata.db'))


def filter_equipment(name, location, db):
    dbname = db.split('.')[0]
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(
        f"SELECT * FROM \'{dbname}\' WHERE name = \'{name}\' AND location = \'{location}\'"
    )
    filtered_data = c.fetchall()
    conn.close()
    return filtered_data


# print(filter_equipment('broadcast_camera', 'Sony', 'equipment.db'))
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Set your OpenAI API key
api_key = OPENAI_API_KEY

# # Initialize the ChatOpenAI instance
llm = ChatOpenAI(model="gpt-4o", temperature=0.2, api_key=api_key)
llm_json = ChatOpenAI(
    model="gpt-4o", temperature=0.2,
    api_key=api_key).bind(response_format={"type": "json_object"})
from pprint import pprint

import json


def get_detailed_desc(desc):
    prompt_detailed_desc = "You are the production advisor and primary contract for the customer. The customer will come to you and describe their project. You need to make the necessary changes so that project details are completely described and even new members can understand the need. It should be such that everyone can get the overview of the project at a glance. The description should try to contain the following in a paragraph : a descriptive overview of the project, locations that will be involved and task at each location, and whether the same team will travel to different locations or if customer will require different teams at different locations. No formatting should be applied to the output, for better clearity and understanding."
    messages = [
        ("system", prompt_detailed_desc),
        ("user", f"This is the project details from user : {desc}"),
    ]
    response = llm.invoke(messages)
    detailed_desc = response.content
    return detailed_desc


def get_unique_roles(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    query = "SELECT DISTINCT roleJobTitle FROM crewdata"
    c.execute(query)
    rows = c.fetchall()
    roleJobTitles = [row[0] for row in rows]
    conn.close()

    return roleJobTitles


def get_crew_requirements(detailed_desc, roleJobTitle):
    prompt_crew_requirement_getter = f"You are an experienced film production assistant and an expert in planning and organizing film crews. Your task is to provide comprehensive list of crew members required to complete a film production project based on the details provided by the user. This includes identifying all essential crew roles, detailing their primary responsibilities, and specifying the number of individuals needed for each specific role. Also, consider any specialized roles required for the specific requirements of the project. Make sure that all roles chose must only be from these : {roleJobTitle}. Note that if project is to be done in multiple locations we might need crew at multiple location or we might travel, understand the requirement and give output accordingly. Now if two camera operator are required one at location1 and other at location2 then output them separately like one camera operator at location1 and one camera operator at locatin2.  Output must be in JSON format and should contain only following fields :[roleJobTitle, responsibilty_in_project, number_needed, location]"
    messages = [
        ("system", prompt_crew_requirement_getter),
        ("user", f"This is the project details from user : {detailed_desc}"),
        # ("user", "The maximum number of crew you can hire is 5")
    ]
    response = llm_json.invoke(messages)
    crew_requirements = json.loads(response.content)
    try:
        crew_requirements = crew_requirements["crew"]
    except:
        crew_requirements = crew_requirements
    return crew_requirements


def get_queries(crew_requirements):
    prompt_query_generator = "You are the database manager at my film production management company, a client will contact you with the crew requirement and then you need to define queries to database to get the data for that particular role. Queries should be for a SQL DB and should filter data out based on, role and location. Output should be in JSON format as list of query. You are a man of words your responses are upto the point and no unnecessary blaberring and words are mentioned, only JSON is outputted"
    messages = [
        ("system", prompt_query_generator),
        ("user",
         f"Following is the requirement of the customer : {crew_requirements}"
         ),
    ]
    response = llm_json.invoke(messages)
    queries = json.loads(response.content)
    try:
        queries = queries["queries"]
    except:
        queries = queries

    return queries


def get_selected_crews(filtered_crew, number_needed, hiring_role,
                       detailed_desc):
    prompt_crew_selection = "You are a HR in my firm and you have to select the best possible crew. Your subordinates will provide you with the project detail, the crew that match the criteria for that particular job title, and the number of the crew we need to hire for that project. Now you need to select the best possible crew for that particular role and the reason why you preferred that particular person. Remember, year of experience should not be the only factor. Make sure preferred member can work well in the project. Output should be in JSON format which should follow this: {'UserId': , 'Preferred_because'}. Only output JSON. You don't need to put anything extra as your output will be directly fed to a function, so just output JSON."
    # selected_crews = []
    messages = [
        ("system", prompt_crew_selection),
        ("user",
         f"Following is the list of available members for the project: {filtered_crew}, you need to hire {number_needed} members, for the role of {hiring_role} for this project: {detailed_desc}"
         ),
    ]

    response = llm_json.invoke(messages)
    selected_crews = json.loads(response.content)
    # selected_crews.append(selected_crew)
    return selected_crews


def get_unique_equipments(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    query = "SELECT DISTINCT name FROM equipment"
    c.execute(query)
    rows = c.fetchall()
    equipments = [row[0] for row in rows]
    conn.close()
    return equipments


def get_equipment_requirements(crew_requirements, detailed_desc, name):
    prompt_equipment_requirement_getter = f"""You are an experienced film production assistant and an expert in planning and organizing film crews. Your task is to provide a comprehensive list of the equipment required to complete a film production project based on the details provided by the user. This includes identifying all essential equipment, detailing their primary responsibilities, and specifying the number of individuals needed for each specific role. Here is the crew requirement: {crew_requirements}. Now you need to provide the equipment required for the project that is well-suited to the crew requirements. Note that if the project is to be done in multiple locations, we might need equipment at multiple locations or we might transport equipment between locations. Understand the requirements and give output accordingly.
    
    Each crew member's role requires specific equipment. Here are some examples of the role-to-equipment mapping:

    - Producer: ["Laptops/Computers", "High-Speed Internet"]
    - Director: ["Teleprompter", "Laptops/Computers", "Walkie-talkies"]
    - Technical Director: ["Camera Switcher", "Streaming Encoder", "High-Speed Internet"]
    - Camera Operator: ["broadcast_camera", "Tripods and Mounts", "HDMI/SDI Cables"]
    - Sound Engineer: ["Lavalier Mics", "Handheld Mics", "Boom Mics", "Audio Mixer", "XLR Cables"]

    Based on these examples and the provided project details and crew requirements, generate a comprehensive list of equipment requirements.
    Output must be in JSON format and should contain only the following fields :[name, number_needed, Specification_required]"""
    messages = [
        ("system", prompt_equipment_requirement_getter),
        ("user", f"This is the project details from user : {detailed_desc}"),
        ("user",
         f"Make sure that all equipment chosen must only be from these: {name}."
         )
    ]
    response = llm_json.invoke(messages)
    equipment_requirements = json.loads(response.content)
    try:
        equipment_requirements = equipment_requirements["equipment"]
    except:
        equipment_requirements = equipment_requirements
    return equipment_requirements


def get_selected_equipments(filtered_equipment, crew_selected, number_needed,
                            equipmentName, specification, detailed_desc):
    prompt_equipment_selection = f"""
     You are the HR in our firm, responsible for selecting the best possible equipment for our projects. Your subordinates will provide you with the project details, including the required equipment and the quantity needed. Based on this information and the selected crew for the project, you need to choose the most suitable equipment and explain your preference.
     Here’s what you need to consider:
     Select equipement according to the specification needed. Here is the datails about their specification: {specification}.
     Match Equipment to Crew: Select equipment that best fits the crew's roles and the number of crew members. For example, if we need to shoot a scene from two different angles and have equal to or more than two camera operators, we can select two cameras. However, if there is only one camera operator, you should select only one camera.
     Assign Equipment Accordingly: Ensure that the equipment is suitable for the crew members available. If a specific piece of equipment requires a specific crew member and none are available, try to assign it to another crew member. If no one can operate it, exclude that equipment.
     Rationale for Selection: Make sure to explain why you prefer a particular piece of equipment. This could be based on compatibility, ease of use, the specific needs of the project, or the capabilities of the crew.
     The output should be in JSON format which should follow this: ['name', 'model', 'brand', 'number_needed', 'Preferred_because', 'provider_email']. Only output JSON. You don't need to put anything extra as your output will be directly fed to a function, so just output JSON.
    """
    messages = [
        ("system", prompt_equipment_selection),
        ("user",
         f"Following is the list of available equipment for the project: {filtered_equipment}, you need to procure {number_needed} pieces of equipment, for the purpose of {equipmentName} for this project: {detailed_desc}"
         ),
        ("user",
         f"Make sure that all equipment chosen must be well fitted to the crew selected. Selected crew are these: {crew_selected}."
         )
    ]

    response = llm_json.invoke(messages)
    selected_equipments = json.loads(response.content)
    return selected_equipments



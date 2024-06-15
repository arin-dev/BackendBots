from typing import TypedDict, List

from .models import CrewMember
from Crew_Bot.CrewGraph import CrewGraph
from crew.models import CrewMember, Project, CrewRequirement, SelectedCrew

class State(TypedDict):
    project_name : str
    content_type : str
    description : str
    additional_details : str
    budget : int
    locations : str
    ai_suggestions : bool
    unique_roles : List[str]
    user_crew_requirements : List[dict]
    crew_requirements : List[dict]
    queries : List[str]
    selected_crews : List[dict]

def get_form_data(request):
    form_data = request.data
    project_name = form_data.get('projectName')
    content_type = form_data.get('contentType')
    description = form_data.get('description')
    additional_details = form_data.get('additional_details')
    budget = form_data.get('budget')
    location_details = form_data.get('locationDetails')
    ai_suggestions = form_data.get('ai_suggestions')
    user_crew_requirements = form_data.get('crew')
    # user_equipment_requirements = form_data.get('equipment')
    # locations = []
    # for location in location_details:
    #     locations.append(location["location"].replace("'", "").split(",")[0])
    ############ because of lack of dataa it is giving error ###########
    locations = ['Dubai']
    my_state = State(project_name=project_name, content_type=content_type, budget=budget, description=description, additional_details=additional_details, locations=locations, ai_suggestions=ai_suggestions, unique_roles=[], user_crew_requirements=user_crew_requirements, crew_requirements=[], queries=[], selected_crews=[])

    return my_state

def transform_crew_data(input_data):
    transformed_data = {}
    # print(" \n\n\n selected crews set \n\n\n ")
    for crew in input_data['selected_crews_set']:
        # print(crew)
        member = crew['crew_member']
        role = member['role']
        preferred_because=crew["preferred_because"]
        user_details = {
            "name": member["name"],
            "yoe": member["yoe"],
            "userid":member["userid"],
            "minRatePerDay": float(member["minRatePerDay"]),
            "maxRatePerDay": float(member["maxRatePerDay"]),
            "location": member["location"],
            "preferred_because": preferred_because
        }
        if role not in transformed_data:
            transformed_data[role] = []
        transformed_data[role].append(user_details)
    final_output = [{role: details} for role, details in transformed_data.items()]
    return final_output

def createCrewRequirement(crew_req, new_project):
    if isinstance(crew_req,List):
        for crew in crew_req:
            new_crew = CrewRequirement(
                project=new_project,
                role=crew["role"], 
                number_needed=crew["number_needed"],
                location=crew["location"],
            )
            new_crew.save()
    else:
        crew = crew_req
        new_crew = CrewRequirement(
            project=new_project,
            role=crew["role"], 
            number_needed=crew["number_needed"],
            location=crew["location"],
        )
        new_crew.save()

def createSelectedCrews(selected_crews, new_project):
    # print("\n\n\n ###########  \n\n\n")
    # print("\n\nselected_crews", type(selected_crews), selected_crews)
    for role_dict in selected_crews:
        # print("\n\n\n ########### role_dict.items() #######  \n\n\n")
        # print("\n\n role_dict", type(role_dict), role_dict.items())
        for role, crews in role_dict.items():
            # print("\n\n\n ########### role and crews ########### ")
            # print("role", role, "crews", crews, "type", type(crews))
            # print("length", len(crews))
            if isinstance(crews, list):
                for crew in crews:
                    # print("\n\n\n ########### crew ########### ")
                    # print("crew[userid]", crew["userid"])
                    new_selected_crew = SelectedCrew(
                    project=new_project,
                    crew_member=CrewMember.objects.get(userid=crew["userid"]),
                    crew_requirements=CrewRequirement.objects.get(project=new_project, role=role, location=crew["location"]),
                    preferred_because=crew["preferred_because"]
                    )
                    new_selected_crew.save()
            else:
                # print("\n\n\n ########### crews ########### ")
                # print("crews[userid]", crews["userid"])
                new_selected_crew = SelectedCrew(
                project=new_project,
                crew_member=CrewMember.objects.get(userid=crews["userid"]),
                crew_requirements=CrewRequirement.objects.get(project=new_project, role=role, location=crews["location"]),
                preferred_because=crews["preferred_because"]
                )
                new_selected_crew.save()
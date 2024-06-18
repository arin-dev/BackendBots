from typing import TypedDict, List

from .models import CrewMember
from Crew_Bot.CrewGraph import CrewGraph
from .models import CrewMember, CrewRequirement, SelectedCrew

def transform_crew_data(input_data):
    transformed_data = {}
    # print(" \n\n\n selected crews set \n\n\n ")
    for crew in input_data['selected_crews_set']:
        # print(crew)
        member = crew['crew_member']
        role = member['role']
        preferred_because=crew["preferred_because"]
        user_details = {
            "id":member["id"],
            "profile_pic":member["profile_pic"],
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
import time
import threading
from culture.models import Culture
from typing import TypedDict, List
from Crew_Bot.CrewGraph import CrewGraph
from culture.models import ProjectCulture
from culture.functions import get_cultural_protocols
from django.core.exceptions import ObjectDoesNotExist
from crew.models import CrewMember, CrewRequirement, SelectedCrew

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
    ########### because of lack of dataa it is giving error ###########
    locations = ['Dubai']
    my_state = State(project_name=project_name, content_type=content_type, budget=budget, description=description, additional_details=additional_details, locations=locations, ai_suggestions=ai_suggestions, unique_roles=[], user_crew_requirements=user_crew_requirements, crew_requirements=[], queries=[], selected_crews=[])
    return my_state


def short_wait():
    time.sleep(2)
    print("done")


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


### This portion is just to make code faster, make sure to remove this in upcoming versions so that i always gives latest trends and details.
def create_culture_for_location(location, project_culture):
    details = get_cultural_protocols(location)
    culture, created = Culture.objects.get_or_create(location=location, defaults={'details': details})
    project_culture.cultures.add(culture)

def complete_culture_details(locations, project):
    project_culture = ProjectCulture.objects.create(project=project)
    threads = []
    for location in locations:
        thread = threading.Thread(target=create_culture_for_location, args=(location, project_culture))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()



def complete_project_details(project_state, new_project):
    result = CrewGraph(State=State, state=project_state)
    locations = result['locations']
    crew_req = result["crew_requirements"]
    createCrewRequirement(crew_req, new_project)
    selected_crews = result["selected_crews"]
    createSelectedCrews(selected_crews, new_project)

from typing import TypedDict, List
import time

from crew.models import CrewMember, CrewRequirement, SelectedCrew
from equipment.models import Equipment, EquipmentRequirement, SelectedEquipments
from .models import Project


from Crew_Bot.CrewGraph import CrewGraph
from Equipment_Bot.EquipmentWorkflow import EquipmentGraph

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
    equipments: List[str]
    equipment_requirements: List[dict]
    user_equipment_requirements: List[dict]
    selected_equipments: List[dict]
    


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
    user_equipment_requirements = form_data.get('equipment')
    # locations = []
    # for location in location_details:
    #     locations.append(location["location"].replace("'", "").split(",")[0])
    ########### because of lack of data it is giving error ###########
    locations = ['Dubai']
    my_state = State(project_name=project_name, content_type=content_type, budget=budget, description=description, additional_details=additional_details, locations=locations, ai_suggestions=ai_suggestions, unique_roles=[], user_crew_requirements=user_crew_requirements, crew_requirements=[], queries=[], selected_crews=[], equipments=[], equipment_requirements=[],user_equipment_requirements=user_equipment_requirements,selected_equipments=[])

    return my_state

def short_wait():
    time.sleep(2)
    print("done")

def complete_project_details(project_state, new_project):
    # Calling CrewGraph
    result = CrewGraph(State = State, state=project_state)
    # print("\n\n Fuction0 calling ",result, "type of ",type(result))
    
    crew_req = result["crew_requirements"]
    
    if(type(crew_req)==dict):
        crew_req=crew_req["crew_requirements"]
        
    createCrewRequirement(crew_req, new_project)
    
    selected_crews = result["selected_crews"]
    createSelectedCrews(selected_crews, new_project)
    
    # print("\n\n\n project state is ",project_state,"\n\n")
    # print("\n\n\n result is ",result,"\n\n")
    
    # Calling EquipmentGraph
    result = EquipmentGraph(State=State, state=result)
    equip_req = result["equipment_requirements"]
       
    if(type(equip_req)==dict):
        equip_req=equip_req["equipment_requirements"]
        
    createEquipmentRequirement(equip_req, new_project)
   
    selected_equipments = result["selected_equipments"]
    createSelectedEquipments(selected_equipments, new_project)
    

def createEquipmentRequirement(equip_req, new_project):
    # print("\n\n Fuction01 calling ",equip_req, "type of ",type(equip_req))
    if isinstance(equip_req,List):
        for equip in equip_req:
            new_equip = EquipmentRequirement(
                project=new_project,
                name=equip["name"], 
                Specification_required = equip["Specification_required"],
                number_needed=equip["number_needed"],
                location=equip["location"],
            )
            new_equip.save()
    else:
        equip = equip_req
        new_equip = EquipmentRequirement(
            project=new_project,
            name=equip["name"], 
            Specification_required = equip["Specification_required"],
            number_needed=equip["number_needed"],
            location=equip["location"],
        )
        new_equip.save()
        
def createSelectedEquipments(selected_equipments, new_project):
    # print("\n\n\n ###########  \n\n\n")
    # print("\n\nselected_equipments", type(selected_equipments), selected_equipments)
    for equipment in selected_equipments:
        
         equipment_queryset = Equipment.objects.filter(name=equipment["name"], brand=equipment["brand"], model=equipment["model"])
         equipment_instance = equipment_queryset.first()
         
        #  location = equipment.get('location')
         location = "Dubai"
        #  if location is None:
        #      location="Dubai"
         
        #  equipment_requirements_instance = EquipmentRequirement.objects.get(project=new_project, name=equipment["name"], location=location)
        #  print("\n\n Last part ",new_project.project_id,"  ",equipment["name"],"\n\n")
         
         new_equip_selected = SelectedEquipments(
             project = new_project,
             equipment = equipment_instance,
             equipment_requirements = EquipmentRequirement.objects.get(project=new_project, name=equipment["name"]),
             preferred_because = equipment["preferred_because"],
         )
         new_equip_selected.save()

def createCrewRequirement(crew_req, new_project):
    # print("\n\n Fuction1 calling ",crew_req, "type of ",type(crew_req))
    if isinstance(crew_req,List):
        for crew in crew_req:
            new_equip = CrewRequirement(
                project=new_project,
                role=crew["role"], 
                number_needed=crew["number_needed"],
                location=crew["location"],
            )
            new_equip.save()
    else:
        crew = crew_req
        new_equip = CrewRequirement(
            project=new_project,
            role=crew["role"], 
            number_needed=crew["number_needed"],
            location=crew["location"],
        )
        new_equip.save()



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
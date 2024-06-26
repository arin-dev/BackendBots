import time
import threading
from typing import TypedDict, List, Dict
from Equipment_Bot.EquipmentWorkflow import unique_equipments_getter

from culture.models import Culture
from logistics.models import Logistics
from compliance.models import Compliance
from culture.models import ProjectCulture
from crew.models import CrewMember, CrewRequirement, SelectedCrew
from equipment.models import Equipment, EquipmentRequirement, SelectedEquipments
from Report.models import *

from Crew_Bot.CrewGraph import CrewGraph
from Equipment_Bot.EquipmentWorkflow import EquipmentGraph
from Report.Report_Bot.ReportGraph import ReportGraph
from culture.functions import get_cultural_protocols
from logistics.functions import get_logistics_details
from compliance.functions import get_compliance_report


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
    # unique_equipments: List[str]
    equipment_requirements: List[dict]
    user_equipment_requirements: List[dict]
    selected_equipments: List[dict]

class ReportState(TypedDict):
    selected_crews: List[dict]
    selected_equipments: List[dict]
    crew_report: List[dict]
    equipment_report: List[dict]
    compliance_report: List[dict]
    logistic_report: List[dict]
    culture_report: List[dict]

# Create an instance of ReportState
report_state: ReportState = {
    "selected_crews": [],
    "selected_equipments": [],
    "crew_report": [],
    "equipment_report": [],
    "compliance_report": [],
    "logistic_report": [],
    "culture_report": []
}


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


    locations = []
    for location in location_details:
        locations.append(location["location"].replace("'", "").split(",")[0])
    
    my_state = State(project_name=project_name, content_type=content_type, budget=budget, description=description, additional_details=additional_details, locations=locations, ai_suggestions=ai_suggestions, unique_roles=[], user_crew_requirements=user_crew_requirements, crew_requirements=[], queries=[], selected_crews=[],equipments=[], equipment_requirements=[],user_equipment_requirements=user_equipment_requirements,selected_equipments=[])
    return my_state, location_details


def complete_project_details(project_state, new_project):
    # Calling CrewGraph
    result = CrewGraph(State = State, state=project_state)
    # print("\n\n Fuction0 calling ",result, "type of ",type(result))

    crew_req = result["crew_requirements"]
    createCrewRequirement(crew_req, new_project)

    selected_crews = result["selected_crews"]
    createSelectedCrews(selected_crews, new_project)
    
   
    
    # Calling EquipmentGraph
    result = EquipmentGraph(State=State, state=result)
    
    equip_req = result["equipment_requirements"]

    if(type(equip_req)==dict):
        equip_req=equip_req["equipment_requirements"]
        
    # print("\n\n OPERATION IN EQUIP REQ JSON \n\n")
    # items= []
    # for x in equip_req:
    #     if x["name"]=="Laptops/Computers":
    #         items.append(x)
    # print("\n After operat  ",items,"\n")    
    print("\n\n\n ############# Entering into create equipment requirement :", equip_req)
    createEquipmentRequirement(equip_req, new_project)

    selected_equipments = result["selected_equipments"]
    print("\n\n\n ############# Entering into create selected equipment :", selected_equipments)
    createSelectedEquipments(selected_equipments, new_project)
    
    print("\n\n Selected crew is",type(result["selected_crews"]),"    ",type(report_state["selected_crews"]),"\n\n")
    # print("\n\n weeed euipmnsko2 is",result["selected_equipments"],"\n\n")
    
    # global report_state
    report_state["selected_crews"]=result["selected_crews"]
    
    report_state["selected_equipments"]=result["selected_equipments"]
    # print("\n Before calling",report_state["selected_equipments"],"\n")
    

def Crew_Equip_Report(project_state, new_project):
    report_result=ReportGraph(report_state)
    print("Report Result is",report_result)
    
    crewrepo=report_result["crew_report"]
    
    if type(crewrepo)==dict:
        if "crew" in crewrepo:
            crewrepo=crewrepo["crew"]
        elif "selected_crew" in crewrepo:
            crewrepo=crewrepo["selected_crew"]
            
    CreateCrewReport(crewrepo, new_project)
    
    equiprepo=report_result["equipment_report"]
    
    if type(equiprepo)==dict:
        if "equipment" in equiprepo:
            equiprepo=equiprepo["equipment"]
        elif "selected_equipment" in equiprepo:
            equiprepo=equiprepo["selected_equipment"]
            
    CreateEquipmentReport(equiprepo, new_project)
    
    CreateCompleteReport(crewrepo,equiprepo,new_project)

    
def CreateCompleteReport(crewrepo,equiprepo,new_project):
    # Handle crew reports
    if isinstance(crewrepo, list):
        crew_report_instances = []
        for crew in crewrepo:
            crew_report_instance = CrewReport.objects.create(
                project=new_project,
                name=crew["name"],
                userid=crew["userid"],
                gender=crew["gender"],
                age=crew["age"],
                driving_licence=crew["driving_licence"]
            )
            crew_report_instances.append(crew_report_instance)
    else:
        crew_report_instances = [crewrepo]  # If crewrepo is a single instance

    # Handle equipment reports
    if isinstance(equiprepo, list):
        equipment_report_instances = []
        for equip in equiprepo:
            equipment_report_instance = EquipmentReport.objects.create(
                project=new_project,
                name=equip["name"],
                brand=equip["brand"],
                model=equip["model"],
                cost=equip["cost"],
                size=equip["size"],
                sensitive=equip["sensitive"]
            )
            equipment_report_instances.append(equipment_report_instance)
    else:
        equipment_report_instances = [equiprepo]  # If equiprepo is a single instance

    # Create complete reports
    min_length = min(len(crew_report_instances), len(equipment_report_instances))

    for i in range(min_length):
        complete_report = CompleteReport(
            project=new_project,
            crew_report=crew_report_instances[i],
            equipment_report=equipment_report_instances[i]
        )
        complete_report.save()

    if len(crew_report_instances) > len(equipment_report_instances):
        for i in range(min_length, len(crew_report_instances)):
            complete_report = CompleteReport(
                project=new_project,
                crew_report=crew_report_instances[i],
                equipment_report=None 
            )
            complete_report.save()
    else:
        for i in range(min_length, len(equipment_report_instances)):
            complete_report = CompleteReport(
                project=new_project,
                crew_report=None, 
                equipment_report=equipment_report_instances[i]
            )
            complete_report.save()

def CreateCrewReport(crew_report,new_project):
    # print("\nInside CreateCrewReport1 ",crew_report)
    
       
    if isinstance(crew_report,List):
        for crew in crew_report:
            # print("\n Inside loop ",new_project)
            new_report = CrewReport(
                project=new_project,
                name=crew["name"],
                userid= crew["userid"],
                age=crew["age"],
                gender = crew["gender"],
                driving_licence = crew["driving_licence"],
            )
            new_report.save()
    else:
        crew = crew_report
        # print("\n Inside without loop ",new_project)
        new_report = CrewReport(
                project=new_project,
                name=crew["name"],
                userid= crew["userid"],
                age=crew["age"],
                gender = crew["gender"],
                driving_licence = crew["driving_licence"],
            )
        new_report.save()

def CreateEquipmentReport(equip_report,new_project):
    
    if type(equip_report)==dict:
        if "equipment" in equip_report:
            equip_report=equip_report["crew"]
        elif "selected_equipment" in equip_report:
            equip_report=equip_report["selected_equipment"]
    
    # print("\n Inside EquipmentCreating ",equip_report)
    
    if isinstance(equip_report,List):
        for equip in equip_report:
            new_report = EquipmentReport(
                project=new_project,
                name = equip["name"],
                model = equip["model"],
                cost = equip["cost"],
                size = equip["size"],
                sensitive = equip["sensitive"],
            )
            new_report.save()
    else:
        equip=equip_report
        new_report = EquipmentReport(
                project=new_project,
                name = equip["name"],
                model = equip["model"],
                cost = equip["cost"],
                size = equip["size"],
                sensitive = equip["sensitive"],
            )
        new_report.save()
    

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
        print(equipment)
        new_equip_selected = SelectedEquipments(
            project = new_project,
            equipment = equipment_instance,
            equipment_requirements = EquipmentRequirement.objects.get(project=new_project, name=equipment["name"]),
            preferred_because = equipment["Preferred_because"],
         )
        new_equip_selected.save()
    print("\n------ Ready to call APIs -------- \n")



def createCrewRequirement(crew_req, new_project):
    # print("\n\n Fuction1 calling ",crew_req, "type of ",type(crew_req))
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
                    # print("\n\n\n ########### I want this : crew ########### \n ", "crew#",crew,"#crew")
                    # print(not crew)
                    if not crew:
                        continue
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
                # print("\n\n\n ########### crew ########### \n ", crews)
                if not crews:
                    continue
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
def create_culture_for_location(location, project):
    details = get_cultural_protocols(location)
    culture, created = Culture.objects.get_or_create(location=location, defaults={'details': details})
    ProjectCulture.objects.create(project=project, culture=culture)

def complete_culture_details(locations, project):
    threads = []
    for location in locations:
        thread = threading.Thread(target=create_culture_for_location, args=(location, project))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()



def create_logistics_details(destination, start_date, end_date, new_project):
    response = get_logistics_details(destination=destination, start_date=start_date, end_date=end_date)
    logistics = Logistics(
        project=new_project,
        flights_details=response.get('flight_details'),
        hotel_details=response.get('hotel_details'),
        taxi_details=response.get('taxi_details')
    )
    logistics.save()

def complete_logistics_details(location_details, new_project):
    threads = []
    for location_detail in location_details:
        location, start_date, end_date = location_detail.get('location'), location_detail.get('start_date'), location_detail.get('end_date')
        thread = threading.Thread(target=create_logistics_details, args=(location, start_date, end_date, new_project))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
        


def create_compliance_details(new_project, location, mode, crew_size, time_frame, landmarks=None, special_equipment=None):
    compliance = Compliance(
        project=new_project,
        location=location,
        mode=mode,
        crew_size=crew_size,
        time_frame=time_frame,
        landmarks=landmarks,
        special_equipment=special_equipment,
        report = get_compliance_report(location, mode, crew_size, time_frame, landmarks, special_equipment)
    )
    compliance.save()

def complete_compliance_reports(project_state, location_details, new_project):
    threads = []
    crew_size = sum(project_state.get('user_crew_requirements').values())
    for location_detail in location_details:
        location, start_date, end_date, mode = location_detail.get('location'), location_detail.get('start_date'), location_detail.get('end_date'), location_detail.get('mode')
        time_frame = str(start_date) + " to " + str(end_date)
        thread = threading.Thread(target=create_compliance_details, args=(new_project, location, mode, crew_size, time_frame, None, None))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
        
# --------------- Creating Reports ------------------#


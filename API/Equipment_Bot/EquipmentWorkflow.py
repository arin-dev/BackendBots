from .PromptFunctions import *
from langgraph.graph import END, StateGraph
from typing import TypedDict, List, Annotated
from equipment.models import Equipment, Provider, Availability


# Finding out all unique equipments
def unique_equipments_getter(State):
    # print("\n\n ########## State in Equipments are: ", State)
    unique_equipments = get_unique_equipments()
    # print("\n\n ########## Uniquie Equipments are: ", unique_equipments)
    return {"unique_equipments": unique_equipments}


# Required Equipments from the data base
def equipment_requirement_getter(State):
    detailed_desc = State["description"]
    unique_equipments = State["unique_equipments"]
    crew_requirement = State["crew_requirements"]
    additional_details = State["additional_details"]
    equipment_requirements = get_equipment_requirements(
        crew_requirement, detailed_desc, additional_details, unique_equipments)
    
    # print("\n\n\n ############# Equipment requirement is:", equipment_requirements,"\n\n\n")
    return {"equipment_requirements": equipment_requirements}

# Selcting the Equipments from the data base
def equipment_selection(State):

    detailed_desc = State["description"]
    equipment_requirements = State["equipment_requirements"]
    crew_selected = State["selected_crews"]
    additional_details = State["additional_details"]
    
    # print("\n\nChecking Data coming or not\n\n")
    # print("description:", detailed_desc)
    # print("crew selected:", crew_selected, "\n\n")
    # print("\n\n\n ############# Equipment requirement is:", equipment_requirements,"Typr of equip_req is",type(equipment_requirements),"\n\n")
    
    # if(type(equipment_requirements)==dict):
    #     equipment_requirements = equipment_requirements["equipment_requirements"]
    
    selected_equipments = []
    for equipment in equipment_requirements:
        filtered_equipment = filter_equipment(equipment["name"])
        number_needed = equipment["number_needed"]
        equipmentName = equipment["name"]
        specification = equipment["Specification_required"]

        # print("\n\n\n ############# filtered_equipment is:", filtered_equipment,"\n\n\n")
        selected_equipments_for_task = get_selected_equipments(
            filtered_equipment, crew_selected, number_needed, equipmentName, specification, detailed_desc, additional_details)
        selected_equipments.append(selected_equipments_for_task)

    return {"selected_equipments": selected_equipments}


def State_printer(State):
    print("\n\n ###### Equipment Project is finished! ###### \n\n")
    return

def EquipmentGraph(State: dict, state):
    workflow = StateGraph(State)

    workflow.add_node("unique_equipments_getter", unique_equipments_getter)
    workflow.add_node("equipment_requirement_getter", equipment_requirement_getter)
    workflow.add_node("equipment_selection", equipment_selection)
    workflow.add_node("State_printer", State_printer)


    workflow.add_edge("unique_equipments_getter", "equipment_requirement_getter")
    workflow.add_edge("equipment_requirement_getter", "equipment_selection")
    workflow.add_edge("equipment_selection", "State_printer")

    workflow.set_entry_point("unique_equipments_getter")
    workflow.add_edge("State_printer", END)

    app = workflow.compile()
    output = app.invoke(state)
    
    return output
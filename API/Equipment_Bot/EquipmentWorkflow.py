from .PromptFunctions import *
from langgraph.graph import END, StateGraph
from typing import TypedDict, List, Annotated
from equipment.models import Equipment, Provider, Availability
from Report.Report_Bot.ReportFunctions import equipment_report


# Finding out all unique equipments
def unique_equipments_getter(State):
    equipments = get_unique_equipments()
    return {"equipments": equipments}


# Required Equipments from the data base
def equipment_requirement_getter(State):
    detailed_desc = State["description"]
    equipments = State["equipments"]
    crew_requirement = State["crew_requirements"]
    additional_details = State["additional_details"]
    ai_suggestions =State["ai_suggestions"]
    user_equipment_requirements = State["user_equipment_requirements"]
    equipment_requirements = get_equipment_requirements(
        crew_requirement, detailed_desc, additional_details, equipments, ai_suggestions, user_equipment_requirements)
    return {
        "equipment_requirements": equipment_requirements}

# Selcting the Equipments from the data base
def equipment_selection(State):

    detailed_desc = State["description"]
    equipment_requirements = State["equipment_requirements"]
    crew_selected = State["selected_crews"]
    additional_details = State["additional_details"]
    user_equipment_requirements = State["user_equipment_requirements"]
    
    # print("\n\nChecking Data coming or not\n\n")
    # print("description:", detailed_desc)
    # print("crew selected:", crew_selected, "\n\n")
    # print("Equipment requirement is:", equipment_requirements,"Typr of equip_req is",type(equipment_requirements),"\n\n")
    # print("User Equipment requirement is:", user_equipment_requirements,"Typr of equip_req is",type(user_equipment_requirements),"\n\n")
    
    if(type(equipment_requirements)==dict):
        equipment_requirements = equipment_requirements["equipment_requirements"]
    
    selected_equipments = []
    for equipment in equipment_requirements:
        filtered_equipment = filter_equipment(equipment["name"], 'Dubai')
        number_needed = equipment["number_needed"]
        equipmentName = equipment["name"]
        specification = equipment["Specification_required"]
        
        # print("\n\n Filtered Equipments are ", filtered_equipment,"\n\n")

        selected_equipments_for_task = get_selected_equipments(
            filtered_equipment, crew_selected, number_needed, equipmentName, specification, detailed_desc, additional_details)
        selected_equipments.append(selected_equipments_for_task)

    return {"selected_equipments": selected_equipments}


def State_printer(State):
    # """print the State"""
    # print(
    #     "\n ########################################################################################################################## \n"
    # )
    # print("------------------State PRINTER----------------")
    # print("detailed_desc:", State["description"])
    # print("selected_crews:", State["selected_crews"])
    # print("equipments:", State["equipments"])
    # print("equipment_requirements:", State["equipment_requirements"])
    # print("selected_equipments:", State["selected_equipments"])
    print("\n ###### Equipment Project is finished! ###### \n")
    return

def EquipmentGraph(State: dict, state):
    # print("\n\n Inside Equipmentgraph ", state,"\n\n")
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
    


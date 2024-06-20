
# from langgraph.graph import END, StateGraph
# from typing import TypedDict, List, Annotated, Dict, Any

# class State(TypedDict):
#     num_steps: int
#     project_detail_from_customer: str
#     detailed_desc: str
#     roleJobTitles: List[str]
#     crew_requirements: List[dict]
#     queries: List[str]
#     selected_crews: List[dict]
#     equipments: List[str]
#     equipment_requirements: List[Dict]
#     selected_equipments: List[Dict]



# Finding out all unique equipments
def unique_equipments_getter(state: State):
    num_steps = int(state['num_steps'])
    num_steps += 1

    equipments = get_unique_equipments('equipment.db')
    return {"equipments": equipments, "num_steps": num_steps}


# Required Equipments from the data base
def equipment_requirement_getter(state: State):
    num_steps = int(state['num_steps'])
    num_steps += 1
    detailed_desc = state["detailed_desc"]
    equipments = state["equipments"]
    crew_requirement = state["crew_requirements"]

    equipment_requirements = get_equipment_requirements(
        crew_requirement, detailed_desc, equipments)
    return {
        "equipment_requirements": equipment_requirements,
        "num_steps": num_steps
    }

# Selcting the Equipments from the data base
def equipment_selection(state: State):
    num_steps = int(state['num_steps'])
    num_steps += 1

    detailed_desc = state["detailed_desc"]
    equipment_requirements = state["equipment_requirements"]
    crew_selected = state["selected_crews"]

    selected_equipments = []
    for equipment in equipment_requirements:
        filtered_equipment = filter_equipment(equipment["name"], 'Dubai','equipment.db')
        number_needed = equipment["number_needed"]
        # number_needed = 1
        equipmentName = equipment["name"]
        specification= equipment["Specification_required"]

        selected_equipments_for_task = get_selected_equipments(
            filtered_equipment, crew_selected, number_needed, equipmentName, specification, detailed_desc)
        selected_equipments.append(selected_equipments_for_task)

    return {"selected_equipments": selected_equipments, "num_steps": num_steps}


# def state_printer(state):
#     """print the state"""
#     print(
#         "\n ########################################################################################################################## \n"
#     )
#     print("------------------STATE PRINTER----------------")
#     print("num_steps:", state["num_steps"])
#     print("project_detail_from_customer:",
#           state["project_detail_from_customer"])
#     print("detailed_desc:", state["detailed_desc"])
#     print("roleJobTitles:", state["roleJobTitles"])
#     print("queries:", state["queries"])
#     print("selected_crews:", state["selected_crews"])
#     print("equipments:", state["equipments"])
#     print("equipment_requirements:", state["equipment_requirements"])
#     print("selected_equipments:", state["selected_equipments"])
#     return


workflow = StateGraph(State)
workflow.add_node("unique_equipments_getter", unique_equipments_getter)
workflow.add_node("equipment_requirement_getter", equipment_requirement_getter)
workflow.add_node("equipment_selection", equipment_selection)
# workflow.add_node("state_printer", state_printer)


workflow.add_edge("unique_equipments_getter", "equipment_requirement_getter")
workflow.add_edge("equipment_requirement_getter", "equipment_selection")
# workflow.add_edge("equipment_selection", "state_printer")

workflow.set_entry_point("unique_equipments_getter")
workflow.add_edge("equipment_selection", END)

app = workflow.compile()

project_detail_from_customer = "I need a 3D movie of a spaceship"
inputs = {
    "project_detail_from_customer": project_detail_from_customer,
    "num_steps": 0,
    "detailed_desc": "",
    "equipments": [],
    "selected_crews": [],
    "equipment_requirements": [],
    "queries": [],
    "equipments_selected": []
}

# for op in app.stream(inputs):
#     print(op)

def equipment_output(inputs):
    output = app.invoke(inputs)
    return output["equipments_selected"]

ans=equipment_output(inputs) 
print(ans)

# ans have all selected equipments in a json
# FRONTEND WORK STARTS HERE
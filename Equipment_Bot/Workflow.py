
from langgraph.graph import END, StateGraph
from typing import TypedDict, List, Annotated, Dict, Any


class State(TypedDict):
    num_steps: int
    project_detail_from_customer: str
    detailed_desc: str
    roleJobTitles: List[str]
    crew_requirements: List[dict]
    queries: List[str]
    selected_crews: List[dict]
    equipments: List[str]
    equipment_requirements: List[Dict]
    selected_equipments: List[Dict]


# description of the project
def detailed_desc_getter(State):
    num_steps = int(State['num_steps'])
    num_steps += 1
    project_detail_from_customer = State["project_detail_from_customer"]
    detailed_desc = get_detailed_desc(project_detail_from_customer)
    return {"detailed_desc": detailed_desc, "num_steps": num_steps}


# all the available crew roles
def unique_roles_getter(State):
    num_steps = int(State['num_steps'])
    num_steps += 1

    roleJobTitles = get_unique_roles('crewdata.db')
    return {"roleJobTitles": roleJobTitles, "num_steps": num_steps}


# break into crew requirements
def crew_requirement_getter(State):
    num_steps = int(State['num_steps'])
    num_steps += 1
    detailed_desc = State["detailed_desc"]
    roleJobTitles = State["roleJobTitles"]

    crew_requirements = get_crew_requirements(detailed_desc, roleJobTitles)
    return {"crew_requirements": crew_requirements, "num_steps": num_steps}


# break into queries
def queries_getter(State):
    num_steps = int(State['num_steps'])
    num_steps += 1
    crew_requirements = State["crew_requirements"]

    queries = get_queries(crew_requirements)
    return {"queries": queries, "num_steps": num_steps}


# check if all queries satisfied ----> planning to drop as I am structuring queries myself, for every requirement
# check if all queries are valid ----> planning to drop as I am structuring queries myself


# call to DB for all qualified enteries
def crew_selection(State):
    num_steps = int(State['num_steps'])
    num_steps += 1

    detailed_desc = State["detailed_desc"]
    crew_requirements = State["crew_requirements"]

    selected_crews = []
    for crew in crew_requirements:
        filtered_crew = filter_crew_members(crew["roleJobTitle"], 'Dubai',
                                            'crewdata.db')
        number_needed = crew["number_needed"]
        hiring_role = crew["roleJobTitle"]

        selected_crews_for_task = get_selected_crews(filtered_crew,
                                                     number_needed,
                                                     hiring_role,
                                                     detailed_desc)
        
        selected_crews.append({hiring_role:selected_crews_for_task})
        # found_crew = False
        # if selected_crews_for_task:
        #     selected_crews.append(selected_crews_for_task)
        #     found_crew = True  # Set flag to True if crew members were found
        # else:
        #     print(f"No suitable crew found for role: {hiring_role}")
        # if not found_crew:
        #     break


    return {"selected_crews": selected_crews, "num_steps": num_steps}


def unique_equipments_getter(state: State):
    num_steps = int(state['num_steps'])
    num_steps += 1

    equipments = get_unique_equipments('equipment.db')
    return {"equipments": equipments, "num_steps": num_steps}


# Selecting Equipment from the data base using a prompt
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

workflow.add_node("detailed_desc_getter", detailed_desc_getter)
workflow.add_node("unique_roles_getter", unique_roles_getter)
workflow.add_node("crew_requirement_getter", crew_requirement_getter)
workflow.add_node("queries_getter", queries_getter)
workflow.add_node("crew_selection", crew_selection)
workflow.add_node("unique_equipments_getter", unique_equipments_getter)
workflow.add_node("equipment_requirement_getter", equipment_requirement_getter)
workflow.add_node("equipment_selection", equipment_selection)
# workflow.add_node("state_printer", state_printer)


workflow.add_edge("detailed_desc_getter", "unique_roles_getter")
workflow.add_edge("unique_roles_getter", "crew_requirement_getter")
workflow.add_edge("crew_requirement_getter", "queries_getter")
workflow.add_edge("queries_getter", "crew_selection")
workflow.add_edge("crew_selection", "unique_equipments_getter")
workflow.add_edge("unique_equipments_getter", "equipment_requirement_getter")
workflow.add_edge("equipment_requirement_getter", "equipment_selection")
# workflow.add_edge("equipment_selection", "state_printer")

workflow.set_entry_point("detailed_desc_getter")
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
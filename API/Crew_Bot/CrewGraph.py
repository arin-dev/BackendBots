from .CrewFunctions import *
from langgraph.graph import END, StateGraph
from typing import TypedDict, List, Annotated
from .apikey import OPENAI_API_KEY
from crew.models import CrewMember, Project, CrewRequirement, SelectedCrew

def detailed_desc_getter(State, ):
    num_steps = int(State['num_steps'])
    num_steps += 1

    project_detail_from_customer = State["project_detail_from_customer"]

    detailed_desc = get_detailed_desc(project_detail_from_customer)
    return {"detailed_desc" : detailed_desc, "num_steps" : num_steps}


def unique_roles_getter(State):
    num_steps = int(State['num_steps'])
    num_steps += 1

    roleJobTitles = get_unique_roles('./DEMO_DB/crewdata.db')
    return {"roleJobTitles" : roleJobTitles, "num_steps" : num_steps}

def crew_requirement_getter(State):
    num_steps = int(State['num_steps'])
    num_steps += 1
    detailed_desc = State["detailed_desc"]
    roleJobTitles = State["roleJobTitles"]

    crew_requirements = get_crew_requirements(detailed_desc, roleJobTitles)
    return {"crew_requirements" : crew_requirements, "num_steps" : num_steps}


def queries_getter(State):
    num_steps = int(State['num_steps'])
    num_steps += 1
    crew_requirements = State["crew_requirements"]

    queries = get_queries(crew_requirements)
    return {"queries" : queries, "num_steps" : num_steps}


def crew_selection(State):
    num_steps = int(State['num_steps'])
    num_steps += 1

    detailed_desc = State["detailed_desc"]
    crew_requirements = State["crew_requirements"]
    # print("crew_requirements:", crew_requirements)
    selected_crews = []
    for crew in crew_requirements:
        filtered_crew = filter_crew_members(crew["roleJobTitle"], 'Dubai')
        number_needed = crew["number_needed"]
        hiring_role = crew["roleJobTitle"]

        selected_crews_for_task = get_selected_crews(filtered_crew, number_needed, hiring_role, detailed_desc)
        selected_crews.append({hiring_role:selected_crews_for_task})
    # print("\n\n\n ############# \n\n\n")
    # print("selected_crews:", selected_crews)


    ## selected_crews = get_selected_crew_details(selected_crews_filtering)
    return {"selected_crews" : selected_crews, "num_steps" : num_steps}

    
def state_printer(state):
    # print("num_steps:", state["num_steps"])
    # print("project_detail_from_customer:", state["project_detail_from_customer"])
    # print("detailed_desc:", state["detailed_desc"])
    # print("roleJobTitles:", state["roleJobTitles"])
    # print("queries:", state["queries"])
    # print("selected_crews:", state["selected_crews"])
    print("Project is finished!")
    return


def CrewGraph(State: dict, project_detail_from_customer: str):

    workflow = StateGraph(State)

    workflow.add_node("detailed_desc_getter", detailed_desc_getter)
    workflow.add_node("unique_roles_getter", unique_roles_getter)
    workflow.add_node("crew_requirement_getter", crew_requirement_getter)
    workflow.add_node("queries_getter", queries_getter)
    workflow.add_node("crew_selection", crew_selection)
    workflow.add_node("state_printer", state_printer)

    workflow.add_edge("detailed_desc_getter", "unique_roles_getter")
    workflow.add_edge("unique_roles_getter", "crew_requirement_getter")
    workflow.add_edge("crew_requirement_getter", "queries_getter")
    workflow.add_edge("queries_getter", "crew_selection")
    workflow.add_edge("crew_selection", "state_printer")

    workflow.set_entry_point("detailed_desc_getter")
    workflow.add_edge("state_printer", END)

    app = workflow.compile()

    inputs = {"project_detail_from_customer": project_detail_from_customer,"num_steps":0}

    var = app.invoke(inputs)
    return var
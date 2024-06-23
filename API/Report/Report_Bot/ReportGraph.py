from .ReportFunctions import *
from langgraph.graph import END, StateGraph
from typing import TypedDict, List, Annotated
from equipment.models import Equipment, Provider, Availability

def crew_report_call(report_state):
    sel_crew = report_state["selected_crews"]
    crewreport = crew_report(sel_crew)
    # print("inside crew is ",report_state)
    report_state["crew_report"]=crewreport
    return report_state

def equipment_report_call(report_state):
    # print("Inside equipment_report_call, report_state:", report_state)
    sel_equip = report_state["selected_equipments"]
    equipreport = equipment_report(sel_equip)
    report_state["equipment_report"]=equipreport
    return report_state

def State_printer(report_state):
    """print Report State"""
    print(
        "\n ########################################################################################################################## \n"
    )
    print("crew_report", report_state["crew_report"])
    print("equipment_report", report_state["equipment_report"])
    return

def ReportGraph(report_state):
    print("\n\n Inside Reportgraph ", report_state,"\n\n")
    workflow = StateGraph(report_state)
    workflow.add_node("crew_report_call", crew_report_call)
    workflow.add_node("equipment_report_call", equipment_report_call)
    workflow.add_node("State_printer", State_printer)


    workflow.add_edge("crew_report_call", "equipment_report_call")
    workflow.add_edge("equipment_report_call", "State_printer")

    workflow.set_entry_point("crew_report_call")
    workflow.add_edge("State_printer", END)

    app = workflow.compile()

    output = app.invoke(report_state)
    return output
    



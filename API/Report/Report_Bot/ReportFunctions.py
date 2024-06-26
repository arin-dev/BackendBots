import sqlite3
import json
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from project.models import Project

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


# For LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0.2, api_key=OPENAI_API_KEY)
# For LLM that returns json
llm_json = ChatOpenAI(model="gpt-4o", temperature=0.2, api_key=OPENAI_API_KEY).bind(response_format={"type": "json_object"})



def crew_report(crew_selected):
        prompt_crew_report = f"""You are an experienced film production assistant and an expert in planning and organizing film crews. Here you are provided with some selected crew:{crew_selected}. Your task is to generate a crew report, which contain name, userid, age, gender, driving_licence(boolean value True or False) of the crew selected. The selected crew data already have name and userid, but age, gender, dridriving_licence are not present in the given data so you have to generate it. Value of driving licence should be in boolean format that is either True or False. gender should be based on their names.
        Output must be in JSON format and should contain only the following fields :[name, userid, age,gender,driving_licence]"""
        messages = [
            ("system", prompt_crew_report),
            ("user", f"This is selected crew from user : {crew_selected}."),
        ]
        response = llm_json.invoke(messages)
        crewreport = json.loads(response.content)
        print("\n\n Crew Report is:  ",crewreport,"\n")
        return crewreport

def equipment_report(equipment_selected):
        prompt_equipment_report = f"""You are an experienced film production assistant and an expert in planning and organizing film crews. Here you are provided with some selected selected:{equipment_selected}. Your task is to generate a equipment report, which contain name, brand, model, cost(cost of the equipment), size(length*breath*height), sensitive(low/medium/high) of the equioment selected. The selected equioment data already have name, brand and model but cost, size are not present in the given data so you have to generate it. Value of cost is how much that equipment will cost to buy in us dollar with a dollar symbol(like $100). Value of size shold be in length*breath*height format, where each dimension should be in centimeter(like: 10cm*25cm*35cm). Value of sensitiveness sholud be low, medium or high.
        Output must be in JSON format and should contain only the following fields :[name, brand, model, cost, size, sensitive]"""
        messages = [
            ("system", prompt_equipment_report),
            ("user", f"This is selected equipment from user : {equipment_selected}."),
        ]
        response = llm_json.invoke(messages)
        equipmentreport = json.loads(response.content)
        print("\n\n Equipment Report is:  ",equipmentreport,"\n")
        return equipmentreport


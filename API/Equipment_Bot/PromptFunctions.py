import sqlite3
import json
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from crew.models import CrewMember, CrewRequirement, SelectedCrew
from equipment.models import Equipment, EquipmentRequirement, SelectedEquipments
from project.models import Project

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


# For LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0.2, api_key=OPENAI_API_KEY)
# For LLM that returns json
llm_json = ChatOpenAI(model="gpt-4o", temperature=0.2, api_key=OPENAI_API_KEY).bind(response_format={"type": "json_object"})

def filter_equipment(name, location):
    equipment_details = Equipment.objects.filter(name=name, location=location)
    filtered_data = []
    for ele in equipment_details:
        filtered_data.append({
        "name": ele.name,
        "Type": ele.Type,
        "brand": ele.brand,
        "model": ele.model,
        "resolution": ele.resolution,
        "frame_rate": ele.frame_rate,
        "sensor_type": ele.sensor_type,
        # "connectivity": ele.connectivity.split(', ') if ele.connectivity else None,
        "connectivity": ele.connectivity,
        # "audio_input": ele.audio_input.split(', ') if ele.audio_input else None,
        "audio_input": ele.audio_input,
        "battery_life": ele.battery_life,
        "weight": ele.weight,
        # "accessories": ele.accessories.split(', ') if ele.accessories else None,
        "accessories": ele.accessories,
        "rental_price_per_day": ele.rental_price_per_day,
        "provider": ele.provider,
        "availability": ele.availability,
        "height_range": ele.height_range,
        "weight_capacity": ele.weight_capacity,
        "material": ele.material,
        # "inputs": ele.inputs.split(', ') if ele.inputs else None,
        "inputs": ele.inputs,
        "output": ele.output,
        "resolution_support": ele.resolution_support,
        "control_interface": ele.control_interface,
        "wireless": ele.wireless,
        "frequency_range": ele.frequency_range,
        "frequency_response": ele.frequency_response,
        "transmitter_battery_life": ele.transmitter_battery_life,
        "transducer_type": ele.transducer_type,
        "directionality": ele.directionality,
        "channels": ele.channels,
        "effects": ele.effects,
        "speaker_type": ele.speaker_type,
        "power_rating": ele.power_rating,
        "light_type": ele.light_type,
        "power": ele.power,
        "color_temperature": ele.color_temperature,
        "brightness": ele.brightness,
        "dimensions": ele.dimensions,
        "shape": ele.shape,
        "diffuser_type": ele.diffuser_type,
        "mount_type": ele.mount_type,
        "sections": ele.sections,
        "features": ele.features,
        "speed": ele.speed,
        "cable_type": ele.cable_type,
        "length": ele.length,
        "bandwidth": ele.bandwidth,
        "range": ele.range,
        "screen_size": ele.screen_size,
        "compatibility": ele.compatibility,
        "processor": ele.processor,
        "memory": ele.memory,
        "storage": ele.storage,
        "power_capacity": ele.power_capacity,
        "battery_runtime": ele.battery_runtime,
        "graphics_card": ele.graphics_card,
        "license_type": ele.license_type,
        "media_support": ele.media_support,
        "interface": ele.interface,
        "capacity": ele.capacity,
        "load_capacity": ele.load_capacity,
        "location": ele.location
    })
    # print(filtered_data)
    return filtered_data

def get_unique_equipments():
    equips = Equipment.objects.values_list('name', flat=True).distinct()
    return list(equips)

def get_equipment_requirements(crew_requirements, detailed_desc, additional_details, name,ai_suggestions,user_equipment_requirements):
    if ai_suggestions:
        prompt_equipment_requirement_getter = f"""You are an experienced film production assistant and an expert in planning and organizing film crews. Your task is to provide a comprehensive list of the equipment required to complete a film production project based on the details provided by the user. This includes identifying all essential equipment, detailing their primary responsibilities, and specifying the number of individuals needed for each specific role. Here is the crew requirement: {crew_requirements}. Now you need to provide the equipment required for the project that is well-suited to the crew requirements. Note that if the project is to be done in multiple locations, we might need equipment at multiple locations or we might transport equipment between locations. Understand the requirements and give output accordingly.
        
        Each crew member's role requires specific equipment. Here are some examples of the role-to-equipment mapping:

        - Producer: ["Laptops/Computers", "High-Speed Internet"]
        - Director: ["Teleprompter", "Laptops/Computers", "Walkie-talkies"]
        - Technical Director: ["Camera Switcher", "Streaming Encoder", "High-Speed Internet"]
        - Camera Operator: ["broadcast_camera", "Tripods and Mounts", "HDMI/SDI Cables"]
        - Sound Engineer: ["Lavalier Mics", "Handheld Mics", "Boom Mics", "Audio Mixer", "XLR Cables"]

        Based on these examples and the provided project details and crew requirements, generate a comprehensive list of equipment requirements.
        Output must be in JSON format and should contain only the following fields :[name, number_needed, Specification_required,location]"""
        messages = [
            ("system", prompt_equipment_requirement_getter),
            ("user", f"This is the project details from user : {detailed_desc}. This is the additional details you have to consider: {additional_details}"),
            ("user",
            f"Make sure that all equipment chosen must only be from these: {name}."
            )
        ]
        response = llm_json.invoke(messages)
        equipment_requirements = json.loads(response.content)
        try:
            equipment_requirements = equipment_requirements["equipment"]
        except:
            equipment_requirements = equipment_requirements
        return equipment_requirements
    else:
        prompt_equipment_requirement_getter = f"""You are an experienced film production assistant and an expert in planning and organizing film crews. Your task is to provide a comprehensive list of the equipment required to complete a film production project based on the details provided by the user. This includes identifying all essential equipment, detailing their primary responsibilities, and specifying the number of individuals needed for each specific role. Here user already provided the list of equipments he wants. Here is the equipment requirement by user: {user_equipment_requirements}.
        User only provided the equipment name and number of equipment needed, you have to generate and add Specification_required and location for equipment.Note that if the project is to be done in multiple locations, we might need equipment at multiple locations or we might transport equipment between locations. Understand the requirements and give output accordingly.
        
        Output must be in JSON format and should contain only the following fields :[name, number_needed, Specification_required,location]"""
        messages = [
            ("system", prompt_equipment_requirement_getter),
            ("user", f"This is the project details from user : {detailed_desc}. This is the additional details you have to consider: {additional_details}. Add all equipment provided by user in your output with provided structure. Equipment provided by user are:{user_equipment_requirements}"),
            ("user",
            f"Make sure that all equipment chosen must only be from these: {name}."
            )
        ]
        response = llm_json.invoke(messages)
        equipment_requirements = json.loads(response.content)
        # print("\n\n prompting func ", equipment_requirements,"\n\n")
        
        try:
            equipment_requirements = equipment_requirements["equipment"]
        except:
            equipment_requirements = equipment_requirements
        return equipment_requirements


def get_selected_equipments(filtered_equipment, crew_selected, number_needed,
                            equipmentName, specification, detailed_desc,additional_details):
    # print("\n Inside selection ", filtered_equipment, "    ",equipmentName,"\n\n")
    
    prompt_equipment_selection = f"""
     You are the HR in our firm, responsible for selecting the best possible equipment for our projects. Your subordinates will provide you with the project details, including the required equipment and the quantity needed. Based on this information and the selected crew for the project, you need to choose the most suitable equipment and explain your preference.
     Here’s what you need to consider:
     Select equipement according to the specification needed. Here is the datails about their specification: {specification}.
     Match Equipment to Crew: Select equipment that best fits the crew's roles and the number of crew members. For example, if we need to shoot a scene from two different angles and have equal to or more than two camera operators, we can select two cameras. However, if there is only one camera operator, you should select only one camera.
     Assign Equipment Accordingly: Ensure that the equipment is suitable for the crew members available. If a specific piece of equipment requires a specific crew member and none are available, try to assign it to another crew member. If no one can operate it, exclude that equipment.
     Rationale for Selection: Make sure to explain why you prefer a particular piece of equipment. This could be based on compatibility, ease of use, the specific needs of the project, or the capabilities of the crew.
     The output should be in JSON format which should follow this: ['name', 'model', 'brand', 'number_needed', 'Preferred_because', 'provider_email']. Only output JSON. You don't need to put anything extra as your output will be directly fed to a function, so just output JSON.
    """
    messages = [
        ("system", prompt_equipment_selection),
        ("user",
         f"Following is the list of available equipment for the project: {filtered_equipment}, you need to procure {number_needed} pieces of equipment, for the purpose of {equipmentName} for this project: {detailed_desc}. Here is some additional details you have to consider further: {additional_details}"
         ),
        ("user",
         f"Make sure that all equipment chosen must be well fitted to the crew selected. Selected crew are these: {crew_selected}. Only give 5 most important equipment in output."
         )
    ]

    response = llm_json.invoke(messages)
    selected_equipments = json.loads(response.content)
    return selected_equipments
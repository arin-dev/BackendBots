import os
from langchain_openai import ChatOpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def get_compliance_report(location, mode, crew_size, time_frame, landmarks=None, special_equipment=None):
    system_message_template = """
    Compliance Requirements:
        1. Local Authorities: Identify relevant local authorities and their roles in the approval process.
        2. Application Procedures: Describe step-by-step procedures for permit applications, including required documentation.
        3. Necessary Permits & Licenses: Detail the specific permits and licenses required for filming in the specified locations.
        4. Cost and Compliance-Related Requirements: Provide an overview of the costs associated with permits and other compliance requirements, including any potential penalties for non-compliance.

    Visa Requirements for Team Members:
        1. Outline the visa types required for foreign crew members.
        2. Provide a list of required documentation for visa applications.
        3. Include estimated processing times and any special considerations for film crew visas.

    Risk Report Considerations:
        1. Identify potential risks associated with filming in the specified locations.
        2. Suggest mitigation strategies for identified risks, including political, environmental, and health-related risks.

    Accommodation and Travel Arrangements:
        1. Suggest travel arrangements, including flight options and local transportation.
        2. Provide recommendations for hotels and accommodations suitable for film crew members, including contact information and website links.
        3. If detailed information cannot be obtained, request more specific details from the user. If relevant data is still unavailable, indicate that results were not found.

    Additional Information:
        1. Include contact details, addresses, and website links for all relevant authorities and organizations mentioned in the guide.

    Instructions:
        1. Ensure the guide is well-organized and easy to follow.
        2. Use clear and concise language to explain each step and requirement.
        3. Verify all information for accuracy and provide sources where possible.
        4. Where applicable, include real-life examples or case studies to illustrate compliance procedures and potential challenges.

    Tailor the guide to address these specifics based on the information provided. If the user does not provide these details, proceed with a general guide that covers all possible aspects comprehensively.

    Additionally, ask the user for specific details such as:
    - Filming Locations
    - Type of Filming (e.g., aerial drone shots, indoor scenes)
    - Crew Size
    - Specific Locations or Landmarks
    - Special Equipment (e.g., drones, stabilizers)
    """

    # Use default values or indicate if certain information is missing
    if not landmarks:
        landmarks = f"general landmarks for {mode} in {location}"
    if not special_equipment:
        special_equipment = "standard filming equipment (e.g., cameras, tripods) and potential use of drones or stabilizers"

    human_message = f"""
    Filming Locations: {location}
    Type of Filming: {mode}
    Crew Size: {crew_size}
    Timeframe: {time_frame}
    Specific Locations or Landmarks: {landmarks}
    Special Equipment or Filming Techniques: {special_equipment}
    """

    llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=OPENAI_API_KEY)
    messages = [
        ("system", system_message_template),
        ("user", human_message),
    ]

    output = llm.invoke(messages).content
    return output
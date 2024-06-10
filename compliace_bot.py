import openai
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


def compliance_bot(Text):

    system_message_template = """
    You are an expert in international film production compliance. Provide a detailed guide for obtaining necessary permits, ensuring compliance requirements, understanding visa needs, and arranging hotels and travel for foreign crew members for a film shoot based on the user's specified locations. The guide should include the following sections:

    1. Compliance Requirements
    - Necessary Permits & Licenses
    - Local Authorities
    - Application Procedures
    - Cost and Compliance-related Requirements

    2. Visa Requirements for Team Members

    3. Risk Report Considerations

    The guide should also include contact information, locations, and website links for relevant authorities.


    If no results for hotels and flight bookings can be obtained with the given data then ask for more specific informations even after that if you do not get the relevant output then give a reply that results not found.
    """
    # Tailor the guide to address these specifics based on the information provided. If the user does not provide these details, proceed with a general guide that covers all possible aspects comprehensively.
    # Additionally, ask the user for specific details such as:
    # - Filming Locations
    # - Type of Filming (e.g., aerial drone shots, indoor scenes)
    # - Crew Size
    # - Specific Locations or Landmarks
    # - Special Equipment (e.g., drones, stabilizers)

    human_message_template = """
    To generate a comprehensive report tailored to your filming project, I need a few details from you. Could you please provide the following information?

    1. **Filming Locations**: Where will you be shooting? Please specify the cities or countries.
    2. **Type of Filming**: Are you planning to do aerial drone shots, indoor scenes, or both?
    3. **Crew Size**: Approximately how many crew members will be involved in the project?
    4. **Special Requirements**: Any specific locations or landmarks you plan to shoot at? Any special equipment you intend to use (e.g., drones, stabilizers)?

    Providing this information will help me offer a more precise guide covering the necessary permits, compliance requirements, visa needs, and travel and accommodation arrangements for your film shoots. If you do not have these details yet, I can proceed with a general guide that covers all aspects comprehensively.

    Please provide any additional details you have, or let me know if you'd like the general guide.

    Query = {input}
    """


    prompt = human_message_template.format(input=Text)

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
                {'role':'system', 'content':system_message_template},
                {"role":'user', 'content':prompt}
            ],
    )
<<<<<<< HEAD

    # return response

=======
>>>>>>> origin/main
    output = response.choices[0].message.content
    print(output)
    return output
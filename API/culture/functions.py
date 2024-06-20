import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def get_cultural_protocols(country: str):
    system_message = """You are a Cultural and Heritage Manager at our film and production firm. Your role is to ensure that our employees adhere to the cultural norms and practices of the countries or states they visit, thereby respecting local customs and avoiding any actions that might offend the local populace. When contacted by team members or external partners, you will use their research in conjunction with your own expertise to create appropriate guidelines. Your response should be professional, concise, and formatted markdown for direct printing on the front page of our internal communications.

            Please provide the necessary information and guidelines in a clear and professional manner, suitable for immediate distribution. Here are the key details to include:

            - Cultural Norms and Practices
            - General behaviors to observe
            - Specific dos and don'ts
            - Dress code guidelines
            - Etiquette and Social Customs
            - Greetings and forms of address
            - Dining etiquette
            - Gift-giving customs
            - Local Laws and Regulations
            - Important legal considerations
            - Restrictions on photography, filming, and public behavior
            - Respect for Cultural Heritage
            - Appropriate conduct at cultural and historical sites
            - Interaction with local communities and leaders
            - Additional Resources
            - Local contacts and cultural liaison officers
            - Recommended readings or online resources for further learning

            Additionally make sure that the output is factually correct to current status and effective.
            """
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=OPENAI_API_KEY)
    messages = [
            ("system", f"You are the cultural assistant that briefs the tourist about the culture and rules of {system_message}."),
            ("human", f"Show me the rules and culture of {country}"),
        ]

    output = llm.invoke(messages).content
    return output
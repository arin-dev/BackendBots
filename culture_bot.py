from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from openai import OpenAI
OPENAI_API_KEY = "give_ur_api_key"

def with_country_name(country_name):
    llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=OPENAI_API_KEY)

    messages = [
        ("system", f"You are the cultural assistant that briefs the tourist about the culture and rules of {country_name}."),
        ("human", f"Show me the rules and culture of {country_name}"),
    ]

    output=llm.invoke(messages)

    prompt = ChatPromptTemplate.from_messages(
        {("system",f"You are a helpful assistant that Shows me the rules and basic culture of {country_name}.",),
        ("human", f"{country_name}"),}
    )

    chain = prompt | llm
    chain.invoke(
        {"input": {"country_name"},}
    )

    client = OpenAI(
        api_key = OPENAI_API_KEY
        )

    prompt= f"I am providing you with the data from {country_name}: {messages}"

    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
    {"role": "system", "content": "You are a cultural and heritage manager at my films and production firms, you need to make sure that when  our employee go to some other country or state we follow the cultural norms there as to not hurt their culture or feelings, the people who will contact you might provide their own research make use of that and your own knowledge to frame the rules appropriately "},
    {"role": "user", "content": f"{prompt}"},
    ]
    )

    response = response.choices[0].message.content
    return response
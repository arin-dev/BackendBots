import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from openai import OpenAI
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def CultureBot(countries: list[str]):
    responses = []
    for country in countries:
        llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=OPENAI_API_KEY)
        messages = [
            ("system", f"You are the cultural assistant that briefs the tourist about the culture and rules of {country}."),
            ("human", f"Show me the rules and culture of {country}"),
        ]

        output=llm.invoke(messages).content

        # print(output)
        client = OpenAI(
            api_key = OPENAI_API_KEY
            )

        prompt= f"I am providing you with the data from {country}: {output}"

        response = client.chat.completions.create( model="gpt-4o",
        messages=[
        {"role": "system", "content": "You are a cultural and heritage manager at my films and production firms, you need to make sure that when  our employee go to some other country or state we follow the cultural norms there as to not hurt their culture or feelings, the people who will contact you might provide their own research make use of that and your own knowledge to frame the rules appropriately. You need to give the data such that it can be passed on direclty for printing on frintpage so keep complete answer professional and neat"},
        {"role": "user", "content": f"{prompt}"},
        ]
        )

        response = response.choices[0].message.content
        responses.append({country: response})
    return responses

import pprint
pprint.pprint(CultureBot(["USA", "Canada"]), width=100)
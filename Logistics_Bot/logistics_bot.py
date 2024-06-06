import os
import json
import openai
import requests
from datetime import datetime
from dotenv import load_dotenv
from Flight_PDF_Generator import ItineraryPDFGenerator
from Hotel_PDF_Generator import HotelPDFGenerator

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")
x_rapid_api_Key = os.environ.get("X_RapidAPI_Key")

user_input = input().strip()

prompt_template = """
Extract the following information and adhere strictly to the given output format:
1. Start Location
2. End Location
3. Start Date
4. End Date
5. Count of Crew Members

Text: {text}

Please provide the output in the exact format below:

1. Start Location:
2. End Location:
3. Start Date:
4. End Date:
5. Count of Crew Members:
"""

def extract_travel_information(text):
    prompt = prompt_template.format(text=text)
    
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {'role':'system', 'content':'The system message is usually a guiding prompt that sets the context for the model, outlining the task and what it should focus on. This helps in obtaining a more structured and relevant response from the model.'},
            {"role":'user', 'content':prompt}
        ],
    )

    with open("chat_response.json", 'w', encoding='utf-8') as file:
        json.dump(response.model_dump_json(), file, indent=4)

    response_text = response.choices[0].message.content
    lines = response_text.split('\n')
    # print(lines)
    start_location = lines[0].split("Start Location:")[1].strip()
    end_location = lines[1].split("End Location:")[1].strip()
    start_date = lines[2].split("Start Date:")[1].strip()
    end_date = lines[3].split("End Date:")[1].strip()
    crew_members = lines[4].split("Count of Crew Members:")[1].split()[0].strip()

    
    return start_location, end_location, start_date, end_date, crew_members

start_location, end_location, start_date, end_date, crew_members = extract_travel_information(user_input)
# print(start_location)
# print(end_location)
# print(start_date)
# print(end_date)
# print(start_location_airport_code)
# print(end_location_airport_code)
# print(crew_members)

def format_date(date_str):
    try:
        parsed_date = datetime.strptime(date_str, '%B %d')
        formatted_date = parsed_date.replace(year=datetime.now().year).strftime('%Y-%m-%d')
    except ValueError as e:
        print(f"Error parsing date: {e}")
        formatted_date = date_str
    return formatted_date

start_date = format_date(start_date)
end_date = format_date(end_date)

# print(start_date)
# print(end_date)


# Searching Flight ID

flightID_url = "https://sky-scanner3.p.rapidapi.com/flights/auto-complete"
flightID_headers = {
	"X-RapidAPI-Key": x_rapid_api_Key,
	"X-RapidAPI-Host": "sky-scanner3.p.rapidapi.com"
}

flightID_querystring = {"query":start_location}
flightID_response = requests.get(flightID_url, headers=flightID_headers, params=flightID_querystring)
fromID = flightID_response.json()['data'][0]['presentation']['skyId']

flightID_querystring = {"query":end_location}
flightID_response = requests.get(flightID_url, headers=flightID_headers, params=flightID_querystring)
toID = flightID_response.json()['data'][0]['presentation']['skyId']


# print(flightID_response)
# print(fromID)
# print(toID)

## Searching for Flights

flight_url = "https://sky-scanner3.p.rapidapi.com/flights/search-roundtrip"
flight_querystring = {"fromEntityId":fromID, "toEntityId":toID, "departDate":start_date, "returnDate":end_date, "currency":"USD"}
flight_headers = {
	"X-RapidAPI-Key": x_rapid_api_Key,
	"X-RapidAPI-Host": "sky-scanner3.p.rapidapi.com"
}
flight_response = requests.get(flight_url, headers=flight_headers, params=flight_querystring)
# print("\n\n##################### FLIGHT JSON ################################\n\n")
# print(flight_response.json())
# print("\n\n")

with open("flight.json", 'w', encoding='utf-8') as flight_file:
    json.dump(flight_response.json(), flight_file, indent=4)
    

generator = ItineraryPDFGenerator(flight_response.json())
generator.generate_pdf("Flight_Data.pdf")



## Searching for Hotels


hotelID_url = "https://sky-scanner3.p.rapidapi.com/hotels/auto-complete"
hotelID_querystring = {"query":end_location}
hotelID_headers = {
	"X-RapidAPI-Key": x_rapid_api_Key,
	"X-RapidAPI-Host": "sky-scanner3.p.rapidapi.com"
}
hotelID_response = requests.get(hotelID_url, headers=hotelID_headers, params=hotelID_querystring)
# print(hotelID_response.json())


entity_ID = hotelID_response.json()['data'][0]['entityId']


hotel_url = "https://sky-scanner3.p.rapidapi.com/hotels/search"
hotel_querystring = {"entityId":entity_ID,"checkin":start_date,"checkout":end_date}
hotel_headers = {
	"X-RapidAPI-Key": x_rapid_api_Key,
	"X-RapidAPI-Host": "sky-scanner3.p.rapidapi.com"
}
hotel_response = requests.get(hotel_url, headers=hotel_headers, params=hotel_querystring)

with open("hotel.json", 'w', encoding='utf-8') as hotel_file:
    json.dump(hotel_response.json(), hotel_file, indent=4)


pdf_generator = HotelPDFGenerator(hotel_response.json())
pdf_generator.generate_pdf()
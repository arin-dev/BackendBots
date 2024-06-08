import os
import json
import openai
import requests
from datetime import datetime
from dotenv import load_dotenv
from functions import process_flight_data, process_hotel_data, process_taxi_data, find_entity_id

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
6. Start location airport code
7. End location airport code

Text: {text}

Please provide the output in the exact format below:

1. Start Location:
2. End Location:
3. Start Date:
4. End Date:
5. Count of Crew Members:
6. Start location airport code:
7. End location airport code:
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
    start_location = lines[0].split("Start Location:")[1].strip()
    end_location = lines[1].split("End Location:")[1].strip()
    start_date = lines[2].split("Start Date:")[1].strip()
    end_date = lines[3].split("End Date:")[1].strip()
    crew_members = lines[4].split("Count of Crew Members:")[1].split()[0].strip()
    start_location_airport_code = lines[5].split("Start location airport code:")[1].strip()
    end_location_airport_code = lines[6].split("End location airport code:")[1].strip()

    return start_location, end_location, start_date, end_date, crew_members, start_location_airport_code, end_location_airport_code

start_location, end_location, start_date, end_date, crew_members, start_location_airport_code, end_location_airport_code = extract_travel_information(user_input)

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



## Searching for Flights
flight_url = "https://sky-scanner3.p.rapidapi.com/flights/search-roundtrip"
flight_querystring = {"fromEntityId":start_location_airport_code, "toEntityId":end_location_airport_code, "departDate":start_date, "returnDate":end_date, "currency":"USD"}
flight_headers = {
	"X-RapidAPI-Key": x_rapid_api_Key,
	"X-RapidAPI-Host": "sky-scanner3.p.rapidapi.com"
}
flight_response = requests.get(flight_url, headers=flight_headers, params=flight_querystring)
simplified_flight_response = process_flight_data(flight_response.json())    #returns a JSON format data (format given in Example_Output/Flight_Data.json)



entity_id, date, time, drop_time = find_entity_id(flight_response.json(), end_location_airport_code)



## Searching for Hotels
hotel_url = "https://sky-scanner3.p.rapidapi.com/hotels/search"
hotel_querystring = {"entityId":entity_id,"checkin":date,"checkout":end_date}
hotel_headers = {
	"X-RapidAPI-Key": x_rapid_api_Key,
	"X-RapidAPI-Host": "sky-scanner3.p.rapidapi.com"
}
hotel_response = requests.get(hotel_url, headers=hotel_headers, params=hotel_querystring)
simplified_hotel_response = process_hotel_data(hotel_response.json())



## Searching for Taxi
taxi_url = "https://sky-scanner3.p.rapidapi.com/cars/search"
taxi_querystring = {"pickUpEntityId":entity_id,  "pickUpDate":date, "pickUpTime":time, "dropOffDate":date, "dropOffTime":drop_time}
taxi_headers = {
	"x-rapidapi-key": x_rapid_api_Key,
	"x-rapidapi-host": "sky-scanner3.p.rapidapi.com"
}
taxi_response = requests.get(taxi_url, headers=taxi_headers, params=taxi_querystring)
simplified_taxi_response = process_taxi_data(taxi_response.json())
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
x_rapid_api_Key = os.environ.get("X_RapidAPI_Key")


def process_flight_data(input_json_data):
    # Function to reformat JSON data
    def reformat_json(data):
        simplified_data = {
            "status": data["status"],
            "message": data["message"],
            "data": {
                "itineraries": []
            }
        }
        for itinerary in data["data"]["itineraries"][:3]:  # Limit to top 5 results
            leg = itinerary["legs"][0]
            departure_datetime = datetime.fromisoformat(leg["departure"])
            arrival_datetime = datetime.fromisoformat(leg["arrival"])
            new_itinerary = {
                "price": itinerary["price"]["formatted"],
                "departure": {
                    "date": departure_datetime.date().isoformat(),
                    "time": departure_datetime.time().isoformat()
                },
                "arrival": {
                    "date": arrival_datetime.date().isoformat(),
                    "time": arrival_datetime.time().isoformat()
                },
                "origin": f'{leg["origin"]["city"]} ({leg["origin"]["displayCode"]})',
                "destination": f'{leg["destination"]["city"]} ({leg["destination"]["displayCode"]})'
            }           
            tags = itinerary.get("tags")
            if tags:
                new_itinerary["tags"] = tags                
            simplified_data["data"]["itineraries"].append(new_itinerary)       
        return simplified_data
    # Reformat the JSON data
    simplified_json = reformat_json(input_json_data)
    return json.dumps(simplified_json, indent=4)



def find_entity_id(data, destination_id):
    itineraries = data.get("data", {}).get("itineraries", [])
    result = []
    for itinerary in itineraries:
        for leg in itinerary.get("legs", []):
            if leg.get("destination", {}).get("id") == destination_id:
                result.append(leg.get("destination", {}).get("entityId"))
                result.append(leg.get("arrival"))
                entity_id = result[0]
                arrival = result[1]
                date, time = arrival.split('T')
                time = time[:-3]               
                # Calculating drop_time by adding 3 hours
                hours, minutes = time.split(':')
                new_hours = int(hours) + 3                
                # Formatting hours to ensure they are in 'HH' format
                drop_time = f"{new_hours:02d}:{minutes}"               
                return entity_id, date, time, drop_time



def process_hotel_data(input_json_data):
    relevant_data = {
        "searchSummary": {
            "total": input_json_data["data"]["results"]["searchSummary"].get("total"),
            "resultsSummary": input_json_data["data"]["results"]["searchSummary"].get("resultsSummary")
        },
        "hotelsRegion": {
            "latitude": input_json_data["data"]["results"]["hotelsRegion"].get("latitude"),
            "longitude": input_json_data["data"]["results"]["hotelsRegion"].get("longitude")
        },
        "hotelCards": []
    }
    top_5_hotel_cards = input_json_data["data"]["results"]["hotelCards"][:3]
    for hotel in top_5_hotel_cards:
        if hotel["reviewsSummary"]:
            relevant_hotel_info = {
                "name": hotel.get("name"),
                "stars": hotel.get("stars"),
                "distance": hotel.get("distance"),
                "reviewsSummary": {
                    "score": hotel["reviewsSummary"].get("score"),
                    "scoreDesc": hotel["reviewsSummary"].get("scoreDesc"),
                    "total": hotel["reviewsSummary"].get("total")
                },
                "lowestPrice": hotel["lowestPrice"].get("price"),
                "images": hotel.get("images", [])
            }
        else:
            relevant_hotel_info = {
                "name": hotel.get("name"),
                "stars": hotel.get("stars"),
                "distance": hotel.get("distance"),
                "reviewsSummary": None,
                "lowestPrice": hotel["lowestPrice"].get("price"),
                "images": hotel.get("images", [])
            }
        relevant_data["hotelCards"].append(relevant_hotel_info)
    # Output the formatted JSON
    reduced_json = json.dumps(relevant_data, indent=4)
    return reduced_json



def process_taxi_data(input_json_data):
    def combined_metric(provider):
        # Combine reviews and rating to create a merit score (could be adjusted as needed)
        reviews = provider.get('reviews', 0)
        rating = provider.get('rating', 0)
        return reviews * rating
    # Filter to keep only providers with non-null reviews and ratings
    valid_providers = [provider for provider in input_json_data["data"]["providers"].values() if provider.get('reviews') is not None and provider.get('rating') is not None]
    # Sort providers based on the combined metric
    top_providers = sorted(valid_providers, key=combined_metric, reverse=True)[:3]
    # Prepare the relevant data
    relevant_data = {
        "status": input_json_data["status"],
        "message": input_json_data["message"],
        "data": {
            "top_providers": top_providers
        }
    }
    # Save the reformatted JSON
    formatted_json = json.dumps(relevant_data, indent=4)
    return formatted_json



def get_logistics_details(destination, start_date, end_date):
    # def extract_travel_information(destination):
    #     prompt = f"Provide the airport code for the location {destination}, output must be the eaxctly a single word that is the airport code"
        
    #     llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)
    #     messages = [
    #         ("system", 'The system message is usually a guiding prompt that sets the context for the model, outlining the task and what it should focus on. This helps in obtaining a more structured and relevant response from the model.'),
    #         ("human", prompt),
    #     ]

    #     output = llm.invoke(messages).content.strip()
    #     return output
    # end_location_airport_code = extract_travel_information(destination)

    
    # ## Searching for Flights
    # flight_url = "https://sky-scanner3.p.rapidapi.com/flights/search-roundtrip"
    # flight_querystring = {"fromEntityId":'DEL', "toEntityId":end_location_airport_code, "departDate":start_date, "returnDate":end_date, "currency":"USD"}
    # flight_headers = {
    #     "X-RapidAPI-Key": x_rapid_api_Key,
    #     "X-RapidAPI-Host": "sky-scanner3.p.rapidapi.com"
    # }
    # flight_response = requests.get(flight_url, headers=flight_headers, params=flight_querystring)
    # with open('flight.json', 'w') as file:
    #     json.dump(flight_response.json(), file, indent=4)
    # simplified_flight_response = process_flight_data(flight_response.json())


    # ## Finding location entity id
    # entity_id, date, time, drop_time = find_entity_id(flight_response.json(), end_location_airport_code)


    # ## Searching for Hotels
    # hotel_url = "https://sky-scanner3.p.rapidapi.com/hotels/search"
    # hotel_querystring = {"entityId":entity_id,"checkin":date,"checkout":end_date}
    # hotel_headers = {
    #     "X-RapidAPI-Key": x_rapid_api_Key,
    #     "X-RapidAPI-Host": "sky-scanner3.p.rapidapi.com"
    # }
    # hotel_response = requests.get(hotel_url, headers=hotel_headers, params=hotel_querystring)
    # with open('hotel.json', 'w') as file:
    #     json.dump(hotel_response.json(), file, indent=4)
    # simplified_hotel_response = process_hotel_data(hotel_response.json())


    # ## Searching for Taxi
    # taxi_url = "https://sky-scanner3.p.rapidapi.com/cars/search"
    # taxi_querystring = {"pickUpEntityId":entity_id,  "pickUpDate":date, "pickUpTime":time, "dropOffDate":date, "dropOffTime":drop_time}
    # taxi_headers = {
    #     "x-rapidapi-key": x_rapid_api_Key,
    #     "x-rapidapi-host": "sky-scanner3.p.rapidapi.com"
    # }
    # taxi_response = requests.get(taxi_url, headers=taxi_headers, params=taxi_querystring)
    # with open('taxi.json', 'w') as file:
    #     json.dump(taxi_response.json(), file, indent=4)
    # simplified_taxi_response = process_taxi_data(taxi_response.json())

    # return {"flight_details":simplified_flight_response, "hotel_details":simplified_hotel_response, "taxi_details":simplified_taxi_response}
    
    ##Remove the lower part when api is available and un comment the above part
    with open('logistics/constant.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return data
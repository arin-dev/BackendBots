import json
from datetime import datetime

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
        for itinerary in data["data"]["itineraries"][:5]:  # Limit to top 5 results
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
    top_5_hotel_cards = input_json_data["data"]["results"]["hotelCards"][:5]
    for hotel in top_5_hotel_cards:
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
    top_providers = sorted(valid_providers, key=combined_metric, reverse=True)[:5]
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
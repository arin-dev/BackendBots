from datetime import datetime

def process_flight_data(input_data):

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
    simplified_json = reformat_json(input_data)

    return simplified_json
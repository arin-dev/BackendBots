import json

def extract_hotel_data(input_json_data):
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
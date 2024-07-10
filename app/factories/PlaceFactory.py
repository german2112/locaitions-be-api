from app.models.Place import PlaceSchema

class PlaceFactory:
    def create_place(place):
        return PlaceSchema(
            id=str(place["_id"]),
            name=place["name"],
            category=place["category"],
            location=place["location"],
            avgRating=place["avgRating"],
            ownerId=place["ownerId"],
            description=place["description"],
            photos=place["photos"]
        )
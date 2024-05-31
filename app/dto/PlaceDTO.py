class PlaceDTO:
    def __init__(self, place_id, name, location, distance, place_photos, description):
        self.id = place_id
        self.name = name
        self.location = location
        self.distance = distance
        self.place_photos = place_photos
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'distance': self.distance,
            'place_photos': self.place_photos,
            'description': self.description
        }
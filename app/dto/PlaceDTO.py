class PlaceDTO:
    global id
    global name
    global location
    global address
    global distance
    global placePhotos
    global description


    def __init__(self, id, name, location, distance, placePhotos, description):
        self.id = id
        self.name = name
        self.location = location
        self.distance = distance
        self.placePhotos = placePhotos
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'distance': self.distance,
            'place_photos': self.placePhotos,
            'description': self.description
        }
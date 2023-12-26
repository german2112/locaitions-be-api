class PlaceDTO:
    global id
    global name
    global location
    global address
    global distance
    global placePhotos
    global description


    def __init__(self, id, name, location, address, distance, placePhotos, description):
        self.id = id,
        self.name = name
        self.location = location
        self.address = address
        self.distance = distance
        self.placePhotos = placePhotos
        self.description = description

    def to_dict(self):
        return self.__dict__
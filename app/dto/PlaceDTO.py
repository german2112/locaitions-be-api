class PlaceDTO:
    global id
    global name
    global location
    global address
    global distance
    global placePhotos


    def __init__(self, id, name, location, address, distance, placePhotos):
        self.id = id,
        self.name = name
        self.location = location
        self.address = address
        self.distance = distance
        self.placePhotos = placePhotos

    def to_dict(self):
        return self.__dict__
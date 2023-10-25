class Photo:
    
    def __init__(self, filename, fileUrl, createdAt):
        self.filename = filename
        self.fileUrl = fileUrl
        self.createdAt = createdAt

    def to_dict(self):
        return self.__dict__
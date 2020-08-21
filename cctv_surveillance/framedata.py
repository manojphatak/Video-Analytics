import numpy

class FrameData:
    def __init__(self):
        self.id : bytes
        self.someint: int
        self.somestring: str
        self.imagedata: bytes
        self.encod: numpy.ndarray 
        self.matches = []


def translate_old_to_new(olddata):
    newdata = FrameData()        
    newdata.id = olddata["id"]
    newdata.someint = olddata["someint"]
    newdata.somestring = olddata["somestring"]
    newdata.imagedata = olddata["imagedata"]
    newdata.encod = olddata["encod"]
    if "matches" in olddata:
        newdata.matches = olddata["matches"]
    else:
        newdata.matches = []
    return newdata


def translate_new_to_old(newdata):
    return {
        "id": newdata.id,    # hash of the encoding matrix: to serve as primary key
        "someint": newdata.someint,
        "somestring": newdata.somestring,
        "imagedata": newdata.imagedata,
        "encod": newdata.encod,
        "matches": newdata.matches,
    }
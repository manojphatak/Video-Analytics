import numpy
from typing import List

# Each frameData describes a "face"
class FrameData:
    def __init__(self, id, imagedata, encod, matches=[]):
        self.id : bytes = id   # this is hash of encoding
        self.imagedata: bytes = imagedata  # image bytes
        self.encod: numpy.ndarray = encod
        self.matches: List[str]  = matches  # people whom it matches to


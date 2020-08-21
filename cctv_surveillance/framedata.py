import numpy
from typing import List

class FrameData:
    def __init__(self, id, someint, somestring, imagedata, encod, matches=[]):
        self.id : bytes = id
        self.someint: int = someint
        self.somestring: str = somestring
        self.imagedata: bytes = imagedata
        self.encod: numpy.ndarray = encod
        self.matches: List[str]  = matches


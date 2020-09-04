import numpy
from typing import List
import datetime

# Each frameData describes a "face"
class FrameData:
    def __init__(self, id=None, imagedata=None, encod=None, matches=[]):
        self.raw_frame: bytes = b""
        self.t_created : datetime.datetime = datetime.datetime.now() 
        
        self.id : bytes = id   # this is hash of encoding
        self.imagedata: bytes = imagedata  # image bytes
        self.encod: numpy.ndarray = encod
        self.matches: List[str]  = matches  # people whom it matches to


# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

import json

class MessageModel():
    """Class for returning a generic message
    """
    # ID of the inserted object
    id=None
    # Generic user message
    message=""

    def __init__(self: object, message: str=None, id: int=None):
        self.id = id
        self.message = message

class MessageEncoder(json.JSONEncoder):
    """Class for converting full object to JSON string
    """
    def default(self, o): 
        if isinstance(o, MessageModel):
            return {
                "id": o.id,
                "message": o.message
                } 
        else:
            # Base class will raise the TypeError.
            return super().default(o)
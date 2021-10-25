# Name: PdfExporter
# Authors: Jonathan CASSAING
# Tool for parsing and extracting PDF file content

import json

class MessageModel():
    """Class for returning a generic message
    """
    message=""

    def __init__(self: object, message: str=None):
        self.message = message

class MessageEncoder(json.JSONEncoder):
    def default(self, o): 
        if isinstance(o, MessageModel):
            return {
                "message": o.message
                } 
        else:
            # Base class will raise the TypeError.
            return super().default(o)
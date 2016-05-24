import Field

class Editable:
    def __init__(self, fields):
        self.fields = fields

    def GetFields(self):
        return self.fields

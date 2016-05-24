from ..gui import Editable
from ..gui import Field as Field
from ..gui import FieldType as FieldType

class Requirement(Editable.Editable):
    def __init__(self, id):
        self.name_field = Field.Field(FieldType.String, "name")
        self.parent_field = Field.Field(FieldType.Integer, "parent")
        self.fields = array(self.name_field, self.parent_field)
        Editable.__init__(self.fields)
        self.id = id
        self.parent = null
        self.name = null

    next_requirement = 0

    @staticmethod
    def NextRequirementId():
        return ++Requirement.next_requirement

    def GetParent(self):
        return self.parent

    def SetParent(self, parent):
        self.parent = parent

    def GetName(self, name):
        return self.name

    def SetName(self, name):
        self.name = name

from ..gui import editable
from ..gui import field
from ..gui import fieldtype

class Requirement(editable.Editable):
    def __init__(self):
        self.name_field = field.Field(fieldtype.FieldType.String, "name")
        self.parent_field = field.Field(fieldtype.FieldType.Integer, "parent")
        self.fields = [self.name_field, self.parent_field]
        editable.Editable.__init__(self, self.fields)
        self.id = id
        self.parent = 0
        self.name = "(new requirement)"

    next_requirement = 0

    @staticmethod
    def NextRequirementId():
        return ++Requirement.next_requirement

    def GetId(self):
        return self.id

    def SetId(self, id):
        self.id = id

    def GetParent(self):
        return self.parent

    def SetParent(self, parent):
        self.parent = parent

    def GetName(self):
        return self.name

    def SetName(self, name):
        print name
        self.name = name

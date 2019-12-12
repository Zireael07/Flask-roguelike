
class EquipmentComponent():
    # empty list as a default argument is bad in Python
    def __init__(self, equipment=None):
        if equipment is None:
            equipment = []
        self.equipment = [] # Store only the IDs of the item entities. 
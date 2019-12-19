' Tags an item as equipped. '

class EquippedComponent():
    def __init__(self, slot="BODY", owner=None):
        self.slot = slot
        self.owner = owner

# Python 3 enum
from enum import Enum, auto

class RenderOrder(Enum):
    ITEM = auto()
    ACTOR = auto()

class RenderableComponent():

    def __init__(self, char='h', color=(255, 255, 255), render_order=RenderOrder.ACTOR):
        self.char = char
        self.color = color
        self.render_order = render_order

    # readable representation
    def __str__(self):
        return 'Char(char='+str(self.char)+', color='+str(self.color)+ ')'
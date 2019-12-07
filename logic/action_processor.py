from . import esper

from .velocity import Velocity

class ActionProcessor(esper.Processor):

    def __init__(self):
        super().__init__()
        self.action = None

    def process(self):

        # Assign the appropriate component.
        # For example, for action == {'move': (0, -1)}, set the vel.dx and vel.dy.

        _move = self.action.get('move')

        for ent, (vel) in self.world.get_components(Velocity):

            if _move:
                dx, dy = _move
                # Flatten
                vel[0].dx = dx
                vel[0].dy = dy


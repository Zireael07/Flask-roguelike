from . import esper

from .AI_processor import AIProcessor

from .velocity import Velocity
from .turn_component import TurnComponent

from .want_to_pickup import WantToPickupComponent

class ActionProcessor(esper.Processor):

    def __init__(self):
        super().__init__()
        self.action = None

    def process(self):
        # Assign the appropriate component.
        # For example, for action == {'move': (0, -1)}, set the vel.dx and vel.dy.

        _move = self.action.get('move')
        _pick_up = self.action.get('pick_up')

        for ent, (turn) in self.world.get_components(TurnComponent):
            #print("Entity has turn...")
            if _move:
                dx, dy = _move
                #print("We have a move to execute " + str(dx) + " " + str(dy))
                self.world.add_component(ent, Velocity(dx=dx, dy=dy))

            if _pick_up:
                print("Pick up to execute...")
                self.world.add_component(ent, WantToPickupComponent())

            # no longer our turn, AI now acts
            self.world.remove_component(ent, TurnComponent)
            #self.world.add_processor(AIProcessor(), 48) # between movement and combat


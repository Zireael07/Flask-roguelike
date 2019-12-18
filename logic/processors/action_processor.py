from .. import esper

from .AI_processor import AIProcessor

from ..components.velocity import Velocity
from ..components.position import Position
from ..components.turn_component import TurnComponent

from ..components.meditem_component import MedItemComponent
from ..components.ranged_component import RangedComponent
from ..components.wearable import WearableComponent
from ..components.cursor_component import CursorComponent

from ..components.want_to_pickup import WantToPickupComponent
from ..components.want_to_use_med import WantToUseMed
from ..components.want_to_use_item import WantToUseItem
from ..components.want_to_drop import WantToDrop

class ActionProcessor(esper.Processor):

    def __init__(self):
        super().__init__()
        self.action = None

    def process(self):
        # Assign the appropriate component.
        # For example, for action == {'move': (0, -1)}, set the vel.dx and vel.dy.

        _move = self.action.get('move')
        _pick_up = self.action.get('pick_up')
        _use_item = self.action.get('use_item')
        _drop_item = self.action.get('drop_item')
        _target = self.action.get('target')

        for ent, (turn) in self.world.get_components(TurnComponent):
            #print("Entity has turn...")
            if _move:
                dx, dy = _move
                if not self.world.has_component(ent, CursorComponent):
                    #print("We have a move to execute " + str(dx) + " " + str(dy))
                    self.world.add_component(ent, Velocity(dx=dx, dy=dy))
                else:
                    cur = self.world.component_for_entity(ent, CursorComponent)
                    cur.x = cur.x + dx
                    cur.y = cur.y + dy

            if _pick_up:
                print("Pick up to execute...")
                self.world.add_component(ent, WantToPickupComponent())

            if _use_item:
                print("Use item to execute... " + str(_use_item))
                if self.world.has_component(_use_item, MedItemComponent):
                    self.world.add_component(ent, WantToUseMed(_use_item))
                if self.world.has_component(_use_item, RangedComponent):
                    #self.world.add_component(ent, WantToUseItem(_use_item))
                    pos = self.world.component_for_entity(ent, Position)
                    self.world.add_component(ent, CursorComponent(pos.x, pos.y, _use_item))
                if self.world.has_component(_use_item, WearableComponent):
                    self.world.add_component(ent, WantToUseItem(_use_item))

            if _drop_item:
                print("Drop item to execute...")
                self.world.add_component(ent, WantToDrop(_drop_item))

            if _target:
                print("Target to execute....")
                cur = self.world.component_for_entity(ent, CursorComponent)
                self.world.add_component(ent, WantToUseItem(cur.item))
                # remove cursor
                #self.world.remove_component(ent, CursorComponent)

            # if not targeting:
            if not self.world.has_component(ent, CursorComponent):
                # no longer our turn, AI now acts
                self.world.remove_component(ent, TurnComponent)
                #self.world.add_processor(AIProcessor(), 48) # between movement and combat


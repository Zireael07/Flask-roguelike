This project started by following the well-known Python 3 libtcod tutorial's logic.

However, we are not using libtcod and Python classes, we are using Flask and esper (an ECS library)

## What is ECS?

ECS stands for Entity-Component-System. It's slightly similar to what the libtcod tutorial does, meaning it uses composition and not inheritance. However, their approach could be termed EC, but there was no S. Entities and components contained functions that operated on them.

In an ECS, all the logic is constrained to the Systems. Entities are just buckets of components. Components are purely data (e.g. a renderable component stores the character and color, and a name component stores a string).

Note that it is NOT a requirement that the entire project follow the ECS pattern.

## Part 0

Getting flask is as easy as 'pip install flask'. Flask is also contained in Anaconda/miniconda. If you're stuck, follow https://flask.palletsprojects.com/en/1.1.x/installation/

Because we're using esper https://github.com/benmoran56/esper you need Python 3 - the library has no version for 2.7. Esper isn't on pip, so we just included it directly. 

## Part 1

To be able to draw stuff, we need a Position and a Renderable component. We use a simple Flask template to output to screen by drawing a website.
I added a keypad with directional buttons so that you can control the @. The keypad.js has the bit of JavaScript required for the keys to be interactive - all it does is fire off an AJAX request that calls a Flask route. The route then uses a template (again) to create and draw our webpage.

## Part 2

Since we are using ECS, we don't need an Entity object at all! This part introduces the map, which lives separately from the ECS pattern. In classic roguelike fashion, it's a simple 2D array. (The way I look up tiles is fairly complex, and has been implemented mostly out of a desire to make saving/debugging easier by storing only integers, not a whole tile structure, so I will not cover it here)

## Part 3

We are generating an extremely simple map - a big arena which is bordered by walls.

The improved "console" drawing code is inspired by yendor-ts https://github.com/jice-nospam/yendor.ts

## Part 4

The field of vision algorithm comes from Roguebasin. It's precise permissive.
To tint explored tiles gray, we use CSS classes. That's all it takes since we're just manipulating the website's DOM when we redraw.

## Part 5

The only two things we need for NPCs is an NPC component and a blocking component. Why two? Because a blocker need not necessarily be an NPC.
To track whose turn it is, the player receives a TurnComponent which is taken away once the move's made, whereupon the AI stubs run.

## Part 6

The precise permissive FOV allows us to take a shortcut - if we can see an enemy, it HAS to see us too! Also it prevents player frustration (being sniped by unseen enemy) and exploits (sniping enemies who can't see us)

The Astar pathfinding code is from Roguebasin. It worked with only a one-liner change to accept the way we look up tiles. To avoid NPCs piling on each other, the pathfinding treats all other NPCs as wall tiles. It's simple and it works - the only downside is that it requires a deepcopy of the map (a copy won't cut it because the map is a 2D array, not a flat list)

To store things such as HP, we added a CombatStats component. For nice pretty messages, we also need a Name component, otherwise our NPCs would all be nameless and easy to confuse! Actual combat consists of adding a Combat component which stores the id of the entity we're attacking. Just the id, nothing more, and it's enough for fighting to work.

## Part 7

We operate some more DOM. To place two divs side by side, I used a table. I know it's passe, but it's what we use at work (be prepared for this rationale to come up several more times ;) )

## Part 8

It introduces a new action - picking up items. This necessitates a couple things: a) a new button b) a new Flask route c) it has to go through the action processor

To know what we can pick up, we have an Item component. To know that they're in our inventory, we have an InBackpack component. To express the fact that we want to pick up, we have a WantToPickup component, which is fairly similar to the Combat component from part 6 in that it just stores the id.

Inventory menu is just a Flask template that draws a line of text for every item in list - the list is created by simply grabbing all entities that have a InBackpack component. Same goes for the drop menu.

The other thing the chapter introduces is usable items. A new component tells the game that the item is used to heal, and a new WantToUseMedItem component tracks the player's intent.

(The idea behind WantToXXXX components is not mine, I borrowed them from thebracket's Rust tutorial)

## Part 9

This part brings targeting and ranged items. Ranged items themselves are very easy - just need a RangedComponent. Same goes for AoE items. Targeting, however, is more difficult.

The way I implemented it is by adding a CursorComponent to the player - I borrowed the idea from Shoes01's project https://github.com/Shoes01/ECS-Game/commit/f11532e8a62fef8b2317462738a927ab053c5cb7. To control it, I reused the normal move action, just without ending player turn. The background color change is done using CSS.

The only new action necessary was the target_confirm action, triggered by a new button on the keypad. This one actually triggers damage to the targeted NPC.

## Part 10

I usually used jsonpickle here, but it turned out it can't deal with _entities and _component storage in Esper's world (probably due to the use of set/dict). Instead, I used pickle - it's secure enough for my day job, after all! The downside is, pickle is not human-readable.

## Part 11

Skipped, as I plan on having a single continuous map.

## Part 12

The tutorial uses random.choices() to select from a weighted list. Instead, I reused the code I already had, which uses bisect() to select from a list instead. Unfortunately I don't have a link to the source which originally suggested using bisect() way back when I originally wrote the Python version of Veins!

Using components means I can list the common parts together and only list the parts that change between different NPCs/items. Also it means that the spawning/generating code does not need to care about the x,y coords at all, apart from the Position component itself.

## Part 13

I placed the wearing code in the same processor that controlled using items. Yes, the file gets a bit long and convoluted, but that way I do not have to create a new action and a new processor. The items that can be worn get a Wearable component and once they're worn, they get an Equipped component that stores the slot they're in (so you can't wield two pieces of e.g. body armor). 
The item may also have a MeleeBonus component, whose value is added to damage if the item in question is equipped. No need to rely on @property descriptor.

* The original code here had a bug, I forgot to store the owner/wearer which was necessary for item bonuses to be applied to the correct entity ONLY. Oops! It's now fixed but you'll have to look for the fix in one of the more recent commits.




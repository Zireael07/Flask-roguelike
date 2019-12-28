from .. import constants
from ..tile_lookups import TileTypes, get_index
from ..map_common import apply_paint, print_map_string

from .. import noise_ext

# kwargs are there for chaining to work (see game.py 75 and 125)
def map_create(level, **kwargs):
    new_map = [[ get_index(TileTypes.TREE) for _ in range(0, constants.MAP_HEIGHT)] for _ in range(0, constants.MAP_WIDTH)]

    # perlin visualization
    ##noise = [[ 0 for _ in range(0, constants.MAP_HEIGHT)] for _ in range(0, constants.MAP_WIDTH)]

	# make actual map
    for x in range (constants.MAP_WIDTH):
        for y in range (constants.MAP_HEIGHT):

            # this would scale the map the bigger it was, instead of continuing
            # black magic here!
            #i = x/constants.MAP_WIDTH
            #j = y/constants.MAP_HEIGHT

            # https://rtouti.github.io/graphics/perlin-noise-algorithm
            # the inputs cannot be integers since that messes up the algorithm
            i = x*0.01
            j = y*0.01

            # noise
            #n = noise.noise_2d(i,j)
            n = noise_ext.octave_perlin(i,j, 4, 2)
            #noise[x][y] = n

            # map
            if n < 0.65:
                apply_paint(new_map, x, y, 2, get_index(TileTypes.FLOOR))
                #new_map[x][y] = get_index(TileTypes.FLOOR)
            #else:
            #    apply_paint(new_map, x, y, 2, get_index(TileTypes.TREE))
            #    new_map[x][y] = get_index(TileTypes.TREE)

    level.mapa = new_map

    #print_map_string(level.mapa)


    return level # for chaining
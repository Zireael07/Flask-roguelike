from . import constants
from .tile_lookups import TileTypes, get_index

from . import noise_ext

def map_create():
    new_map = [[ get_index(TileTypes.WALL) for _ in range(0, constants.MAP_HEIGHT)] for _ in range(0, constants.MAP_WIDTH)]

	# make actual map
    for x in range (constants.MAP_WIDTH):
        for y in range (constants.MAP_HEIGHT):

            # black magic here!
            i = x/constants.MAP_WIDTH
            j = y/constants.MAP_HEIGHT

            # noise
            #n = noise.noise_2d(i,j)
            n = noise_ext.octave_perlin(i,j, 2, 3)

            # map
            if n < 0.45:
                new_map[x][y] = get_index(TileTypes.FLOOR)
            else:
                new_map[x][y] = get_index(TileTypes.WALL)

    return new_map
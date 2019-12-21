from . import constants
from .tile_lookups import TileTypes, get_index

from . import noise_ext

def map_create():
    new_map = [[ get_index(TileTypes.WALL) for _ in range(0, constants.MAP_HEIGHT)] for _ in range(0, constants.MAP_WIDTH)]

    # perlin visualization
    noise = [[ 0 for _ in range(0, constants.MAP_HEIGHT)] for _ in range(0, constants.MAP_WIDTH)]

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
            noise[x][y] = n

            # map
            if n < 0.45:
                new_map[x][y] = get_index(TileTypes.FLOOR)
            else:
                new_map[x][y] = get_index(TileTypes.WALL)

    return new_map
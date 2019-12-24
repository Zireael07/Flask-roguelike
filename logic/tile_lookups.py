from .enum_constants import Tile_Lookups

class struc_Tile(object):
    def __init__(self, name, map_str, block_path):
        self.block_path = block_path
        self.name = name
        self.map_str = map_str


# outside of both classes
def tile_from_index(i):
    return TileTypes.test[i]

def get_index(val):
    return val[0]

def get_map_str_type(val):
    return val[1].map_str

def get_map_str(i):
    return tile_from_index(i).map_str

def get_block_path(i):
    return TileTypes.test[i].block_path



TileTypes = Tile_Lookups(WALL=(1,struc_Tile("wall", "#", True)),
                        # if they ever are needed outside of drawing glyphs...
                        #  WALL_V = (2, struc_Tile("wall", "║", True)),
                        #  WALL_H = (3, struc_Tile("wall", "═", True)),
                        #  WALL_SE_C = (4, struc_Tile("wall", "╝", True)),
                        #  WALL_NE_C = (5, struc_Tile("wall", "╗", True)),
                        #  WALL_SW_C = (6, struc_Tile("wall", "╚", True)),
                        #  WALL_NW_C = (7, struc_Tile("wall", "╔", True)),
                        #  WALL_TE = (8, struc_Tile("wall", "╣", True)),
                        #  WALL_TW = (9, struc_Tile("wall", "╠", True)),
                        #  WALL_TS = (10, struc_Tile("wall", "╩", True)),
                        #  WALL_TN = (11, struc_Tile("wall", "╦", True)),
                        #  WALL_PILLAR = (12, struc_Tile("wall", "○", True)),
                         FLOOR=(2, struc_Tile("floor", ".", False)),
                         DEBUG=(3, struc_Tile("debug", ">", False)),
                      )



if __name__ == "__main__":


    # way to look up by string
    print(TileTypes.dict["FLOOR"])

    # doesn't work
    #print(TileTypes["FLOOR"])

    print("Wall is " + str(TileTypes.WALL))

    print("Wall index is " + str(get_index(TileTypes.WALL)))

    print("Map str is " + str(get_map_str_type(TileTypes.WALL)))

    print("Tile from index: " + str(tile_from_index(1)) + ", " + str(tile_from_index(1).name))

    print("Map str from index is: " + str(get_map_str(1)))
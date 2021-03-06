from ..map_common import print_map_string, Directions, Rect
from ..tile_lookups import TileTypes, get_index

# for histogram
from collections import namedtuple
Info = namedtuple('Info', 'start height')

# sorting
from operator import itemgetter

# step one of finding rectangle of floor in matrix
# https://stackoverflow.com/a/12387148
def num_unbroken_floors_columns(inc_map):
    num_floors = [[0 for _ in range(len(inc_map[0]))] for _ in range(len(inc_map))]

    for x in range(0, len(inc_map)): # width
        for y in range(0, len(inc_map[0])): #height
            north = (x + Directions.NORTH[0], y + Directions.NORTH[1])
            num_floors[x][y] = 1 + num_floors[north[0]][north[1]] if inc_map[x][y] == get_index(TileTypes.FLOOR) else 0

    return num_floors

# parse it nicely
def unbroken_floors_columns_get(num_floors):
    floors = []
    for y in range(len(num_floors)):
        row = []
        for x in range(len(num_floors[0])):
            row.append(num_floors[x][y])

        floors.append(row)

    return floors

def unbroken_floors_columns_print(num_floors):
    list_str = []
    for y in range(len(num_floors)):
        for x in range(len(num_floors[0])):
            list_str.append(str(num_floors[x][y]))

        # our row ended, add a line break
        list_str.append("\n")

    string = ''.join(list_str)
    # print string
    return string

# max area rect under histogram
# based on https://stackoverflow.com/a/4690790
def max_rectangle_area( histogram, hist_index):
    """Find the area of the largest rectangle that fits entirely under
    the histogram.
    Return: rect (x,y,w,h), area
    """

    #print("Histogram: " + str(histogram) + " " + str(len(histogram)))

    stack = []
    top = lambda: stack[-1]
    max_area = 0
    # new
    rects = []
    res = None

    pos = 0  # current position in the histogram
    for pos, height in enumerate(histogram):
        #print("Index " + str(pos) + " height " + str(height))
        start = pos  # position where rectangle starts
        while True:
            # if higher than previous, push to stack
            if not stack or height > top().height:
                #print("Append to stack")
                stack.append(Info(start, height))  # push
            # if lower, pop from stack
            elif stack and height < top().height:
                width = pos - top().start
                area = height * width
                if area > max_area:
                    max_area = area
                    # we assigned 1 for the first free cell in a column, but a Rect with a height of 1 is x+1 not x
                    # so we need to deduce 1 (so we get x and not x+1)
                    # this algo is bottom-up, rect is top-down - deduce height from y and add 1 so that we cover the bottom line
                    res = Rect(pos-width, hist_index-height-1, width, height+1), hist_index

                start, _ = stack.pop()
                continue
            break  # height == top().height goes here

    return max_area, res

# step two of finding rectangle of floor in matrix
# https://stackoverflow.com/a/12387148
def largest_area_rects(floors):
    rects = []
    # reverse order
    for y in range(len(floors) - 1, -1, -1):
        #print("Index: " + str(y))
        #print(str(floors[y]))

        rect = max_rectangle_area(floors[y], y)

        # discard all rects whose area is 0 or 1 (TODO: why do they happen?)
        if rect[0] > 1:
                #print("Appending: " + str(rect))
                rects.append(rect)

    # this sorts in ascending order
    sort = sorted(rects, key=itemgetter(0))
    # .. so we need the last entry
    return sort[len(sort) - 1]


def run_rectangle_detection(mapa):
    floors = num_unbroken_floors_columns(mapa)
    # pretty
    #print(unbroken_floors_columns_print(floors))

    # get tidy rows from the floors 2d array
    row_floors = unbroken_floors_columns_get(floors)
    #print(row_floors)

    largest = largest_area_rects(row_floors)

    big_rect = largest[1][0]
    index = largest[1][1]
    w = big_rect.x2 - big_rect.x1
    h = big_rect.y2 - big_rect.y1

    print("Largest: " + "index: " + str(index) + " x " + str(big_rect.x1) + ",y " + str(big_rect.y1) +
            " w: " + str(w) + " h: " + str(h))
    # " to x: " + str(big_rect.x2) + ",y: " + str(big_rect.y2))

    return big_rect


def fill_big_rect(rect, mapa):
    #print("Filling... " + str(rect.x1) + "," + str(rect.y1) + ", w " + str(rect.x2-rect.x1) + " h " + str(rect.y2-rect.y1))
    # Set all tiles in rect to debug
    # range is exclusive at the end!
    for x in range(rect.x1, rect.x2+1):
        for y in range(rect.y1, rect.y2+1):
            # it's just for debugging purposes
            mapa[x][y] = get_index(TileTypes.DEBUG)

# kwargs are there for chaining to work (see game.py 75 and 125)
def apply_rectangle_detection(level, **kwargs):
    rect = run_rectangle_detection(level.mapa)

    # add to submaps list
    level.submaps.append(rect)

    #print_map_string(mapa)

    fill_big_rect(rect, level.mapa)

    # debug
    print_map_string(level.mapa)

    # debug
    for s in level.submaps:
        print(str(s))

    return level # for chaining
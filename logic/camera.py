from . import game_vars

class obj_Camera(object):
    def __init__(self):
        self.width = 20  # 80
        self.height = 20  # 25
        self.x, self.y = (0, 0)
        self.top_x, self.top_y = (0, 0)
        self.offset = (0, 0)

    def start_update(self):
        target_pos = (1, 1)
        self.offset = (target_pos[0] - self.x, target_pos[1] - self.y)

    def update(self, position):

        # this calculates cells
        self.x, self.y = position.x, position.y
        self.top_x, self.top_y = int(self.x - self.width / 2), int(self.y - self.height / 2)

    def debug_update(self):
        self.top_x, self.top_y = self.x - self.width / 2, self.y - self.height / 2

    def debug_move(self, x, y):
        self.x, self.y = x,y
        self.debug_update()

        target_pos = (80, 20)

        self.offset = (target_pos[0] - self.x, target_pos[1] - self.y)
        #print("Offset: " + str(self.offset))


    def move(self, dx, dy):
        # straightforward for cartesian coords
        self.offset = (self.offset[0] + dx, self.offset[1] + dy)

    # camera extents to speed up rendering
    def get_width_start(self):
        if self.top_x > 0:
            return self.top_x
        else:
            return 0

    def get_width_end(self, map_draw):
        if self.top_x + self.width <= len(map_draw):  # constants.MAP_WIDTH:
            return int(self.top_x + self.width)
        else:
            return len(map_draw)  # constants.MAP_WIDTH

    def get_height_start(self):
        if self.top_y > 0:
            return self.top_y
        else:
            return 0

    def get_height_end(self, map_draw):
        if self.top_y + self.height <= len(map_draw[0]):  # constants.MAP_HEIGHT:
            return int(self.top_y + self.height)
        else:
            return len(map_draw[0])  # constants.MAP_HEIGHT
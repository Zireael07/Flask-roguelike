class Velocity():
    def __init__(self, dx=0, dy=0):
        self.dx = dx
        self.dy = dy

    # readable representation
    def __str__(self):
        return 'Vel(dx='+str(self.dx)+', dy='+str(self.dy)+ ')'


class RenderableComponent():

    def __init__(self, char='h', color=(255, 255, 255)):
        self.char = char
        self.color = color

    # readable representation
    def __str__(self):
        return 'Char(char='+str(self.char)+', color='+str(self.color)+ ')'
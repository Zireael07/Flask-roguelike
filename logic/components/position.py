class Position():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
   
    # readable representation
    def __str__(self):
        return 'Pos(x='+str(self.x)+', y='+str(self.y)+ ')'
    

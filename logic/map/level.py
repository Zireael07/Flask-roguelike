
class obj_Level(object):
    def __init__(self, mapa=None, submaps=None):
        self.mapa = mapa
        if submaps is None:
            self.submaps = []
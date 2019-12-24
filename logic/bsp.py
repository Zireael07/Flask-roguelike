# based on https://github.com/AtTheMatinee/dungeon-generation

import random

from .map_common import Rect

# ==== BSP Tree ====
class BSPTree:
	def __init__(self, m_leaf=24):
		self.level = []
		self.room = None
		self.MAX_LEAF_SIZE = m_leaf
		# used by create rooms below
		self.ROOM_MAX_SIZE = m_leaf-2
		self.ROOM_MIN_SIZE = 5

	def generateLevel(self, x,y, mapWidth, mapHeight, roomHook, mapa):
		self._leafs = []
		rootLeaf = Leaf(x,y,mapWidth,mapHeight)
		#print("root: " + str(rootLeaf.x) + " " + str(rootLeaf.y) + ' : ' + str(rootLeaf.width) + " " + str(rootLeaf.height))
		self._leafs.append(rootLeaf)

		splitSuccessfully = True

		# loop through all leaves until they can no longer split successfully
		while (splitSuccessfully):
			splitSuccessfully = False
			for l in self._leafs:
				if (l.child_1 == None) and (l.child_2 == None):
					if ((l.width > self.MAX_LEAF_SIZE) or 
					(l.height > self.MAX_LEAF_SIZE) or
					(random.random() > 0.8)):
						if (l.splitLeaf()): #try to split the leaf
							self._leafs.append(l.child_1)
							self._leafs.append(l.child_2)
							splitSuccessfully = True

		rootLeaf.createRooms(self, roomHook, mapa)

		return rootLeaf, self._leafs

class Leaf:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.MIN_LEAF_SIZE = 8 #10
		self.child_1 = None
		self.child_2 = None
		#print("Leaf: " + str(self.x) + " " + str(self.y) + ' : ' + str(self.width) + " " + str(self.height))

	def splitLeaf(self):
		# begin splitting the leaf into two children
		if (self.child_1 != None) or (self.child_2 != None):
			return False # This leaf has already been split

		'''
		==== Determine the direction of the split ====
		If the width of the leaf is >25% larger than the height,
		split the leaf vertically.
		If the height of the leaf is >25 larger than the width,
		split the leaf horizontally.
		Otherwise, choose the direction at random.
		'''

		splitHorizontally = random.choice([True, False])

		if (self.width/self.height >= 1.25):
			splitHorizontally = False

		elif (self.height/self.width >= 1.25):
			splitHorizontally = True

		if (splitHorizontally):
			max = self.height - self.MIN_LEAF_SIZE
		else:
			max = self.width - self.MIN_LEAF_SIZE

		if (max <= self.MIN_LEAF_SIZE):
			return False # the leaf is too small to split further

		split = random.randint(self.MIN_LEAF_SIZE,max) #determine where to split the leaf

		if (splitHorizontally):
			self.child_1 = Leaf(self.x, self.y, self.width, split)
			self.child_2 = Leaf( self.x, self.y+split, self.width, self.height-split)
		else:
			self.child_1 = Leaf( self.x, self.y,split, self.height)
			self.child_2 = Leaf( self.x + split, self.y, self.width-split, self.height)

		return True

	def createRooms(self, bspTree, createRoom, mapa):
		if (self.child_1) or (self.child_2):
			# recursively search for children until you hit the end of the branch
			if (self.child_1):
				self.child_1.createRooms(bspTree, createRoom, mapa)
			if (self.child_2):
				self.child_2.createRooms(bspTree, createRoom, mapa)

			# if (self.child_1 and self.child_2):
			# 	bspTree.createHall(self.child_1.getRoom(),
			# 		self.child_2.getRoom())

		else:
		# Create rooms in the end branches of the bsp tree
			w = random.randint(bspTree.ROOM_MIN_SIZE, min(bspTree.ROOM_MAX_SIZE,self.width-1))
			h = random.randint(bspTree.ROOM_MIN_SIZE, min(bspTree.ROOM_MAX_SIZE,self.height-1))
			x = random.randint(self.x, self.x+(self.width-1)-w)
			y = random.randint(self.y, self.y+(self.height-1)-h)
			self.room = Rect(x,y,w,h)
			createRoom(self.room, mapa)
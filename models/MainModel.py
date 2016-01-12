#!/usr/bin/env python3

import random
from models.components import *

class MainModel:
	def __init__(self):
		self.breadboard = []
		for _ in range(10):
			toAppend = []
			for _ in range(10):
				toAppend.append((None, None))
			self.breadboard.append(toAppend)

		self.components = []
		self.freePositions = []
		for x in range(10):
			for y in range(10):
				self.freePositions.append((x, y))

	# supply zero or both indices, otherwise fails
	def addComponent(self, component, x=None, y=None):
		if x is None and y is None:
			component.position = self.freePosition()
		elif x is None or y is None or self.breadboard[x][y] is not None:
			return False

		if component.position is not None:
			self.freePositions.remove(component.position)
			self.breadboard[component.position[0]][component.position[1]] = component
			self.components.append(component)
			return True
		
		return False

	def freePosition(self):
		return None if len(self.freePositions) == 0 else random.choice(self.freePositions)
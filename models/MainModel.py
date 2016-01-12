#!/usr/bin/env python3

import random
from models.components import *
import itertools

class MainModel:
	def __init__(self):
		self.counter = 0
		self.breadboard = [[None for _ in range(10)] for _ in range(10)]
		self.components = []
		self.freePositions = list(itertools.product(range(10),range(10)))

	# supply zero or both indices, otherwise fails
	def addComponent(self, component, x=None, y=None):
		if x is None and y is None:
			component.position = self.freePosition()
		elif x is not None and y is not None and self.breadboard[x][y] is not None:
			component.position = (x, y)

		if component.position is not None:
			component.position
			self.breadboard[component.position[0]][component.position[1]] = component
			self.components.append(component)
			component.id = self.counter
			self.counter += 1

			self.freePositions.remove(component.position)
			return True
		
		return False
	# TODO: CONNECTION CODE 

	def freePosition(self):
		return None if len(self.freePositions) == 0 else random.choice(self.freePositions)
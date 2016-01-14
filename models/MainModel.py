#!/usr/bin/env python3

import random
from models.components import *
import itertools
from PyQt5.QtCore import QObject, pyqtSignal

class MainModel(QObject):
	modelChanged = pyqtSignal(name='modelChanged')

	def __init__(self):
		QObject.__init__(self)
		self.gridSize = 10
		self.counter = 0
		self.breadboard = [[None for _ in range(self.gridSize)] for _ in range(self.gridSize)]
		self.components = []
		self.freePositions = list(itertools.product(range(self.gridSize),range(self.gridSize)))

	# supply zero or both indices, otherwise fails
	def addComponent(self, component):
		# check validity of index and vacancy of insertion position
		if self.validIndex(component.position) and self.breadboard[component.position[0]][component.position[1]] is None:
			component.id = self.counter
			self.counter += 1
			self.breadboard[component.position[0]][component.position[1]] = component
			self.components.append(component)
			self.modelChanged.emit()
			return True
		else:
			return False

	def removeComponent(self, component):
		if component in self.components:
			component.removeConnections()
			self.breadboard[component.position[0]][component.position[1]] = None
			self.components.remove(component)
			self.modelChanged.emit()	

	def addConnection(self, component1, component2):
		print(component1.position)
		print(component2.position)
		print(abs(component1.position[0] - component2.position[0]))
		if component1.position[0] == component2.position[0]:
			if abs(component1.position[1] - component2.position[1]) != 1:
				return False
			else:
				if component1.position[1] > component2.position[1]:
					component1.connections[Direction.Top] = component2
					component2.connections[Direction.Bottom] = component1
				else:
					component1.connections[Direction.Bottom] = component2
					component2.connections[Direction.Top] = component1
				self.modelChanged.emit()
				return True
		elif component1.position[1] == component2.position[1]:
			if abs(component1.position[0] - component2.position[0]) != 1:
				return False
			else:
				if component1.position[0] > component2.position[0]:
					component1.connections[Direction.Left] = component2
					component2.connections[Direction.Right] = component1
				else:
					component1.connections[Direction.Right] = component2
					component2.connections[Direction.Left] = component1
				self.modelChanged.emit()
				return True
		return False

	def moveComponent(self, component, newIndex):
		if component in self.components and self.validIndex(newIndex) and self.breadboard[newIndex[0]][newIndex[1]] is None:
			component.removeConnections()
			self.breadboard[component.position[0]][component.position[1]] = None
			component.position = newIndex
			self.breadboard[newIndex[0]][newIndex[1]] = component
			self.modelChanged.emit()
			return True
		else:
			return False

	def validIndex(self, index):
		return index is not None and len(index) == 2 and index[0] >= 0 and index[0] < self.gridSize and index[1] >= 0 and index[1] <= self.gridSize
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
			return True
		else:
			return False

	def removeComponentAtIndex(self, index):
		return self.removeComponent(self.componentAtIndex(index))

	def addConnection(self, component1, component2):
		if component1.position[0] == component2.position[0]:
			# vertical
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
			# horizontal
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

	def componentAtIndex(self, index):
		return self.breadboard[index[0]][index[1]] if self.validIndex(index) else None

	def validIndex(self, index):
		return index is not None and len(index) == 2 and index[0] >= 0 and index[0] < self.gridSize and index[1] >= 0 and index[1] <= self.gridSize
		
	def saveModel(self, fname=None):
		file = open(fname, 'w')
		output = ""
		for row in self.breadboard:
			output += "%"
			for component in row:
				if component is not None:
					output += "@"
					# Type
					output += "x" + str(component.type.value)
					# Voltage
					output += "x" + str(component.voltage)
					# Current
					output += "x" + str(component.current)
					# Position
					output += "x" + str(component.position[0]) + "$" + str(component.position[1])
					# Connections
					output += "x"
					for connection in component.connections:
						if connection is not None:
							output += "$" + str(connection.position[0]) + "$" + str(connection.position[1])
						else:
							output += "$NA$NA"
					# Resistance
					try:
					    output += "x" + str(component.resistance)
					except AttributeError:
					    output += "xNA"
					# Closed
					try:
					    output += "x" + str(component.closed)
					except AttributeError:
					    output += "xNA"
					# Negative Side
					try:
					    output += "x" + str(component.negativeSide.value)
					except AttributeError:
					    output += "xNA"
				else:
					output += "@EM"
		file.write(output)
		# print(output)

	def clearModel(self):
		self.breadboard = [[None for _ in range(self.gridSize)] for _ in range(self.gridSize)]
		self.components = []
		self.freePositions = list(itertools.product(range(self.gridSize),range(self.gridSize)))
		self.modelChanged.emit()

	def readModel(self, fname=None):
		self.clearModel()
		file = open(fname, 'r')
		inputText = file.read()
		try:
			encodedBreadboard = inputText.split("%")
			encodedBreadboard = [s for s in encodedBreadboard if s != ""]
			for x in range(self.gridSize):
				encodedBreadboard[x] = encodedBreadboard[x].split("@")
				encodedBreadboard[x] = [s for s in encodedBreadboard[x] if s != ""]
			for x in range(self.gridSize):
				for y in range(self.gridSize):
					encodedComponent = encodedBreadboard[x][y].split("x")
					encodedComponent = [s for s in encodedComponent if s != ""]
					if encodedBreadboard[x][y] != "EM":
						cType = int(encodedComponent[0])
						if cType == 7:
							newComponent = Wire()
						elif cType == 1:
							newComponent = Battery()
						elif cType == 2:
							newComponent = Switch()
						elif cType == 3:
							newComponent = Button()
						elif cType == 4:
							newComponent = Resistor()
						elif cType == 5:
							newComponent = Ammeter()
						elif cType == 6:
							newComponent = Voltmeter()
						elif cType == 8:
							newComponent = Junction()
						else:
							newComponent = Bulb()
						currentComponent = newComponent
						# currentComponent.type = int(encodedComponent[0])
						currentComponent.voltage = float(encodedComponent[1])
						currentComponent.current = float(encodedComponent[2])
						currentComponent.position = (x, y)
						if encodedComponent[5] != "NA":
							currentComponent.resistance = float(encodedComponent[5])
						if encodedComponent[6] != "NA":
							if encodedComponent[6] == "True":
								currentComponent.closed = True
							else:
								currentComponent.closed = False
						#if encodedComponent[7] != "NA":
						#	currentComponent.negativeSide = int(encodedComponent[7])
						self.addComponent(currentComponent)
			# Config connections
			for x in range(self.gridSize):
				for y in range(self.gridSize):
					currentComponent = self.breadboard[x][y]
					if currentComponent is not None:
						encodedComponent = encodedBreadboard[x][y].split("x")
						encodedComponent = [s for s in encodedComponent if s != ""]
						encodedConnections = encodedComponent[4].split("$")
						encodedConnections = [s for s in encodedConnections if s != ""]
						# print(encodedConnections)
						if encodedConnections[0] != "NA":
							currentComponent.connections[0] = self.breadboard[int(encodedConnections[0])][int(encodedConnections[1])]
						if encodedConnections[2] != "NA":
							currentComponent.connections[1] = self.breadboard[int(encodedConnections[2])][int(encodedConnections[3])]
						if encodedConnections[4] != "NA":
							currentComponent.connections[2] = self.breadboard[int(encodedConnections[4])][int(encodedConnections[5])]
						if encodedConnections[6] != "NA":
							currentComponent.connections[3] = self.breadboard[int(encodedConnections[6])][int(encodedConnections[7])]
						# print(currentComponent)
			self.modelChanged.emit()
			return True
		except Exception as e:
			return False
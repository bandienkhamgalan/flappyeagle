#!/usr/bin/env python3

from models.components import *
from functools import reduce
import math

class Series:
	def __init__(self):
		self.components = []
		self.completed = False
		self.inputVoltage = 0

	@property
	def resistance(self):
		return sum(self.componentResistances.values())

	@property
	def componentResistances(self):
		toReturn = {}
		for component in self.components:
			toReturn[component] = 0
			if hasattr(component, 'resistance'):
				toReturn[component] = component.resistance
		return toReturn

	@property
	def voltage(self):
		return self.inputVoltage + sum([battery.voltage for battery in self.batteries])
	@voltage.setter
	def voltage(self, value):
		self.inputVoltage = value

	@property
	def batteries(self, recursive=False):
		toReturn = []
		for component in self.components:
			if isinstance(component, Battery):
				toReturn.append(component)
		return toReturn		

	@property
	def nonWireComponents(self):
		toReturn = []
		for component in self.components:
			if not isinstance(component, Wire):
				toReturn.append(component)
		return toReturn

	@property
	def valid(self):
		# check completion
		if not self.completed:
			return False
		# check connection of batteries, if multiple batteries are connected
		for battery in self.batteries:
			if battery.negativeTerminal is not battery.directionOfCurrent:
				return False
		return True

	@property
	def closed(self):
		if not self.valid:
			return False
		# check switches and buttons
		for component in self.components:
			if isinstance(component, Switch) or isinstance(component, Button):
				if not component.closed:
					return False
		return True

	def updateComponentProperties(self):
		circuitClosed = self.closed
		componentResistances = self.componentResistances
		totalResistance = sum(componentResistances.values())
		totalVoltage = self.voltage
		print("total resistance ", totalResistance, " and total voltage ", totalVoltage)
		print("component resistances ", componentResistances)
		current = totalVoltage / totalResistance if totalResistance > 0 else math.inf
		for component in self.components:
			component.current = current if circuitClosed else 0
			if isinstance(component, Voltmeter):
				component.voltage = totalVoltage
			elif not isinstance(component, Battery):
				component.voltage = component.current * componentResistances[component]
			print(component, " voltage: ", component.voltage, " current: ", component.current)
			if isinstance(component, Parallel):
				component.updateComponentProperties()

	def addComponent(self, component):
		if isinstance(component, Component) or isinstance(component, Parallel):
			self.components.append(component)
			return True
		else:
			return False

	def __str__(self):
		toReturn = ""
		if len(self.components) > 0:
			toReturn = "Series(%s" % self.components[0]
			for x in range(1, len(self.components)):
				if not isinstance(self.components[x], Wire):
					toReturn += ", \n%s with %f volts and %f amps" % (self.components[x], self.components[x].voltage, self.components[x].current)
					toReturn += (" and %f ohms" % self.components[x].resistance) if hasattr(self.components[x], 'resistance') else ""
			toReturn += ")"
		return toReturn

class Parallel:
	def __init__(self):
		self.branchA = Series()
		self.branchB = Series()
		self.voltage = 0 
		self.current = 0

	@property
	def resistance(self):
		# check voltmeter logic
		branchAComponents = self.branchA.nonWireComponents
		branchAVoltmeterCount = len([component for component in branchAComponents if isinstance(component, Voltmeter)])
		branchBComponents = self.branchB.nonWireComponents
		branchBVoltmeterCount = len([component for component in branchBComponents if isinstance(component, Voltmeter)])
		if branchAVoltmeterCount > 0 and branchBVoltmeterCount > 0:
			return math.inf
		else:
			print("branchA (%d voltmeters): %f ohms and branchB (%d voltmeters): %f ohms" % (branchAVoltmeterCount, self.branchA.resistance, branchBVoltmeterCount, self.branchB.resistance))
			print("final resistance: ", 1 / (1 / self.branchA.resistance + 1 / self.branchB.resistance))
			return 1 / (1 / self.branchA.resistance + 1 / self.branchB.resistance)

	def updateComponentProperties(self):
		self.branchA.voltage = self.voltage
		self.branchB.voltage = self.voltage
		self.branchA.updateComponentProperties()
		self.branchB.updateComponentProperties()

	def __str__(self):
		return "Parallel(%s, %s)" % (self.branchA, self.branchB)

class CircuitLogicController:
	def __init__(self, model=None):
		self.model = model
		self.resetModelRunVariables()

	def printBreadboard(self):
		for component in self.model.components:
			print(component)

	def resetModelRunVariables(self):
		self.batteries = []
		if self.model is not None:
			for component in self.model.components:
				if component.type is ComponentType.Battery:
					self.batteries.append(component)
				else:
					component.voltage = 0.0

				component.current = 0.0
				component.visited = False
				component.directionOfCurrent = None

				self.voltmeters = {}
				self.ignorableJunctions = []

	def runBreadboard(self):
		# reset and find batteries
		self.resetModelRunVariables()
		while len(self.batteries) > 0:
			battery = self.batteries.pop()
			if not battery.visited:
				self.runCircuit(battery)

		self.model.modelChanged.emit()

	def stopBreadboard(self):
		self.resetModelRunVariables()
		self.model.modelChanged.emit()

	def runCircuit(self, battery):
		battery.directionOfCurrent = battery.negativeTerminal
		componentTree = self.buildComponentTree(battery, battery)
		# print("circuit: ", componentTree)
		componentTree.updateComponentProperties()
		print("\n\n\n\n\n")
		print("circuit: ", componentTree)
		# self.printBreadboard()

	def buildComponentTree(self, startingComponent, endingComponent):
		seriesTree = Series()
		currentComponent = startingComponent
		nextComponent = None
		print("in buildComponentTree starting at ", startingComponent)
		while True:
			currentComponent.visited = True
			exitingConnections = currentComponent.exitingConnections(currentComponent.directionOfCurrent)
			seriesTree.addComponent(currentComponent)
			print("at %s\n\t\t\tWITH %d neigbhors" % (currentComponent, len(exitingConnections)))
			
			if len(exitingConnections) == 0:
				print("found component with 0 connections, ending invalid")
				break
			elif len(exitingConnections) == 1:
				nextComponent = exitingConnections[0]
				nextComponent.directionOfCurrent = Direction(currentComponent.connections.index(nextComponent))
			elif len(exitingConnections) == 2 and currentComponent.type is ComponentType.Wire:
				# find shortest path
				exitingConnections[0].directionOfCurrent = Direction(currentComponent.connections.index(exitingConnections[0]))
				exitingConnections[1].directionOfCurrent = Direction(currentComponent.connections.index(exitingConnections[1]))
				branchA = self.shortestPath(exitingConnections[0], endingComponent)
				branchB = self.shortestPath(exitingConnections[1], endingComponent)
				print("branch A not cleanedd: ", branchA)
				print("branch B not cleanedd: ", branchB)
				if branchA is not None and branchB is not None and len(branchA) > 1 and len(branchB) > 1:
					while branchA[-2] is branchB[-2] and len(branchA) > 1 and len(branchB) > 1:
						branchA.pop()
						branchB.pop()
					branchALast = branchA.pop()
					branchBLast = branchB.pop()

					if branchALast.type is ComponentType.Wire and branchALast.numberOfConnections() == 3:
						print("got last junction ", branchALast)
						endingJunction = branchALast
						endingJunction.directionOfCurrent = [Direction(branchA[-1].connections.index(endingJunction)), Direction(branchB[-1].connections.index(endingJunction))]
						directionAfterJunction = [direction for direction in Direction if endingJunction.connections[direction] is not None and endingJunction.connections[direction] not in endingJunction.directionOfCurrent][0]

						parallelComponent = Parallel()
						print("branch A: ", branchA)
						print("branch B: ", branchB)
						parallelComponent.branchA = self.buildComponentTree(branchA[0], branchA[-1])
						parallelComponent.branchB = self.buildComponentTree(branchB[0], branchB[-1])
						print("Finished rescursion of ", currentComponent)
						seriesTree.addComponent(parallelComponent)
						seriesTree.addComponent(endingJunction)

						currentComponent = endingJunction
						nextComponent = endingJunction.connections[directionAfterJunction]
						nextComponent.directionOfCurrent = directionAfterJunction

						print("Jumping to ", nextComponent)
					else:
						print("found parallel with no common junction, ending invalid")
						# invalid shortest path found -> invalid circuit
						break
				else:
					print("couldn't find shortest path, ending invalid")
					# couldn't find shortest path -> invalid circuit
					break

			if currentComponent is endingComponent:
				if currentComponent.type is ComponentType.Battery and len(seriesTree.components) > 1:
					seriesTree.components.pop()
					seriesTree.completed = True
					break
				elif currentComponent.type is not ComponentType.Battery:
					seriesTree.completed = True
					break

			currentComponent = nextComponent
		return seriesTree

	def shortestPath(self, start, end):
		distances = {}
		previous = {}
		vertices = []
		for component in self.model.components:
			distances[component] = math.inf
			vertices.append(component)

		distances[start] = 0
		while len(vertices) > 0 or currentComponent == end:
			# get nearest node in list of vertices and remove it
			currentComponent = reduce(lambda x, y: x if x[1] < y[1] else y, [(component, distances[component]) for component in vertices])[0]
			vertices.remove(currentComponent)

			if currentComponent == end:
				break

			for direction in Direction:
				if currentComponent.connections[direction] is not None:
					if currentComponent.directionOfCurrent is not None and direction is currentComponent.directionOfCurrent.opposite():
						continue
					else:
						neighbor = currentComponent.connections[direction]
						alt = distances[currentComponent] + 1
						if alt < distances[neighbor]:
							distances[neighbor] = alt
							previous[neighbor] = currentComponent
		
		# follow references and build a path
		backwardsPath = []
		currentComponent = end
		while currentComponent is not None:
			backwardsPath.append(currentComponent)
			if currentComponent in previous:
				currentComponent.directionOfCurrent = Direction(previous[currentComponent].connections.index(currentComponent))
			currentComponent = previous.get(currentComponent, None)

		if len(backwardsPath) > 1:
			return list(reversed(backwardsPath))
		else:
			None
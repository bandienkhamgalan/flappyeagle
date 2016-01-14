#!/usr/bin/env python3

from models.components import *

class CircuitLogicController():
	def __init__(self, model):
		self.model = model

	def printBreadboard(self):
		for component in self.model.components:
			print(component)

	def runBreadboard(self):
		# reset and find batteries
		batteries = []
		for component in self.model.components:
			if component.type is ComponentType.Battery:
				batteries.append(component)
			else:
				component.voltage = 0.0
				component.current = 0.0
			component.visited = False
			component.direction = None

		while len(batteries) > 0: 
			battery = batteries.pop()
			battery.visited = True

			print(self.runCircuit(battery, battery.negativeSide.opposite()))


	def runCircuit(self, startingComponent, enteringDirection):
		visitedComponents = []
		currentComponent = startingComponent
		currentEnteringDirection = enteringDirection
		totalVoltage = 0
		totalResistance = 0
		switchClosed = True
		while True:
			exitingConnections = currentComponent.exitingConnections(currentEnteringDirection)

			if currentComponent is startingComponent and len(visitedComponents) > 0:
				# completed circuit	
				break			
			
			if len(exitingConnections) == 1 and currentComponent.type is not ComponentType.Junction:
				resistance = 0
				try:
					resistance = currentComponent.resistance
				except AttributeError:
					pass
				totalResistance += resistance

				if currentComponent.type is ComponentType.Battery:
					totalVoltage += currentComponent.voltage
					if currentComponent.negativeSide is currentEnteringDirection:
						# invalid circuit
						return False	

				if currentComponent.type is ComponentType.Button or currentComponent.type is ComponentType.Switch and not currentComponent.closed:
					switchClosed = False

				visitedComponents.append(currentComponent)
				currentComponent.visited = True
				currentComponent.direction = currentEnteringDirection

				currentEnteringDirection = Direction(currentComponent.connections.index(exitingConnections[0])).opposite()
				currentComponent = exitingConnections[0]
			# junction 
			# HANDLE THIS
			elif len(exitingConnections) == 2 and currentComponent.type is ComponentType.Junction:
				pass
			else:
				# invalid circuit
				return False

		if switchClosed:
			seriesCurrent = totalVoltage / totalResistance
			for currentComponent in visitedComponents:
				currentComponent.current = seriesCurrent

				if currentComponent.type is not ComponentType.Battery:
					resistance = 0
					try:
						resistance = currentComponent.resistance
					except AttributeError:
						pass
					currentComponent.voltage = currentComponent.current * resistance

		return True
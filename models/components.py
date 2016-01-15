#!/usr/bin/env python3

from enum import IntEnum
from math import inf

class Direction(IntEnum):
	Left = 0
	Top = 1
	Right = 2
	Bottom = 3

	def opposite(self):
		return Direction((self + 2) % 4)

class ComponentType(IntEnum):
	Bulb = 0
	Battery = 1
	Switch = 2
	Button = 3
	Resistor = 4
	Ammeter = 5
	Voltmeter = 6 
	Wire = 7

	def __str__(self):
		names = ["Bulb", "Battery", "Switch", "Button", "Resistor", "Ammeter", "Voltmeter", "Wire"]
		return names[self]

class Component:
	def __init__(self, componentType=None):
		self.id = None
		self.type = componentType
		self.voltage = 0.0
		self.current = 0.0
		self.position = (None, None)
		self.connections = [None for _ in range(4)]

	def __str__(self):
		toReturn = "%s component with %g volts and %g amperes at position (%d, %d)" % (self.type, self.voltage, self.current, self.position[0], self.position[1])
		"""
		
		if self.connections[Direction.Left] is not None:
			toReturn += "\n\tleft: %s component" % (self.connections[Direction.Left].type)
		if self.connections[Direction.Right] is not None:
			toReturn += "\n\tright: %s component" % (self.connections[Direction.Right].type)
		if self.connections[Direction.Top] is not None:
			toReturn += "\n\ttop: %s component" % (self.connections[Direction.Top].type)
		if self.connections[Direction.Bottom] is not None:
			toReturn += "\n\tbottom: %s component" % (self.connections[Direction.Bottom].type)
		"""
		return toReturn

	def numberOfConnections(self):
		return sum([1 for x in self.connections if x is not None and isinstance(x.type, ComponentType)])

	# remove references to self in neighbors & set connections to None
	def removeConnections(self):
		for direction in Direction:
			neighbor = self.connections[direction]
			if neighbor is not None:
				neighbor.connections[direction.opposite()] = None
			self.connections[direction] = None

	def exitingConnections(self, directionOfCurrent):
		toReturn = []
		for currentDirection in Direction:
			if currentDirection is not directionOfCurrent.opposite():
				connectionInCurrentDirection = self.connections[currentDirection]
				toAppend = self.connections[currentDirection]
				if toAppend is not None:
					toReturn.append(toAppend)
		return toReturn

class Bulb(Component):
	def __init__(self, resistance=3):
		Component.__init__(self, ComponentType.Bulb)
		self.resistance = resistance

	def isOn(self):
		return self.voltage > 0 and self.current > 0

class Switch(Component):
	def __init__(self):
		Component.__init__(self, ComponentType.Switch)
		self.closed = False

	def flip(self):
		self.closed = not self.closed

class Button(Switch):
	def __init__(self):
		Switch.__init__(self)
		self.type = ComponentType.Button

class Resistor(Component):
	def __init__(self, resistance=1):
		Component.__init__(self, ComponentType.Resistor)
		self.resistance = resistance

class Battery(Component):
	def __init__(self, voltage=9):
		Component.__init__(self, ComponentType.Battery)
		self.negativeTerminal = Direction.Right
		self.voltage= voltage

class Ammeter(Component):
	def __init__(self):
		Component.__init__(self, ComponentType.Ammeter)

class Voltmeter(Component):
	def __init__(self):
		Component.__init__(self, ComponentType.Voltmeter)
		self.resistance = inf

class Wire(Component):
	def __init__(self):
		Component.__init__(self, ComponentType.Wire)
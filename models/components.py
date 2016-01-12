#!/usr/bin/env python3

from enum import IntEnum

class Direction(IntEnum):
	Left = 0
	Top = 1
	Right = 2
	Bottom = 3

class ComponentType(IntEnum):
	LED = 0
	Battery = 1
	Switch = 2
	Button = 3
	Resistor = 4
	Ammeter = 5
	Voltmeter = 6 

class Component:
	def __init__(self, componentType=None):
		self.voltage = 0.0
		self.current = 0.0
		self.resistance = 0.0
		self.position = (None, None)
		self.connections = [None for _ in range(4)]
		self.type = componentType

	def __str__(self):
		return "%s component with %g volts and %g amperes at position (%d, %d)" % (self.type, self.voltage, self.current, self.position[0], self.position[1])

	def numberOfConnections():
		return sum([1 for x in self.connections if x is not None and isinstance(x.type, ComponentType)])

class LED(Component):
	def __init__(self):
		Component.__init__(self, ComponentType.LED)

class Switch(Component):
	def __init__(self, componentType=None):
		Component.__init__(self, ComponentType.Switch)
		self.closed = False

	def flip(self):
		self.closed = not self.closed

class Button(Component):
	def __init__(self):
		Switch.__init__(self, ComponentType.Button)

class Battery(Component):
	def __init__(self):
		Component.__init__(self, ComponentType.Battery)
		self.negative = Direction.Right

class Ammeter(Component):
	def __init__(self):
		Component.__init__(self, ComponentType.Ammeter)

class Voltmeter(Component):
	def __init__(self):
		Component.__init__(self, ComponentType.Voltmeter)
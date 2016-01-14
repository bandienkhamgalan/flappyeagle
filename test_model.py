import pytest
from models.MainModel import MainModel
from controllers.MainController import MainController
from models.components import * 
import math

class TestComponent:
	def init_newComponent_initializesValues_base(self, component):
		assert hasattr(component, 'id')
		assert hasattr(component, 'current')
		assert hasattr(component, 'position')
		assert hasattr(component, 'connections')
		assert hasattr(component, 'voltage')
		assert hasattr(component, 'type')
		assert component.id is None
		assert component.current is 0
		assert component.position is (None, None)
		assert component.connections == [None, None, None, None]

	def init_newComponent_initializesValues(self):
		component = Component()
		self.init_newComponent_initializesValues_base(component)
		assert component.voltage is 0
		assert component.type is None

	def init_newBattery_initializesValues(self):
		component = Battery()
		self.init_newComponent_initializesValues_base(component)
		assert component.type is ComponentType.Battery
		assert hasattr(component, 'negativeSide')
		assert component.negativeSide is Direction.Right

		component = Bulb(5)
		assert component.resistance is 5

	def init_newBulb_initializesValues(self):
		component = Bulb()
		self.init_newComponent_initializesValues_base(component)
		assert component.type is ComponentType.Bulb
		assert hasattr(component, 'resistance')
		assert component.resistance is 3

		component = Bulb(5)
		assert component.resistance is 5

	def init_newResistor_initializesValues(self):
		component = Resistor()
		self.init_newComponent_initializesValues_base(component)
		assert component.type is ComponentType.Resistor
		assert hasattr(component, 'resistance')
		assert component.resistance is 1

		component = Resistor(5)
		assert component.resistance is 5

	def init_newSwitch_initializesValues(self):
		component = Switch()
		self.init_newComponent_initializesValues_base(component)
		assert component.type is ComponentType.Switch
		assert hasattr(component, 'closed')
		assert component.closed is False

	def init_newButton_initializesValues(self):
		component = Switch()
		self.init_newComponent_initializesValues_base(component)
		assert component.type is ComponentType.Button
		assert hasattr(component, 'closed')
		assert component.closed is False

	def init_newAmmeter_initializesValues(self):
		component = Ammeter()
		self.init_newComponent_initializesValues_base(component)
		assert component.type is ComponentType.Ammeter

	def init_newVoltmeter_initializesValues(self):
		component = Ammeter()
		self.init_newComponent_initializesValues_base(component)
		assert component.type is ComponentType.Voltmeter
		assert hasattr(component, 'resistance')
		assert component.resistance is math.inf

	def init_newWire_initializesValues(self):
		component = Wire()
		self.init_newComponent_initializesValues_base(component)
		assert component.type is ComponentType.Wire

	def numberOfConnections_noConnections_returnsCorrectValue(self):
		component = Component()
		assert component.numberOfConnections() is 0
		for x in range(4):
			component.connections[x] = Component()
			assert component.numberOfConnections is x + 1
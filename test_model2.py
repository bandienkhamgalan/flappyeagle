import unittest
from models.MainModel import MainModel
from controllers.MainController import MainController
from controllers.CircuitLogicController import CircuitLogicController
from models.components import * 
import math

class TestComponent(unittest.TestCase):
	def test_newComponent_initializesValues_base(self):
		component = Component()
		self.assertTrue(hasattr(component, 'id'))
		self.assertTrue(hasattr(component, 'position'))
		self.assertTrue(hasattr(component, 'connections'))
		self.assertTrue(hasattr(component, 'voltage'))
		self.assertTrue(hasattr(component, 'type'))
		self.assertTrue(hasattr(component, 'current'))
		self.assertTrue(component.id == None)
		self.assertTrue(component.current == 0)
		self.assertTrue(component.position == (None, None))
		self.assertTrue(component.connections == [None, None, None, None])

	def test_newComponent_initializesValues(self):
		component = Component()
		self.assertTrue(component.voltage == 0)
		self.assertTrue(component.type is None)

	def test_newBattery_initializesValues(self):
		component = Battery()
		self.assertTrue(component.type is ComponentType.Battery)
		self.assertTrue(hasattr(component, 'negativeSide'))
		self.assertTrue(component.negativeSide is Direction.Right)

		component = Bulb(5)
		self.assertTrue(component.resistance is 5)

	def test_newBulb_initializesValues(self):
		component = Bulb()
		self.assertTrue(component.type is ComponentType.Bulb)
		self.assertTrue(hasattr(component, 'resistance'))
		self.assertTrue(component.resistance is 3)

		component = Bulb(5)
		self.assertTrue(component.resistance is 5)

	def test_newResistor_initializesValues(self):
		component = Resistor()
		self.assertTrue(component.type is ComponentType.Resistor)
		self.assertTrue(hasattr(component, 'resistance'))
		self.assertTrue(component.resistance is 1)

		component = Resistor(5)
		self.assertTrue(component.resistance is 5)

	def test_newSwitch_initializesValues(self):
		component = Switch()
		self.assertTrue(component.type is ComponentType.Switch)
		self.assertTrue(hasattr(component, 'closed'))
		self.assertTrue(component.closed is False)

	def test_newButton_initializesValues(self):
		component = Button()
		self.assertTrue(component.type is ComponentType.Button)
		self.assertTrue(hasattr(component, 'closed'))
		self.assertTrue(component.closed is False)

	def test_newAmmeter_initializesValues(self):
		component = Ammeter()
		self.assertTrue(component.type is ComponentType.Ammeter)

	def test_newVoltmeter_initializesValues(self):
		component = Voltmeter()
		self.assertTrue(component.type is ComponentType.Voltmeter)
		self.assertTrue(hasattr(component, 'resistance'))
		self.assertTrue(component.resistance is math.inf)

	def test_newWire_initializesValues(self):
		component = Wire()
		self.assertTrue(component.type is ComponentType.Wire)

	def numberOfConnections_noConnections_returnsCorrectValue(self):
		component = Component()
		self.assertTrue(component.numberOfConnections() is 0)
		for x in range(4):
			component.connections[x] = Component()
			self.assertTrue(component.numberOfConnections is x + 1)

class TestModel(unittest.TestCase):
	def setUp(self):
		self.model = MainModel()
		self.bulb = Bulb()
		self.bulb.position = (1,1)
		self.model.addComponent(self.bulb)
		self.wire1 = Wire()
		self.wire1.position = (0,1)
		self.model.addComponent(self.wire1)
		self.wire2 = Bulb()
		self.wire2.position = (1,0)
		self.model.addComponent(self.wire2)
		self.wire3 = Bulb()
		self.wire3.position = (2,1)
		self.model.addComponent(self.wire3)
		self.wire4 = Bulb()
		self.wire4.position = (1,2)
		self.model.addComponent(self.wire4)
	
	def test_addComponent(self):
		self.assertTrue(self.model.breadboard[1][1] is self.bulb)
		self.assertTrue(self.model.breadboard[0][1] is self.wire1)
		self.assertTrue(self.model.breadboard[1][0] is self.wire2)
		self.assertTrue(self.model.breadboard[2][1] is self.wire3)
		self.assertTrue(self.model.breadboard[1][2] is self.wire4)
	
	def test_addConnection(self):
		self.model.addConnection(self.bulb, self.wire1)
		self.assertTrue(self.bulb.connections[0] is self.wire1)
		self.assertTrue(self.wire1.connections[2] is self.bulb)
		self.model.addConnection(self.bulb, self.wire2)
		self.assertTrue(self.bulb.connections[1] is self.wire2)
		self.assertTrue(self.wire2.connections[3] is self.bulb)
		self.model.addConnection(self.bulb, self.wire3)
		self.assertTrue(self.bulb.connections[2] is self.wire3)
		self.assertTrue(self.wire3.connections[0] is self.bulb)
		self.model.addConnection(self.bulb, self.wire4)
		self.assertTrue(self.bulb.connections[3] is self.wire4)
		self.assertTrue(self.wire4.connections[1] is self.bulb)
	
	def test_removeComponent(self):
		self.model.removeComponent(self.bulb)
		self.assertTrue(self.model.breadboard[1][1] is None)
		self.assertTrue(self.wire1.connections[2] is None)
		self.assertTrue(self.wire2.connections[3] is None)
		self.assertTrue(self.wire3.connections[0] is None)
		self.assertTrue(self.wire4.connections[1] is None)
	
	def test_moveComponent(self):
		self.model.moveComponent(self.bulb, (9,9))
		self.assertTrue(self.model.breadboard[9][9] is self.bulb)

class TestCircuitLogic(unittest.TestCase):
	def setUp(self):
		self.model1 = MainModel()
		self.battery = Battery()
		self.battery.position = (1,1)
		self.model1.addComponent(self.battery)
		self.bulb = Bulb()
		self.bulb.position = (1,2)
		self.model1.addComponent(self.bulb)
		self.wire1 = Wire()
		self.wire1.position = (0,1)
		self.model1.addComponent(self.wire1)
		self.wire2 = Wire()
		self.wire2.position = (0,2)
		self.model1.addComponent(self.wire2)
		self.wire3 = Wire()
		self.wire3.position = (3,1)
		self.model1.addComponent(self.wire3)
		self.wire4 = Wire()
		self.wire4.position = (3,2)
		self.model1.addComponent(self.wire4)
		self.wire5 = Wire()
		self.wire5.position = (2,1)
		self.model1.addComponent(self.wire5)
		self.wire6 = Wire()
		self.wire6.position = (2,2)
		self.model1.addComponent(self.wire6)
		self.model1.addConnection(self.battery,self.wire1)
		self.model1.addConnection(self.battery,self.wire5)
		self.model1.addConnection(self.bulb,self.wire2)
		self.model1.addConnection(self.bulb,self.wire6)
		self.model1.addConnection(self.wire1,self.wire2)
		self.model1.addConnection(self.wire3,self.wire4)
		self.model1.addConnection(self.wire5,self.wire3)
		self.model1.addConnection(self.wire6,self.wire4)
		self.circuitLogicController = CircuitLogicController(self.model1)
	
	def test_currentWithOneBulb(self):
		self.assertTrue(self.bulb.current == 0)
		self.circuitLogicController.runBreadboard()
		self.assertTrue(self.bulb.current == 3)
	
	def test_currentWithMultipleResistors(self):
		self.model1.removeComponent(self.wire6)
		resistor = Resistor()
		resistor.position = (2,2)
		self.model1.addComponent(resistor)
		self.model1.addConnection(self.bulb,resistor)
		self.model1.addConnection(resistor,self.wire4)
		self.assertTrue(self.bulb.current == 0)
		self.assertTrue(resistor.current == 0)
		self.circuitLogicController.runBreadboard()
		self.assertTrue(self.bulb.current == 2.25)
		self.assertTrue(resistor.current == 2.25)
	
	def test_voltageWithMultipleBatteries(self):
		self.model1.removeComponent(self.wire5)
		battery2 = Battery()
		battery2.position = (2,1)
		self.model1.addComponent(battery2)
		self.model1.addConnection(self.battery,battery2)
		self.model1.addConnection(battery2,self.wire3)
		self.assertTrue(self.bulb.current == 0)
		self.circuitLogicController.runBreadboard()
		self.assertTrue(self.bulb.current == 6)

if __name__ == '__main__':
    unittest.main()
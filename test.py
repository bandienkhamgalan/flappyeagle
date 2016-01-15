from models.MainModel import MainModel
from controllers.CircuitLogicController import CircuitLogicController
from models.components import * 

model = MainModel()

wire = Wire()
wire.position = (0, 0)
model.addComponent(wire)

battery = Battery()
wire.position = (1, 0)
model.addComponent(wire)

wire2 = Battery()
wire2.position = (2, 0)
model.addComponent(wire2)

wire3 = Wire()
wire3.position = (2, 1)
model.addComponent(wire3)

bulb = Bulb()
bulb.position = (1, 1)
model.addComponent(bulb)

wire4 = Wire()
wire4.position = (0, 1)
model.addComponent(wire4)

wire5 = Wire()
wire5.position = (0, 2)
model.addComponent(wire5)

resistor = Resistor()
resistor.position = (1, 2)
model.addComponent(resistor)

wire6 = Wire()
wire6.position = (2, 2)
model.addComponent(wire6)

model.addConnection(wire, battery)
model.addConnection(battery, wire2)
model.addConnection(wire2, wire3)
model.addConnection(wire3, bulb)
model.addConnection(bulb, wire4)
model.addConnection(wire4, wire5)
model.addConnection(wire5, resistor)
model.addConnection(resistor, wire6)
model.addConnection(wire6, wire3)

circuitLogic = CircuitLogicController(model)
# circuitLogic.printBreadboard()
circuitLogic.runBreadboard()
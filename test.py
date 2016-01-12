from models.MainModel import MainModel
from controllers.MainController import MainController
from models.components import * 

model = MainModel()
controller = MainController(model)

battery = Battery()
battery2 = Battery()
wire = Wire()
wire2 = Wire()
wire3 = Wire()
wire4 = Wire()
bulb = Bulb()
switch  = Switch()
switch.flip()

battery.connections[Direction.Right] = battery2
battery2.connections[Direction.Left] = battery
battery2.connections[Direction.Right] = wire
wire.connections[Direction.Left] = battery2
wire.connections[Direction.Bottom] = wire4
wire4.connections[Direction.Top] = wire

wire4.connections[Direction.Left] = bulb
bulb.connections[Direction.Right] = wire4

bulb.connections[Direction.Left] = switch
switch.connections[Direction.Right] = bulb

switch.connections[Direction.Left] = wire2
wire2.connections[Direction.Right] = switch
wire2.connections[Direction.Top] = wire3
wire3.connections[Direction.Bottom] = wire2
wire3.connections[Direction.Right] = battery
battery.connections[Direction.Left] = wire3

model.addComponent(battery)
model.addComponent(battery2)
model.addComponent(switch)
model.addComponent(bulb)
model.addComponent(wire)
model.addComponent(wire2)
model.addComponent(wire3)
model.addComponent(wire4)

controller.runBreadboard()
controller.printBreadboard()
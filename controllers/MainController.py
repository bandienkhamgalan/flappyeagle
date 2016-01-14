#!/usr/bin/env python3

from models.components import *
from controllers.CircuitLogicController import CircuitLogicController
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtCore import Qt, QMimeData, QPoint
from enum import Enum
# from views.MainView import * 

class Tool(Enum):
	Select = 0 
	Wire = 1
	Delete = 2
	NewComponent = 3

class MouseState(Enum):
	Normal = 0
	Dragging = 1

class Mode(Enum):
	Build = 0
	Run = 1

class MainController():
	def __init__(self, model=None, view=None):
		self._view = None
		self._model = None

		# instantiate sub controllers
		self.circuitLogic = CircuitLogicController(model)

		# default states
		self.previousTool = None
		self._mode = Mode.Run
		self._tool = Tool.Select
		self._mouseState = MouseState.Normal

		# circuit diagram variables
		#   wire tool
		self.wirePath = []
		self.currentBlock = (None, None)
		#   drag and drop new component
		self.newComponentType = None
		# 	drag and drop existing component
		self._selection = None

		# run mode variable
		self.buttonHeld = (None, None)

		self.view = view
		self.model = model 

	@property
	def view(self):
		return self._view
	@view.setter
	def view(self, value):
		if self.view is None and value is not self.view:
			self._view = value
			self.updateProperties()
	
	@property
	def mode(self):
		return self._mode
	@mode.setter
	def mode(self, value):
		if value is not self.mode:
			self._mode = value
			if self.mode is Mode.Run:
				self.circuitLogic.runBreadboard()
			else:
				self.circuitLogic.bulbsOff()
		self.view.updateCursorAndToolButtons(self.mode, self.tool, self.mouseState)
	
	@property
	def tool(self):
		return self._tool
	@tool.setter
	def tool(self, value):
		if value is not self._tool:
			self.previousTool = self._tool
			self._tool = value
			self.mode = Mode.Build
			self.view.ui.circuitDiagram.shouldShowSelection = self.tool is Tool.Select
		self.view.updateCursorAndToolButtons(self.mode, self.tool, self.mouseState)

	@property
	def mouseState(self):
		return self._mouseState
	@mouseState.setter
	def mouseState(self, value):
		if value is not self._mouseState:
			self._mouseState = value
			if self.tool is Tool.Select:
				self.view.ui.circuitDiagram.dragging = value is MouseState.Dragging
		self.view.updateCursorAndToolButtons(self.mode, self.tool, self.mouseState)

	@property
	def selection(self):
	    return self._selection
	@selection.setter
	def selection(self, value):
		if self.selection is not value:
			self._selection = value
			self.updateProperties()
			self.view.ui.circuitDiagram.selection = self.selection

	def updateProperties(self):
		if self.view is not None:
			self.view.ui.componentTypeLabel.hide()
			self.view.ui.componentType.hide()
			self.view.ui.componentType.clear()
			self.view.ui.voltageLabel.hide()
			self.view.ui.voltage.hide()
			self.view.ui.resistanceLabel.hide()
			self.view.ui.resistance.hide()
			self.view.ui.closedLabel.hide()
			self.view.ui.closed.hide()
			self.view.ui.currentLabel.hide()
			self.view.ui.current.hide()
			if self.selection is not None:
				self.view.ui.componentTypeLabel.show()
				self.view.ui.componentType.show()
				self.view.ui.componentType.addItem("%s" % self.selection.type)
				if self.selection.type is ComponentType.Battery:
					self.view.ui.voltageLabel.show()
					self.view.ui.voltage.show()
					self.view.ui.voltage.setValue(self.selection.voltage)
				elif self.selection.type is ComponentType.Bulb or self.selection.type is ComponentType.Resistor:
					self.view.ui.resistanceLabel.show()
					self.view.ui.resistance.show()
					self.view.ui.voltage.setValue(self.selection.resistance)
				elif self.selection.type is ComponentType.Switch or self.selection.type is ComponentType.Button:
					self.view.ui.closedLabel.show()
					self.view.ui.closed.show()
					self.view.ui.closed.setChecked(self.selection.closed)
			
	def circuitDiagramMousePress(self, index, coordinate):
		if self.mode is Mode.Build:
			if self.tool is Tool.Select:
				if self.model.componentAtIndex(index) is not None:
					self.view.ui.circuitDiagram.draggingStart = coordinate
					print("about to start dragging: ", self.view.ui.circuitDiagram.draggingStart)
					self.selection = self.model.componentAtIndex(index)
					self.mouseState = MouseState.Dragging
			elif self.tool is Tool.Wire:
				if self.model.componentAtIndex(index) is not None:
					# print("starting wire at ", index)
					self.mouseState = MouseState.Dragging
					self.currentBlock = index
					self.wirePath = [index]
				else:
					pass
					# print("invalid wire start")
			elif self.tool is Tool.Delete:
				if self.model.componentAtIndex(index) is not None:
					self.model.removeComponentAtIndex(index)
		elif self.mode is Mode.Run:
			if self.model.componentAtIndex(index) is not None:
				if self.model.componentAtIndex(index).type is ComponentType.Switch:
					self.model.componentAtIndex(index).flip()
					self.circuitLogic.runBreadboard()
				elif self.model.componentAtIndex(index).type is ComponentType.Button:
					self.model.componentAtIndex(index).flip()
					self.buttonHeld = index
					self.circuitLogic.runBreadboard()

	def circuitDiagramMouseMove(self, index, coordinate):
		if self.tool is Tool.Select and self.mouseState is MouseState.Dragging:
			if self.model.validIndex(index):
				pass # print("moving %s to %s" % (self.selectedComponent, index))
			else:
				self.mouseState = MouseState.Normal
		elif self.tool is Tool.NewComponent and self.mouseState is MouseState.Dragging:
			pass
		elif self.tool is Tool.Wire and self.mouseState is MouseState.Dragging:
			if not self.model.validIndex(index):
				#print("invalid wire")
				self.mouseState = MouseState.Normal
			else:
				if index != self.currentBlock:
					#print("move wire to ", index)
					self.wirePath.append(index)
					print(self.wirePath)
					self.currentBlock = index
					if self.model.componentAtIndex(self.currentBlock) is not None:
						if self.model.componentAtIndex(self.currentBlock).numberOfConnections() < 2:
							# wire has formed a connection to existing component
							self.model.addConnection(self.model.componentAtIndex(self.wirePath[-2]), self.model.componentAtIndex(self.wirePath[-1]))
							if self.model.componentAtIndex(self.currentBlock).type in [ComponentType.Battery, ComponentType.Switch, ComponentType.Button, ComponentType.Resistor] and (self.currentBlock[0] == self.wirePath[-2][0]):
								self.wirePath.pop()
								self.wirePath.pop(0)
								for block in self.wirePath:
									if self.model.componentAtIndex(block).type is ComponentType.Wire:
										self.model.removeComponentAtIndex(block)
								self.mouseState = MouseState.Normal
						else:
							# wire has formed 3rd connection to existing component -> end and destroy wires in invalid path here
							self.wirePath.pop()
							self.wirePath.pop(0)
							for block in self.wirePath:
								if self.model.componentAtIndex(block).type is ComponentType.Wire:
									self.model.removeComponentAtIndex(block)
							self.mouseState = MouseState.Normal
					else:
						# restrict wires coming in and out of horizontal components to horizontal
						if (len(self.wirePath) == 2) and (self.model.componentAtIndex(self.wirePath[0]).type in [ComponentType.Battery, ComponentType.Switch, ComponentType.Button, ComponentType.Resistor]) and (self.wirePath[0][0] == self.wirePath[1][0]):
							# invalid wire direction coming out of horizontal component -> end and destroy wires in invalid path here
							self.wirePath.pop()
							self.wirePath.pop(0)
							for block in self.wirePath:
								if self.model.componentAtIndex(block).type is ComponentType.Wire:
									self.model.removeComponentAtIndex(block)
							self.mouseState = MouseState.Normal
						else: 
							if self.model.componentAtIndex(self.wirePath[-2]).numberOfConnections() > 1:
								# trying to add a wire which would create a 3rd connection on previous wire -> end invalid wire keep valid portion of wire up to invalid component
								self.mouseState = MouseState.Normal
							else:
								wireComponent = Wire()
								wireComponent.position = self.wirePath[-1]
								if self.model.addComponent(wireComponent):
									print("added wire")
								else:
									print("could not add wire")
								#print(self.wirePath)
								
								self.model.addConnection(self.model.componentAtIndex(self.wirePath[-2]), self.model.componentAtIndex(self.wirePath[-1]))

	def circuitDiagramMouseRelease(self, index, coordinate):
		if self.mode is Mode.Build:
			if self.tool is Tool.Select:
				if self.mouseState is MouseState.Normal:
					self.selection = self.model.componentAtIndex(index)
				elif self.mouseState is MouseState.Dragging:
					if self.model.validIndex(index) and self.model.componentAtIndex(index) is None:
						self.model.moveComponent(self.selection, index)
						print("moved %s to %s" % (self.selection, index))
					else:
						print("invalid move")
			elif self.tool is Tool.Wire:
				if self.model.validIndex(index):
					print("valid end wire at ", index)
				else:
					print("invalid wire")	
			elif self.tool is Tool.NewComponent:
				newComponent = None
				if self.model.validIndex(index) and self.model.componentAtIndex(index) is None:
					if self.newComponentType is ComponentType.Battery:
						newComponent = Battery()
					elif self.newComponentType is ComponentType.Bulb:
						newComponent = Bulb()
					elif self.newComponentType is ComponentType.Resistor:
						newComponent = Resistor()
					elif self.newComponentType is ComponentType.Switch:
						newComponent = Switch()
					elif self.newComponentType is ComponentType.Button:
						newComponent = Button()
					elif self.newComponentType is ComponentType.Ammeter:
						newComponent = Ammeter()
					elif self.newComponentType is ComponentType.Voltmeter:
						newComponent = Voltmeter()

					if newComponent is not None:
						newComponent.position = index
						self.model.addComponent(newComponent)
				self.tool = self.previousTool
				self.mouseState = MouseState.Normal
				self.selection = newComponent	
		elif self.mode is Mode.Run:
			if self.buttonHeld != (None, None):
				self.model.componentAtIndex(self.buttonHeld).flip()
				self.buttonHeld = (None, None)
				self.circuitLogic.runBreadboard()	
	
		self.mouseState = MouseState.Normal

	def newComponentButtonMousePress(self, componentType, event):
		self.tool = Tool.NewComponent
		self.mouseState = MouseState.Dragging
		self.newComponentType = componentType
		
		newComponentDrag = QDrag(self.view)
		newComponentDrag.setHotSpot(QPoint(self.view.ui.circuitDiagram.blockSideLength / 2, self.view.ui.circuitDiagram.blockSideLength / 2))
		newComponentDrag.setMimeData(QMimeData())
		newComponentDrag.setPixmap(QPixmap(self.view.ui.circuitDiagram.componentTypeToImageName(componentType)).scaled(self.view.ui.circuitDiagram.blockSideLength, self.view.ui.circuitDiagram.blockSideLength))
		newComponentDrag.exec_(Qt.MoveAction)
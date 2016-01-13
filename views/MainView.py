#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QCursor, QDrag, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt, QSize, QMimeData, QPoint
from views.mainWindow import Ui_mainWindow
from models import MainModel
from models.components import *
from controllers import MainController
from enum import Enum

class CursorState(Enum):
	Select = 0
	Wire = 1
	WireDragging = 2
	NewComponentDragging = 3
	ExistingComponentDragging = 4
	Delete = 5

class MainView(QMainWindow):
	def __init__(self, model, controller):
		QWidget.__init__(self)

		self.controller = controller
		self.model = model

		# load QtDesigner UI 
		self.ui = Ui_mainWindow()
		self.ui.setupUi(self)

		#### SETUP CircuitDiagramView MODEL
		self.ui.circuitDiagram.setModel(self.model)
		# circuit diagram drag and drop
		self.selectedComponent = None
		self.cursorState = CursorState.Select
		# connect to CircuitDiagramView mouse triggers
		self.ui.circuitDiagram.mousePress.connect(self.circuitDiagramMousePress)
		self.ui.circuitDiagram.mouseMove.connect(self.circuitDiagramMouseMove)
		self.ui.circuitDiagram.mouseRelease.connect(self.circuitDiagramMouseRelease)

		#### SETUP TOOLBAR
		self.ui.wireMode.setCheckable(True)
		self.ui.wireMode.clicked.connect(self.toggleWireMode)

		self.ui.deleteMode.setCheckable(True)
		self.ui.deleteMode.clicked.connect(self.toggleDeleteMode)
		
		self.ui.selectMode.setCheckable(True)
		self.ui.selectMode.clicked.connect(self.toggleSelectMode)
		self.ui.selectMode.setChecked(True)

		# toolbar drag and drop
		self.newComponentDrag = None
		self.newComponentType = None
		
		self.toolbarComponents = []
		self.ui.newBattery.componentType = ComponentType.Battery
		self.toolbarComponents.append(self.ui.newBattery)

		self.ui.newBulb.componentType = ComponentType.Bulb
		self.toolbarComponents.append(self.ui.newBulb)

		self.ui.newResistor.componentType = ComponentType.Resistor
		self.toolbarComponents.append(self.ui.newResistor)

		self.ui.newSwitch.componentType = ComponentType.Switch
		self.toolbarComponents.append(self.ui.newSwitch)

		self.ui.newButton.componentType = ComponentType.Button
		self.toolbarComponents.append(self.ui.newButton)

		self.ui.newAmmeter.componentType = ComponentType.Ammeter
		self.toolbarComponents.append(self.ui.newAmmeter)

		self.ui.newVoltmeter.componentType = ComponentType.Voltmeter
		self.toolbarComponents.append(self.ui.newVoltmeter)

		for toolbarButton in self.toolbarComponents:
			toolbarButton.setIcon(QIcon(QPixmap(self.ui.circuitDiagram.componentTypeToImageName(toolbarButton.componentType))))
			toolbarButton.setIconSize(QSize(50, 50))
			toolbarButton.mousePress.connect(self.newComponentButtonMousePress)

		self.statusBar().showMessage('Ready')

		self.ui.actionNew.setShortcut('Ctrl+N')
		self.ui.actionNew.setStatusTip('New document')
		
		self.wirePath = []
		self.currentBlock = (None,None)

	def newComponentButtonMousePress(self, componentType, event):
		self.cursorState = CursorState.NewComponentDragging
		self.newComponentType = componentType
		self.newComponentDrag = QDrag(self)
		self.newComponentDrag.setHotSpot(QPoint(self.ui.circuitDiagram.blockSideLength / 2, self.ui.circuitDiagram.blockSideLength / 2))
		self.newComponentDrag.setMimeData(QMimeData())
		self.newComponentDrag.setPixmap(QPixmap(self.ui.circuitDiagram.componentTypeToImageName(componentType)).scaled(self.ui.circuitDiagram.blockSideLength, self.ui.circuitDiagram.blockSideLength))
		QApplication.setOverrideCursor(QCursor(Qt.ForbiddenCursor))
		self.newComponentDrag.exec_(Qt.MoveAction)

		self.cursorState = CursorState.Select
		self.updateCursor()

	def updateCursor(self):
		if self.cursorState is CursorState.Wire or self.cursorState is CursorState.WireDragging:
			QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
		elif self.cursorState is CursorState.ExistingComponentDragging or self.cursorState is CursorState.NewComponentDragging:
			QApplication.setOverrideCursor(QCursor(Qt.ClosedHandCursor))
		elif self.cursorState is CursorState.Delete:
			QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
		else:
			QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))

	def toggleWireMode(self):
		self.ui.deleteMode.setChecked(False)
		self.ui.selectMode.setChecked(False)
		self.cursorState = CursorState.Wire if self.ui.wireMode.isChecked() else CursorState.Select
		if self.cursorState is CursorState.Select :
			self.ui.selectMode.setChecked(True)
		self.updateCursor()
		
	def toggleDeleteMode(self):
		self.ui.wireMode.setChecked(False)
		self.ui.selectMode.setChecked(False)
		self.cursorState = CursorState.Delete if self.ui.deleteMode.isChecked() else CursorState.Select
		if self.cursorState is CursorState.Select :
			self.ui.selectMode.setChecked(True)
		self.updateCursor()
		
	def toggleSelectMode(self):
		self.ui.wireMode.setChecked(False)
		self.ui.deleteMode.setChecked(False)
		self.cursorState = CursorState.Select if self.ui.selectMode.isChecked() else CusrsorState.Select
		self.updateCursor()

	def circuitDiagramMousePress(self, index, coordinate):
		if self.cursorState is CursorState.Select:
			if self.model.validIndex(index) and self.model.breadboard[index[0]][index[1]] is not None:
				self.cursorState = CursorState.ExistingComponentDragging
				self.selectedComponent = self.model.breadboard[index[0]][index[1]]
				self.ui.circuitDiagram.draggingStart = (coordinate[0], coordinate[1])
				self.ui.circuitDiagram.setSelection(self.selectedComponent)
				self.ui.circuitDiagram.setDragging(True)
		elif self.cursorState is CursorState.Wire:
			if self.model.validIndex(index) and self.model.breadboard[index[0]][index[1]] is not None:
				print("starting wire at ", index)
				self.cursorState = CursorState.WireDragging
				self.currentBlock = index
				self.wirePath.append(index)
			else:
				print("invalid wire start")
		elif self.cursorState is CursorState.Delete:
			if self.model.breadboard[index[0]][index[1]] is not None:
				self.model.removeComponent(self.model.breadboard[index[0]][index[1]])
		self.updateCursor()

	def circuitDiagramMouseMove(self, index, coordinate):
		if self.cursorState is CursorState.WireDragging:
			if not self.model.validIndex(index):
				print("invalid wire")
				self.cursorState = CursorState.Wire
			else:
				if index != self.currentBlock:
					print("move wire to ", index)
					self.wirePath.append(index)
					print(self.wirePath)
					self.currentBlock = index
					if self.model.breadboard[self.currentBlock[0]][self.currentBlock[1]] is not None:
						if self.model.breadboard[self.currentBlock[0]][self.currentBlock[1]].numberOfConnections() < 2:
							print(self.model.addConnection(self.model.breadboard[self.wirePath[-2][0]][self.wirePath[-2][1]],self.model.breadboard[self.wirePath[-1][0]][self.wirePath[-1][1]]))
							if self.model.breadboard[self.currentBlock[0]][self.currentBlock[1]].type in [ComponentType.Battery, ComponentType.Switch, ComponentType.Button, ComponentType.Resistor] and (self.currentBlock[0] == self.wirePath[-2][0]):
								self.wirePath.pop()
								self.wirePath.pop(0)
								for block in self.wirePath:
									if self.model.breadboard[block[0]][block[1]].type is ComponentType.Wire:
										self.model.removeComponent(self.model.breadboard[block[0]][block[1]])
								self.wirePath = []
								self.currentBlock = (None,None)
								self.cursorState = CursorState.Wire
						else:
							self.wirePath.pop()
							self.wirePath.pop(0)
							for block in self.wirePath:
								if self.model.breadboard[block[0]][block[1]].type is ComponentType.Wire:
									self.model.removeComponent(self.model.breadboard[block[0]][block[1]])
							self.wirePath = []
							self.currentBlock = (None,None)
							self.cursorState = CursorState.Wire
					else:
						if (len(self.wirePath) == 2) and (self.model.breadboard[self.wirePath[0][0]][self.wirePath[0][1]].type in [ComponentType.Battery, ComponentType.Switch, ComponentType.Button, ComponentType.Resistor]) and (self.wirePath[0][0] == self.wirePath[1][0]):
							self.wirePath.pop()
							self.wirePath.pop(0)
							for block in self.wirePath:
								if self.model.breadboard[block[0]][block[1]].type is ComponentType.Wire:
									self.model.removeComponent(self.model.breadboard[block[0]][block[1]])
							self.wirePath = []
							self.currentBlock = (None,None)
							self.cursorState = CursorState.Wire
						else:
							wireComponent = Wire()
							wireComponent.position = self.wirePath[-1]
							if self.model.addComponent(wireComponent):
								print("added wire")
							else:
								print("could not add wire")
							#print(self.wirePath)
							print(self.model.addConnection(self.model.breadboard[self.wirePath[-2][0]][self.wirePath[-2][1]],self.model.breadboard[self.wirePath[-1][0]][self.wirePath[-1][1]]))
		elif self.cursorState is CursorState.ExistingComponentDragging:
			if self.model.validIndex(index):
				pass # print("moving %s to %s" % (self.selectedComponent, index))
			else:
				self.ui.circuitDiagram.setDragging(False)
				self.cursorState = CursorState.Select
		elif self.cursorState is CursorState.NewComponentDragging:
			pass
		self.updateCursor()

	def circuitDiagramMouseRelease(self, index, coordinate):
		if self.cursorState is CursorState.Select:
			if self.model.validIndex(index):
				self.ui.circuitDiagram.setSelection(self.model.breadboard[index[0]][index[1]])
			else:
				self.ui.circuitDiagram.setSelection(None)

		if self.cursorState is CursorState.WireDragging:
			if self.model.validIndex(index):
				print("valid end wire at ", index)
				self.wirePath = []
				self.currentBlock = (None,None)
			else:
				print("invalid wire")
			self.cursorState = CursorState.Wire

		elif self.cursorState is CursorState.ExistingComponentDragging:
			if self.model.validIndex(index) and self.model.breadboard[index[0]][index[1]] is None:
				self.model.moveComponent(self.selectedComponent, index)
				print("moved %s to %s" % (self.selectedComponent, index))
			else:
				print("invalid move")
			self.selectedComponent = None
			self.ui.circuitDiagram.setDragging(False)
			self.cursorState = CursorState.Select
		
		elif self.cursorState is CursorState.NewComponentDragging:
			if self.model.validIndex(index) and self.model.breadboard[index[0]][index[1]] is None:
				print("adding component")
				newComponent = None
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

				print(self.newComponentType, ": ", self.ui.circuitDiagram.componentTypeToImageName(self.newComponentType))

				if newComponent is not None:
					newComponent.position = index
					self.model.addComponent(newComponent)
			self.cursorState = CursorState.Select

		self.updateCursor()

	def insertBattery(self):
		# print("in insert battery")
		self.cursorState = CursorState.Select
		self.ui.wireMode.setChecked(False)
		self.updateCursor()

		batteryComponent = Battery()
		batteryComponent.position = self.model.freePosition()
		if self.model.addComponent(batteryComponent):
			pass #print("added battery")
		else:
			pass #print("could not add battery")

	def closeEvent(self, event):
		reply = QMessageBox.question(self, "Message", "Do want to save your changes?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)

		if reply == QMessageBox.No:
			event.accept()
		else:
			event.ignore()
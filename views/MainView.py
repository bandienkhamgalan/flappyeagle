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
		# toolbar drag and drop
		self.newComponentDrag  = None
		self.newComponentType = None

		self.ui.newBattery.componentType = ComponentType.Battery
		self.ui.newBattery.setIcon(QIcon(QPixmap("assets/battery.png")))
		self.ui.newBattery.setIconSize(QSize(50, 50))
		self.ui.newBattery.mousePress.connect(self.newComponentButtonMousePress)

		self.statusBar().showMessage('Ready')

		self.ui.actionNew.setShortcut('Ctrl+N')
		self.ui.actionNew.setStatusTip('New document')

		self.insertBattery()

	def newComponentButtonMousePress(self, componentType, event):
		self.cursorState = CursorState.NewComponentDragging
		self.newComponentType = componentType
		self.newComponentDrag = QDrag(self)
		self.newComponentDrag.setHotSpot(QPoint(self.ui.circuitDiagram.blockSideLength / 2, self.ui.circuitDiagram.blockSideLength / 2))
		self.newComponentDrag.setMimeData(QMimeData())
		self.newComponentDrag.setPixmap(self.ui.circuitDiagram.componentTypeToImage(componentType))
		QApplication.setOverrideCursor(QCursor(Qt.ForbiddenCursor))
		self.newComponentDrag.exec_(Qt.MoveAction)

		self.cursorState = CursorState.Select
		self.updateCursor()

	def updateCursor(self):
		if self.cursorState is CursorState.Wire or self.cursorState is CursorState.WireDragging:
			QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
		elif self.cursorState is CursorState.ExistingComponentDragging or self.cursorState is CursorState.NewComponentDragging:
			QApplication.setOverrideCursor(QCursor(Qt.ClosedHandCursor))
		else:
			QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))

	def toggleWireMode(self):
		self.cursorState = CursorState.Wire if self.ui.wireMode.isChecked() else CursorState.Select
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
			else:
				print("invalid wire start")
		self.updateCursor()

	def circuitDiagramMouseMove(self, index, coordinate):
		if self.cursorState is CursorState.WireDragging:
			if not self.model.validIndex(index):
				print("invalid wire")
				self.cursorState = CursorState.Wire
			else:
				print("move wire to ", index)
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

		elif self.cursorState is CursorState.WireDragging:
			if self.model.validIndex(index):
				print("valid end wire at ", index)
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
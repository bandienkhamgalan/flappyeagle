#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QCursor, QDrag, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt, QSize
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
		# drag and drop
		self.selectedComponent = None
		self.cursorState = CursorState.Select
		# connect to CircuitDiagramView mouse triggers
		self.ui.circuitDiagram.mousePress.connect(self.circuitDiagramMousePress)
		self.ui.circuitDiagram.mouseMove.connect(self.circuitDiagramMouseMove)
		self.ui.circuitDiagram.mouseRelease.connect(self.circuitDiagramMouseRelease)

		#### SETUP TOOLBAR
		self.ui.wireMode.setCheckable(True)
		self.ui.wireMode.clicked.connect(self.toggleWireMode)

		self.ui.newBattery.componentType = ComponentType.Battery
		self.ui.newBattery.setIcon(QIcon(QPixmap("assets/battery.png")))
		self.ui.newBattery.setIconSize(QSize(50, 50))
		#self.ui.newBattery.mouseMove.connect(self.newComponentButtonMouseMove)
		#self.ui.newBattery.mouseRelease.connect(self.newComponentButtonMouseRelease)
		self.ui.newBattery.clicked.connect(self.insertBattery)

		self.statusBar().showMessage('Ready')

		self.ui.actionNew.setShortcut('Ctrl+N')
		self.ui.actionNew.setStatusTip('New document')

	def newComponentButtonMouseMove(componentType, event):
		# if event.buttons() != Qt.LeftButton:
		print("dragging")

	def newComponentButtonMouseRelease(componentType, event):
		# if event.buttons() != Qt.LeftButton:
		print("released")

	def updateCursor(self):
		if self.cursorState is CursorState.Select:
			QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
		elif self.cursorState is CursorState.Wire or self.cursorState is CursorState.WireDragging:
			QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
		elif self.cursorState is CursorState.ExistingComponentDragging or self.cursorState is CursorState.NewComponentDragging:
			QApplication.setOverrideCursor(QCursor(Qt.ClosedHandCursor))
		else:
			QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))

	def toggleWireMode(self):
		self.cursorState = CursorState.Wire if self.ui.wireMode.isChecked() else CursorState.Select
		self.updateCursor()

	def circuitDiagramMousePress(self, event):
		if self.cursorState is CursorState.Select:
			if self.model.validIndex(event.index) and self.model.breadboard[event.index[0]][event.index[1]] is not None:
				self.cursorState = CursorState.ExistingComponentDragging
				self.selectedComponent = self.model.breadboard[event.index[0]][event.index[1]]
				self.ui.circuitDiagram.draggingStart = (event.x(), event.y())
				self.ui.circuitDiagram.setSelection(self.selectedComponent)
				self.ui.circuitDiagram.setDragging(True)

		elif self.cursorState is CursorState.Wire:
			if self.model.validIndex(event.index) and self.model.breadboard[event.index[0]][event.index[1]] is not None:
				print("starting wire at ", event.index)
				self.cursorState = CursorState.WireDragging
			else:
				print("invalid wire start")
		self.updateCursor()

	def circuitDiagramMouseMove(self, event):
		if self.cursorState is CursorState.WireDragging:
			if not self.model.validIndex(event.index):
				print("invalid wire")
				self.cursorState = CursorState.Wire
			else:
				print("move wire to ", event.index)
		elif self.cursorState is CursorState.ExistingComponentDragging:
			if self.model.validIndex(event.index):
				pass # print("moving %s to %s" % (self.selectedComponent, event.index))
			else:
				self.ui.circuitDiagram.setDragging(False)
				self.cursorState = CursorState.Select
				# print("invalid move")

		self.updateCursor()

	def circuitDiagramMouseRelease(self, event):
		if self.cursorState is CursorState.Select:
			if self.model.validIndex(event.index):
				self.ui.circuitDiagram.setSelection(self.model.breadboard[event.index[0]][event.index[1]])
			else:
				self.ui.circuitDiagram.setSelection(None)

		if self.cursorState is CursorState.WireDragging:
			if self.model.validIndex(event.index):
				print("valid end wire at ", event.index)
			else:
				print("invalid wire")
			self.cursorState = CursorState.Wire

		elif self.cursorState is CursorState.ExistingComponentDragging:
			if self.model.validIndex(event.index) and self.model.breadboard[event.index[0]][event.index[1]] is None:
				self.model.moveComponent(self.selectedComponent, event.index)
				print("moved %s to %s" % (self.selectedComponent, event.index))
			else:
				print("invalid move")
			self.selectedComponent = None
			self.ui.circuitDiagram.setDragging(False)
			self.cursorState = CursorState.Select

		self.updateCursor()

	def insertBattery(self):
		print("in insert battery")
		self.cursorState = CursorState.Select
		self.ui.wireMode.setChecked(False)
		self.updateCursor()

		batteryComponent = Battery()
		batteryComponent.position = self.model.freePosition()
		if self.model.addComponent(batteryComponent):
			print("added battery")
		else:
			print("could not add battery")

	def closeEvent(self, event):
		reply = QMessageBox.question(self, "Message", "Do want to save your changes?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)

		if reply == QMessageBox.No:
			event.accept()
		else:
			event.ignore()
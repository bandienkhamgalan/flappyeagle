#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QCursor, QDrag, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt, QSize, QMimeData, QPoint
from views.mainWindow import Ui_mainWindow
from models import MainModel
from models.components import *
from controllers.MainController import *
from enum import Enum

class MainView(QMainWindow):
	def __init__(self, model, controller):
		QWidget.__init__(self)

		self.controller = controller
		self.model = model

		# load QtDesigner UI 
		self.ui = Ui_mainWindow()
		self.ui.setupUi(self)

		#### SETUP CircuitDiagramView and controller
		self.ui.circuitDiagram.model = self.model
		self.ui.circuitDiagram.controller = self.controller

		# connect to CircuitDiagramView mouse triggers
		self.ui.circuitDiagram.mousePress.connect(self.controller.circuitDiagramMousePress)
		self.ui.circuitDiagram.mouseMove.connect(self.controller.circuitDiagramMouseMove)
		self.ui.circuitDiagram.mouseRelease.connect(self.controller.circuitDiagramMouseRelease)

		#### SETUP TOOLBAR
		self.ui.wireMode.clicked.connect(self.setWireMode)
		self.ui.deleteMode.clicked.connect(self.setDeleteMode)
		self.ui.selectMode.clicked.connect(self.setSelectMode)

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
			toolbarButton.mousePress.connect(self.controller.newComponentButtonMousePress)

		self.statusBar().showMessage('Ready')

		self.ui.actionNew.setShortcut('Ctrl+N')
		self.ui.actionNew.setStatusTip('New document')

	def updateCursor(self, tool, mouseState):
		if tool is Tool.Select:
			if mouseState is MouseState.Dragging:
				QApplication.setOverrideCursor(QCursor(Qt.ClosedHandCursor))
			else:
				QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
		elif tool is Tool.Wire:
			QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
		elif tool is Tool.Delete:
			QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
		elif tool is Tool.NewComponent:
			QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
	
	def setSelectMode(self):
		self.ui.selectMode.setChecked(True)
		self.ui.wireMode.setChecked(False)
		self.ui.deleteMode.setChecked(False)
		self.controller.tool = Tool.Select

	def setWireMode(self):
		self.ui.selectMode.setChecked(False)
		self.ui.wireMode.setChecked(True)
		self.ui.deleteMode.setChecked(False)
		self.controller.tool = Tool.Wire
		
	def setDeleteMode(self):
		self.ui.selectMode.setChecked(False)
		self.ui.wireMode.setChecked(False)
		self.ui.deleteMode.setChecked(True)
		self.controller.tool = Tool.Delete

	def closeEvent(self, event):
		reply = QMessageBox.question(self, "Message", "Do want to save your changes?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)

		if reply == QMessageBox.No:
			event.accept()
		else:
			event.ignore()
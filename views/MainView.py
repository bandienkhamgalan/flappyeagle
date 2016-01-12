#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt
from views.mainWindow import Ui_mainWindow
from models import MainModel
from models import components
from controllers import MainController

class MainView(QMainWindow):
	def __init__(self, model, controller):
		QWidget.__init__(self)

		self.controller = controller
		self.model = model

		# load QtDesigner UI 
		self.ui = Ui_mainWindow()
		self.ui.setupUi(self)

		# set CircuitDiagramView model
		self.ui.circuitDiagram.model = self.model

		self.wireMode = False
		# connect to CircuitDiagramView mouse triggers
		self.ui.circuitDiagram.mousePress.connect(self.circuitDiagramMousePress)
		self.ui.circuitDiagram.mouseMove.connect(self.circuitDiagramMouseMove)
		self.ui.circuitDiagram.mouseRelease.connect(self.circuitDiagramMouseRelease)

		self.ui.wireMode.setCheckable(True)
		self.ui.wireMode.clicked.connect(self.updateWireMode)

		self.ui.newBattery.clicked.connect(self.insertBattery)

		self.statusBar().showMessage('Ready')

		self.ui.actionNew.setShortcut('Ctrl+N')
		self.ui.actionNew.setStatusTip('New document')

	def updateWireMode(self):
		self.wireMode = self.ui.wireMode.isChecked()
		QApplication.setOverrideCursor(QCursor(Qt.CrossCursor) if self.wireMode else QCursor(Qt.ArrowCursor))

	def circuitDiagramMousePress(self, index):
		if self.wireMode:
			print("start wire at ", index)

	def circuitDiagramMouseMove(self, index):
		if self.wireMode:
			print("move wire to ", index)

	def circuitDiagramMouseRelease(self, index):
		if self.wireMode:
			print("end wire at ", index)

	def insertBattery(self):
		batteryComponent = components.Battery()
		if self.model.addComponent(batteryComponent):
			self.ui.circuitDiagram.render()

	def closeEvent(self, event):
		reply = QMessageBox.question(self, "Message", "Do want to save your changes?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)

		if reply == QMessageBox.No:
			event.accept()
		else:
			event.ignore()
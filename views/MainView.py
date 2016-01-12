#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QPen, QColor, QBrush, QPixmap, QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt
from views.mainWindow import Ui_mainWindow
from models import MainModel
from models import components
from models.components import ComponentType
from controllers import MainController

class MainView(QMainWindow):
	def __init__(self, model, controller):
		QWidget.__init__(self)

		self.controller = controller
		self.model = model

		# load QtDesigner UI 
		self.ui = Ui_mainWindow()
		self.ui.setupUi(self)

		self.ui.wireMode.setCheckable(True)
		self.ui.wireMode.clicked.connect(self.wireMode)

		self.ui.newBattery.clicked.connect(self.insertBattery)

		self.statusBar().showMessage('Ready')

		self.ui.actionNew.setShortcut('Ctrl+N')
		self.ui.actionNew.setStatusTip('New document')

	def wireMode(self):
		QApplication.setOverrideCursor(QCursor(Qt.CrossCursor) if self.ui.wireMode.isChecked() else QCursor(Qt.ArrowCursor))

	def insertBattery(self):
		batteryComponent = components.Battery()
		if self.model.addComponent(batteryComponent):
			self.renderCircuitDiagram()

	def closeEvent(self, event):
		reply = QMessageBox.question(self, "Message", "Do want to save your changes?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)

		if reply == QMessageBox.No:
			event.accept()
		else:
			event.ignore()
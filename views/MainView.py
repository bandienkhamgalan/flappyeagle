#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QCursor, QDrag, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QGraphicsScene, QGraphicsView, QFileDialog
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

		self.ui.runMode.clicked.connect(self.setRunMode)
		self.ui.buildMode.clicked.connect(self.setBuildMode)
		
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
		
		saveMenu = self.menuBar().addMenu('Save')
		openAction = saveMenu.addAction('Open File...')
		openAction.triggered.connect(self.showFileDialog)
		saveAction = saveMenu.addAction('Save File')
		saveAction.triggered.connect(self.showSaveDialog)
		saveAsAction = saveMenu.addAction('Save As...')
		saveAsAction.triggered.connect(self.saveAs)
		saveAction.setShortcut('Ctrl+S')
		saveAsAction.setShortcut('Ctrl+Shift+S')
		openAction.setShortcut('Ctrl+O')
		
		self.savePath = None

	def saveAs(self):
		fname = QFileDialog.getSaveFileName(self, 'Save file', 'breadboard.eagle')
		if fname[0]:
			self.savePath = fname[0]
			self.model.saveModel(fname[0])
			self.statusBar().showMessage('Saved')
		
	def showFileDialog(self):
		reply = QMessageBox.question(self, "Message", "Opening a new file overwrites the current file. Do you want to save the current file?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
		if reply == QMessageBox.No:
			fname = QFileDialog.getOpenFileName(self, 'Open file', '')
			if fname[0]:
				self.savePath = fname[0]
				if not self.model.readModel(fname[0]):
					QMessageBox.question(self, "Message", "Parsing failed. File may be corrupted.", QMessageBox.Cancel, QMessageBox.Cancel)
				else:
					self.statusBar().showMessage('File Opened. Ready')
		elif reply == QMessageBox.Yes:
			self.showSaveDialog()
			self.statusBar().showMessage('Saved')
	
	def showSaveDialog(self):
		if self.savePath is None:
			self.saveAs()
		else:
			self.model.saveModel(self.savePath)
			self.statusBar().showMessage('Saved')

	def newComponentButtonMousePress(self, componentType, event):
		self.ui.build.setChecked(True)
		self.ui.wireMode.setChecked(False)
		self.ui.deleteMode.setChecked(False)
		self.ui.selectMode.setChecked(True)
		self.controller.bulbsOff()
		self.model.reRender()

		self.cursorState = CursorState.NewComponentDragging
		self.newComponentType = componentType
		self.newComponentDrag = QDrag(self)
		self.newComponentDrag.setHotSpot(QPoint(self.ui.circuitDiagram.blockSideLength / 2, self.ui.circuitDiagram.blockSideLength / 2))
		self.newComponentDrag.setMimeData(QMimeData())
		self.newComponentDrag.setPixmap(QPixmap(self.ui.circuitDiagram.componentTypeToImageName(componentType)).scaled(self.ui.circuitDiagram.blockSideLength, self.ui.circuitDiagram.blockSideLength))
		QApplication.setOverrideCursor(QCursor(Qt.ForbiddenCursor))
		self.newComponentDrag.exec_(Qt.MoveAction)

		self.cursorState = CursorState.Select
		self.ui.selectMode.setChecked(True)
		self.updateCursor()

	def updateCursorAndToolButtons(self, mode, tool, mouseState):
		self.ui.selectMode.setChecked(False)
		self.ui.wireMode.setChecked(False)
		self.ui.deleteMode.setChecked(False)
		self.ui.runMode.setChecked(False)
		self.ui.buildMode.setChecked(False)

		if mode is Mode.Build:
			self.ui.buildMode.setChecked(True)
			if tool is Tool.Select:
				self.ui.selectMode.setChecked(True)
				if mouseState is MouseState.Dragging:
					QApplication.setOverrideCursor(QCursor(Qt.ClosedHandCursor))
				else:
					QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
			elif tool is Tool.Wire:
				self.ui.wireMode.setChecked(True)
				QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
			elif tool is Tool.Delete:
				self.ui.deleteMode.setChecked(True)
				QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
			elif tool is Tool.NewComponent:
				QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
		elif mode is Mode.Run:
			QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
			self.ui.runMode.setChecked(True)

	def setRunMode(self):
		self.controller.mode = Mode.Run

	def setBuildMode(self):
		self.controller.mode = Mode.Build

	def setSelectMode(self):
		self.controller.tool = Tool.Select

	def setWireMode(self):
		self.controller.tool = Tool.Wire
		
	def setDeleteMode(self):
		self.controller.tool = Tool.Delete

	def closeEvent(self, event):
		reply = QMessageBox.question(self, "Message", "Do want to save your changes?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)

		if reply == QMessageBox.No:
			event.accept()
		else:
			self.showSaveDialog()
			event.accept()
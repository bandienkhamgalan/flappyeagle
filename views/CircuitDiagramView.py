#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QPen, QColor, QBrush, QPixmap, QMouseEvent, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt, pyqtSignal
from models.components import ComponentType
from models.components import Direction

class CircuitDiagramView(QGraphicsView):
	mousePress = pyqtSignal(tuple, tuple, name='mousePress')
	mouseMove = pyqtSignal(tuple, tuple, name='mouseMove')
	mouseRelease = pyqtSignal(tuple, tuple, name='mouseRelease')

	def __init__(self, parent=None):
		QGraphicsView.__init__(self, parent)

		self._model = None
		self.controller = None

		self.setAcceptDrops(True)

		# setup & render circuit diagram grid
		self.scene = QGraphicsScene()
		self.setScene(self.scene)

		self._shouldShowSelection = False
		self._selection = None
		self._dragging = False
		self.mousePosition = None
		self.draggingStart = None

		self.render()

	@property
	def shouldShowSelection(self):
		return self._shouldShowSelection

	@shouldShowSelection.setter
	def shouldShowSelection(self, value):
		if self.shouldShowSelection is not value and value is not None:
			self._shouldShowSelection = value
			self.render()		

	@property
	def model(self):
		return self._model

	@model.setter
	def model(self, value):
		self._model = value
		self.model.modelChanged.connect(self.render)

	@property
	def selection(self):
		return self._selection

	@selection.setter
	def selection(self, value):
		if self.selection is not value:
			self._selection = value
			self.render()	

	@property
	def dragging(self):
		return self._dragging

	@dragging.setter
	def dragging(self, value):
		self._dragging = value
		self.render()

	def componentTypeToImageName(self, componentType):
		dictionary = {
			ComponentType.Battery: "assets/battery.png",
			ComponentType.Resistor: "assets/resistor.png",
			ComponentType.Voltmeter: "assets/voltmeter.png",
			ComponentType.Ammeter: "assets/ammeter.png",
			ComponentType.Switch: "assets/switch-off.png",
			ComponentType.Bulb: "assets/bulb-off.png",
			ComponentType.Button: "assets/button-off.png",
		}

		return dictionary[componentType]

	def componentToImage(self, component):
		if component.type == ComponentType.Wire:
			image = QPixmap("assets/icon.png").scaled(self.blockSideLength, self.blockSideLength)
			if component.numberOfConnections() == 1:
				image = QPixmap("assets/wire-top.png").scaled(self.blockSideLength, self.blockSideLength)
				if component.connections[Direction.Right] is not None:
					image = image.transformed(QtGui.QTransform().rotate(90))
				elif component.connections[Direction.Bottom] is not None:
					image = image.transformed(QtGui.QTransform().rotate(180))
				elif component.connections[Direction.Left] is not None:
					image = image.transformed(QtGui.QTransform().rotate(270))
			elif component.numberOfConnections() == 2:
				if component.connections[Direction.Left] is not None and component.connections[Direction.Right] is not None:
					image = QPixmap("assets/wire-left-right.png").scaled(self.blockSideLength, self.blockSideLength)
				elif component.connections[Direction.Top] is not None and component.connections[Direction.Bottom] is not None:
					image = QPixmap("assets/wire-left-right.png").scaled(self.blockSideLength, self.blockSideLength).transformed(QtGui.QTransform().rotate(90))
				elif component.connections[Direction.Top] is not None and component.connections[Direction.Right] is not None:
					image = QPixmap("assets/wire-top-right.png").scaled(self.blockSideLength, self.blockSideLength)
				elif component.connections[Direction.Top] is not None and component.connections[Direction.Left] is not None:
					image = QPixmap("assets/wire-top-right.png").scaled(self.blockSideLength, self.blockSideLength).transformed(QtGui.QTransform().rotate(270))
				elif component.connections[Direction.Bottom] is not None and component.connections[Direction.Right] is not None:
					image = QPixmap("assets/wire-top-right.png").scaled(self.blockSideLength, self.blockSideLength).transformed(QtGui.QTransform().rotate(90))
				elif component.connections[Direction.Bottom] is not None and component.connections[Direction.Left] is not None:
					image = QPixmap("assets/wire-top-right.png").scaled(self.blockSideLength, self.blockSideLength).transformed(QtGui.QTransform().rotate(180))
			elif component.numberOfConnections() == 3:
				image = QPixmap("assets/wire-left-top-right.png").scaled(self.blockSideLength, self.blockSideLength)
				if component.connections[Direction.Left] is None:
					image = image.transformed(QtGui.QTransform().rotate(90))
				elif component.connections[Direction.Top] is None:
					image = image.transformed(QtGui.QTransform().rotate(180))
				elif component.connections[Direction.Right] is None:
					image = image.transformed(QtGui.QTransform().rotate(270))
			return image
		else:
			imageName = "assets/wire-right.png"
		
			if component.type == ComponentType.Bulb:
				if component.isOn():
					imageName = "assets/bulb-on.png"
				else:
					imageName = "assets/bulb-off.png"
			elif component.type == ComponentType.Switch:
				if component.closed:
					imageName = "assets/switch-on.png"
				else:
					imageName = "assets/switch-off.png"
			elif component.type == ComponentType.Button:
				if component.closed:
					imageName = "assets/button-on.png"
				else:
					imageName = "assets/button-off.png"
			else:
				imageName = self.componentTypeToImageName(component.type)
			
			return QPixmap(imageName).scaled(self.blockSideLength, self.blockSideLength)

	def mouseCoordinatesToBlockIndex(self, x, y):
		if self.model is None or x < self.startingX or y < self.startingY or x > self.startingX + self.model.gridSize * self.blockSideLength or y > self.startingY + self.model.gridSize * self.blockSideLength:
			return (-1, -1)
		else:
			return (int((x - self.startingX) / self.blockSideLength), int((y - self.startingY) / self.blockSideLength))

	def blockIndexToCoordinate(self, x, y):
		return (self.startingX + self.blockSideLength * x, self.startingY + self.blockSideLength * y)

	def mousePressEvent(self, event):
		index = self.mouseCoordinatesToBlockIndex(event.x(), event.y())
		self.mousePress.emit(index, (event.x(), event.y()))

	def dragEnterEvent(self, event):
		event.acceptProposedAction()

	def dragMoveEvent(self, event):
		index = self.mouseCoordinatesToBlockIndex(event.pos().x(), event.pos().y())
		self.mouseMove.emit(index, (event.pos().x(), event.pos().y()))

	def dropEvent(self, event):
		event.acceptProposedAction()
		index = self.mouseCoordinatesToBlockIndex(event.pos().x(), event.pos().y())
		self.mouseRelease.emit(index, (event.pos().x(), event.pos().y()))
		
	def mouseMoveEvent(self, event):
		self.mousePosition = (event.x(), event.y())
		if self.dragging:
			self.render()
		index = self.mouseCoordinatesToBlockIndex(event.x(), event.y())
		self.mouseMove.emit(index, (event.pos().x(), event.pos().y()))

	def mouseReleaseEvent(self, event):
		index = self.mouseCoordinatesToBlockIndex(event.x(), event.y())
		self.mouseRelease.emit(index, (event.pos().x(), event.pos().y()))

	def resizeEvent(self, event):
		self.render()

	def render(self):
		if self.model is not None:
			self.scene.clear()
			self.renderCircuitDiagramGrid() 
			self.renderComponents() 

	def renderComponents(self):
		if self.model is not None:
			for component in self.model.components:
				pixmap = self.componentToImage(component)
				pixmapItem = self.scene.addPixmap(pixmap)
				offset = self.blockIndexToCoordinate(component.position[0],component.position[1])
				pixmapItem.setOffset(offset[0],offset[1])
				pixmapItem.setTransformationMode(Qt.SmoothTransformation)
		
				if component is self.selection:
					if self.dragging:
						renderPosition = (self.startingX + self.selection.position[0] * self.blockSideLength + self.mousePosition[0] - self.draggingStart[0], self.startingY + self.selection.position[1] * self.blockSideLength + self.mousePosition[1] - self.draggingStart[1])
						pixmapItem.setOffset(renderPosition[0], renderPosition[1])
					elif self.shouldShowSelection:
						pen = QPen(QBrush(QColor(0,0,255,100)), 2, Qt.DashLine)
						self.scene.addRect(self.startingX + component.position[0] * self.blockSideLength, self.startingY + component.position[1] * self.blockSideLength, self.blockSideLength, self.blockSideLength, pen)
				if component.type is ComponentType.Ammeter:
					font = QFont("Arial", self.blockSideLength/3.5)
					reading = self.scene.addText(str("%.2f" % component.current) + "A", font)
					offset = self.blockIndexToCoordinate(component.position[0],component.position[1])
					reading.setPos(offset[0]+self.blockSideLength/20,offset[1]+self.blockSideLength/4)
				elif component.type is ComponentType.Voltmeter:
					font = QFont("Arial", self.blockSideLength/3.5)
					reading = self.scene.addText(str("%.2f" % component.voltage) + "V", font)
					offset = self.blockIndexToCoordinate(component.position[0],component.position[1])
					reading.setPos(offset[0]+self.blockSideLength/20,offset[1]+self.blockSideLength/4)

	def renderCircuitDiagramGrid(self):
		pen = QPen(QBrush(QColor(200,200,200,255)), 1)
		pen2 = QPen(QBrush(QColor(100,100,100,255)), 3)
		width = self.width()
		height = self.height()
		self.blockSideLength = width / (self.model.gridSize + 2) if width < height else height / (self.model.gridSize + 2)

		# draw vertical lines
		currentX = width / 2
		self.startingX = currentX - (self.model.gridSize / 2) * self.blockSideLength
		while currentX - self.blockSideLength >= 0:
			currentX -= self.blockSideLength
		
		while currentX < width:
			self.scene.addLine(currentX, 1, currentX, height - 1, pen)
			
			currentX += self.blockSideLength

		# draw horizontal lines
		currentY = height / 2
		self.startingY = currentY - (self.model.gridSize / 2) * self.blockSideLength
		while currentY - self.blockSideLength >= 0:
			currentY -= self.blockSideLength
		while currentY < height:
			self.scene.addLine(1, currentY, width - 1, currentY, pen)
			currentY += self.blockSideLength

		self.scene.addLine(self.startingX, self.startingY, self.startingX + self.model.gridSize * self.blockSideLength, self.startingY, pen2)
		self.scene.addLine(self.startingX, self.startingY + self.model.gridSize * self.blockSideLength, self.startingX + self.model.gridSize * self.blockSideLength, self.startingY + 10 * self.blockSideLength, pen2)
		self.scene.addLine(self.startingX, self.startingY, self.startingX, self.startingY + self.model.gridSize * self.blockSideLength, pen2)
		self.scene.addLine(self.startingX + self.model.gridSize * self.blockSideLength, self.startingY, self.startingX + self.model.gridSize * self.blockSideLength, self.startingY + 10 * self.blockSideLength, pen2)
#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QPen, QColor, QBrush, QPixmap, QMouseEvent
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

		self.model = None

		self.setAcceptDrops(True)

		# setup & render circuit diagram grid
		self.scene = QGraphicsScene()
		self.setScene(self.scene)

		# drag and drop
		self.selection = None
		self.dragging = False
		self.mousePosition = None
		self.draggingStart = None

		self.render()

	def setModel(self, model):
		self.model = model
		self.model.modelChanged.connect(self.render)

	def setSelection(self, selection):
		self.selection = selection
		self.render()

	def setDragging(self, dragging):
		self.dragging = dragging
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
		imageName = "assets/icon.png"
		
		if component.type == ComponentType.Wire:
			if component.connections[Direction.Top] is not None:
				print("Top Connection")
				if component.connections[Direction.Right] is not None:
					imageName = "assets/wire-topright.png"
				elif component.connections[Direction.Bottom] is not None:
					imageName = "assets/wire-topbottom.png"
				elif component.connections[Direction.Left] is not None:
					imageName = "assets/wire-topleft.png"
				else:
					imageName = "assets/wire-top.png"
			elif component.connections[Direction.Right] is not None:
				if component.connections[Direction.Bottom] is not None:
					imageName = "assets/wire-bottomright.png"
				elif component.connections[Direction.Left] is not None:
					imageName = "assets/wire-leftright.png"
				else:
					imageName = "assets/wire-right.png"
			elif component.connections[Direction.Left] is not None:
				if component.connections[Direction.Bottom] is not None:
					imageName = "assets/wire-bottomleft.png"
				else:
					imageName = "assets/wire-left.png"
			else:
				imageName = "assets/wire-bottom.png"
		elif component.type == ComponentType.Bulb:
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
				pixmapItem.setTransformationMode(Qt.SmoothTransformation)
				pixmapItem.setOffset(self.startingX + self.blockSideLength * component.position[0], self.startingY + self.blockSideLength * component.position[1])
		
				if component is self.selection:
					if self.dragging:
						renderPosition = (self.startingX + self.selection.position[0] * self.blockSideLength + self.mousePosition[0] - self.draggingStart[0], self.startingY + self.selection.position[1] * self.blockSideLength + self.mousePosition[1] - self.draggingStart[1])
						pixmapItem.setOffset(renderPosition[0], renderPosition[1])
					else:
						pen = QPen(QBrush(QColor(0,0,255,100)), 2, Qt.DashLine)
						self.scene.addRect(self.startingX + component.position[0] * self.blockSideLength, self.startingY + component.position[1] * self.blockSideLength, self.blockSideLength, self.blockSideLength, pen)
				
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
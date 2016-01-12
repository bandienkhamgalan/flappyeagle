#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QPen, QColor, QBrush, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt, pyqtSignal
from models.components import ComponentType

class CircuitDiagramView(QGraphicsView):
	mousePress = pyqtSignal(tuple, name='mousePress')
	mouseMove = pyqtSignal(tuple, name='mouseMove')
	mouseRelease = pyqtSignal(tuple, name='mouseRelease')

	def __init__(self, parent=None):
		QGraphicsView.__init__(self, parent)
		self.model = None

		# setup & render circuit diagram grid
		self.scene = QGraphicsScene()
		self.setScene(self.scene)

		self.render()

	def mouseCoordinatesToBlockIndex(self, x, y):
		return (int((x - self.startingX) / self.blockSideLength), int((y - self.startingY) / self.blockSideLength))

	def mousePressEvent(self, event):
		self.mousePress.emit(self.mouseCoordinatesToBlockIndex(event.x(), event.y()))

	def mouseMoveEvent(self, event):
		self.mouseMove.emit(self.mouseCoordinatesToBlockIndex(event.x(), event.y()))

	def mouseReleaseEvent(self, event):
		self.mouseRelease.emit(self.mouseCoordinatesToBlockIndex(event.x(), event.y()))

	def resizeEvent(self, event):
		self.render()

	def render(self):
		self.scene.clear()
		self.renderCircuitDiagramGrid() 
		self.renderComponents() 

	def renderComponents(self):
		if self.model is not None:
			for component in self.model.components:
				if component.type is ComponentType.Battery:
					batteryImage = QPixmap("assets/battery.png", format="png").scaled(self.blockSideLength, self.blockSideLength)
					battery = self.scene.addPixmap(batteryImage)
					battery.setOffset(self.startingX + self.blockSideLength * component.position[0], self.startingY + self.blockSideLength * component.position[1])

	def renderCircuitDiagramGrid(self):
		pen = QPen(QBrush(QColor(200,200,200,255)), 1)
		pen2 = QPen(QBrush(QColor(100,100,100,255)), 3)
		width = self.width()
		height = self.height()
		self.blockSideLength = width / 12 if width < height else height / 12

		# draw vertical lines
		currentX = width / 2
		self.startingX = currentX - 5 * self.blockSideLength
		while currentX - self.blockSideLength >= 0:
			currentX -= self.blockSideLength
		
		while currentX < width:
			self.scene.addLine(currentX, 1, currentX, height - 1, pen)
			
			currentX += self.blockSideLength

		# draw horizontal lines
		currentY = height / 2
		self.startingY = currentY - 5 * self.blockSideLength
		while currentY - self.blockSideLength >= 0:
			currentY -= self.blockSideLength
		while currentY < height:
			self.scene.addLine(1, currentY, width - 1, currentY, pen)
			currentY += self.blockSideLength

		self.scene.addLine(self.startingX, self.startingY, self.startingX + 10 * self.blockSideLength, self.startingY, pen2)
		self.scene.addLine(self.startingX, self.startingY + 10 * self.blockSideLength, self.startingX + 10 * self.blockSideLength, self.startingY + 10 * self.blockSideLength, pen2)
		self.scene.addLine(self.startingX, self.startingY, self.startingX, self.startingY + 10 * self.blockSideLength, pen2)
		self.scene.addLine(self.startingX + 10 * self.blockSideLength, self.startingY, self.startingX + 10 * self.blockSideLength, self.startingY + 10 * self.blockSideLength, pen2)
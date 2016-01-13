#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtCore import Qt, pyqtSignal
from models.components import *

class DraggableComponentButton(QToolButton):
	mousePress = pyqtSignal(ComponentType, QMouseEvent, name='mousePress')
	mouseMove = pyqtSignal(ComponentType, QMouseEvent, name='mouseMove')
	mouseRelease = pyqtSignal(ComponentType, QMouseEvent, name='mouseRelease')

	def __init__(self, parent=None):
		QToolButton.__init__(self, parent)
		self.componentType = None

	#def mouseMoveEvent(self, event):
		#self.mouseMove.emit(self.componentType, event)

	#def mouseReleaseEvent(self, event):
		#self.mouseRelease.emit(self.componentType, event)
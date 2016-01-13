#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtCore import Qt, pyqtSignal
from models.components import *

class DraggableComponentButton(QToolButton):
	mousePress = pyqtSignal(ComponentType, QMouseEvent, name='mousePress')
	def __init__(self, parent=None):
		QToolButton.__init__(self, parent)
		self.componentType = None

	def mousePressEvent(self, event):
		self.checked = False
		self.mousePress.emit(self.componentType, event)
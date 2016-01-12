#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication
from views.MainView import MainView
from models.MainModel import MainModel
from controllers.MainController import MainController

class App(QApplication):
	def __init__(self, sysargv):
		super(App, self).__init__(sysargv)
		self.model = MainModel()
		self.controller = MainController(self.model)
		self.view = MainView(self.model, self.controller)
		self.view.show()

if __name__ == '__main__':
	app = App(sys.argv)
	sys.exit(app.exec_())
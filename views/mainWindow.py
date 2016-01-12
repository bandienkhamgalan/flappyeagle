# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'views/mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(788, 605)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mainWindow.sizePolicy().hasHeightForWidth())
        mainWindow.setSizePolicy(sizePolicy)
        mainWindow.setMinimumSize(QtCore.QSize(788, 605))
        mainWindow.setAutoFillBackground(False)
        mainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.build = QtWidgets.QRadioButton(self.centralwidget)
        self.build.setObjectName("build")
        self.horizontalLayout_4.addWidget(self.build)
        self.run = QtWidgets.QRadioButton(self.centralwidget)
        self.run.setObjectName("run")
        self.horizontalLayout_4.addWidget(self.run)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.toolbox = QtWidgets.QVBoxLayout()
        self.toolbox.setContentsMargins(-1, -1, 0, -1)
        self.toolbox.setObjectName("toolbox")
        self.toolboxComponents = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolboxComponents.sizePolicy().hasHeightForWidth())
        self.toolboxComponents.setSizePolicy(sizePolicy)
        self.toolboxComponents.setMinimumSize(QtCore.QSize(250, 0))
        self.toolboxComponents.setMaximumSize(QtCore.QSize(250, 400))
        self.toolboxComponents.setObjectName("toolboxComponents")
        self.gridLayoutWidget = QtWidgets.QWidget(self.toolboxComponents)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 20, 251, 231))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.toolboxComponentsGrid = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.toolboxComponentsGrid.setObjectName("toolboxComponentsGrid")
        self.newSwitch = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.newSwitch.setMinimumSize(QtCore.QSize(75, 60))
        self.newSwitch.setAutoFillBackground(False)
        self.newSwitch.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.newSwitch.setObjectName("newSwitch")
        self.toolboxComponentsGrid.addWidget(self.newSwitch, 2, 2, 1, 1)
        self.newVoltmeter = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.newVoltmeter.setMinimumSize(QtCore.QSize(75, 60))
        self.newVoltmeter.setAutoFillBackground(False)
        self.newVoltmeter.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.newVoltmeter.setObjectName("newVoltmeter")
        self.toolboxComponentsGrid.addWidget(self.newVoltmeter, 4, 1, 1, 1)
        self.newAmmeter = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.newAmmeter.setMinimumSize(QtCore.QSize(75, 60))
        self.newAmmeter.setAutoFillBackground(False)
        self.newAmmeter.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.newAmmeter.setObjectName("newAmmeter")
        self.toolboxComponentsGrid.addWidget(self.newAmmeter, 4, 0, 1, 1)
        self.newBattery = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.newBattery.setMinimumSize(QtCore.QSize(75, 60))
        self.newBattery.setAutoFillBackground(False)
        self.newBattery.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.newBattery.setObjectName("newBattery")
        self.toolboxComponentsGrid.addWidget(self.newBattery, 2, 0, 1, 1)
        self.newResistor = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.newResistor.setMinimumSize(QtCore.QSize(75, 60))
        self.newResistor.setAutoFillBackground(False)
        self.newResistor.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.newResistor.setObjectName("newResistor")
        self.toolboxComponentsGrid.addWidget(self.newResistor, 4, 2, 1, 1)
        self.newLED = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.newLED.setMinimumSize(QtCore.QSize(75, 60))
        self.newLED.setAutoFillBackground(False)
        self.newLED.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.newLED.setObjectName("newLED")
        self.toolboxComponentsGrid.addWidget(self.newLED, 2, 1, 1, 1)
        self.wireMode = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.wireMode.setMinimumSize(QtCore.QSize(75, 30))
        self.wireMode.setAutoFillBackground(False)
        self.wireMode.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.wireMode.setObjectName("wireMode")
        self.toolboxComponentsGrid.addWidget(self.wireMode, 0, 1, 1, 1)
        self.toolbox.addWidget(self.toolboxComponents)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.toolbox.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.toolbox)
        self.circuitDiagram = CircuitDiagramView(self.centralwidget)
        self.circuitDiagram.setMinimumSize(QtCore.QSize(500, 500))
        self.circuitDiagram.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.circuitDiagram.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.circuitDiagram.setRenderHints(QtGui.QPainter.HighQualityAntialiasing|QtGui.QPainter.SmoothPixmapTransform|QtGui.QPainter.TextAntialiasing)
        self.circuitDiagram.setResizeAnchor(QtWidgets.QGraphicsView.NoAnchor)
        self.circuitDiagram.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.circuitDiagram.setObjectName("circuitDiagram")
        self.horizontalLayout.addWidget(self.circuitDiagram)
        self.verticalLayout.addLayout(self.horizontalLayout)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 788, 22))
        self.menubar.setDefaultUp(False)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuWindow = QtWidgets.QMenu(self.menubar)
        self.menuWindow.setObjectName("menuWindow")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        mainWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(mainWindow)
        self.statusBar.setObjectName("statusBar")
        mainWindow.setStatusBar(self.statusBar)
        self.actionFile = QtWidgets.QAction(mainWindow)
        self.actionFile.setObjectName("actionFile")
        self.actionNew = QtWidgets.QAction(mainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(mainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(mainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionClose = QtWidgets.QAction(mainWindow)
        self.actionClose.setIconVisibleInMenu(True)
        self.actionClose.setObjectName("actionClose")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "FlappyEagle"))
        self.build.setText(_translate("mainWindow", "Build"))
        self.run.setText(_translate("mainWindow", "Run"))
        self.toolboxComponents.setTitle(_translate("mainWindow", "Components"))
        self.newSwitch.setText(_translate("mainWindow", "Switch"))
        self.newVoltmeter.setText(_translate("mainWindow", "Voltmeter"))
        self.newAmmeter.setText(_translate("mainWindow", "Ammeter"))
        self.newBattery.setText(_translate("mainWindow", "Battery"))
        self.newResistor.setText(_translate("mainWindow", "Resistor"))
        self.newLED.setText(_translate("mainWindow", "LED"))
        self.wireMode.setText(_translate("mainWindow", "Wire"))
        self.menuFile.setTitle(_translate("mainWindow", "File"))
        self.menuEdit.setTitle(_translate("mainWindow", "Edit"))
        self.menuWindow.setTitle(_translate("mainWindow", "Window"))
        self.menuHelp.setTitle(_translate("mainWindow", "Help"))
        self.actionFile.setText(_translate("mainWindow", "File"))
        self.actionNew.setText(_translate("mainWindow", "New"))
        self.actionOpen.setText(_translate("mainWindow", "Open"))
        self.actionSave.setText(_translate("mainWindow", "Save"))
        self.actionClose.setText(_translate("mainWindow", "Close"))

from views.CircuitDiagramView import CircuitDiagramView

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())


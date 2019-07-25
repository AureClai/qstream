#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 18:56:32 2019

@author: aurelienclairais
"""

from PyQt5 import uic, QtWidgets, QtCore

import os

dir_path = os.path.dirname(os.path.realpath(__file__))
FORM_CLASS, _ = uic.loadUiType(os.path.join(dir_path, 'generateXT_widget.ui'))

class generateXTWidget(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, currentFolder):
        super(generateXTWidget, self).__init__()
        # setup the ui from the Qt designer
        #uic.loadUi('ML_widget.ui', self)
        self.setupUi(self)
        self.currentFolder = currentFolder

        self.setWindowTitle("Générer les informations XT")
        self.setFixedSize(self.size())

        self.show()

        # setup the buttons
        self.ok_button.clicked.connect(self.processOK)
        self.DX_slider.valueChanged.connect(self.update_DX_LB)
        self.DT_slider.valueChanged.connect(self.update_DT_LB)
        self.getDir_PB.clicked.connect(self.getSimulationFile)

        #init the result
        self.val = {}

    @QtCore.pyqtSlot()
    def processOK(self):
        file = self.simulation_LE.text()
        name = self.name_LE.text()
        dx = self.DX_slider.value()
        dt = self.DT_slider.value()

        self.val = {'file' : file , 'name' : name, 'dx' : dx, 'dt' : dt}

        self.accept()
        return self.val

    def update_DX_LB(self):
        self.DX_LB.setText(str(self.DX_slider.value()))
        return

    def update_DT_LB(self):
        self.DT_LB.setText(str(self.DT_slider.value()))
        return

    def getSimulationFile(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Sélectionner un fichier de résultat", self.currentFolder, "Fichier Numpy (*.npy)")
        self.simulation_LE.setText(file)
        self.update()
#
if __name__ == '__main__':
    d = generateXTWidget()

#res = ''
#dial = generateXTWidget()
#dial.setAttribute(QtCore.Qt.WA_DeleteOnClose)
#if dial.exec_() == QtWidgets.QDialog.Accepted:
#    res = dial.val
#print(res)

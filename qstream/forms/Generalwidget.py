#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 18:56:32 2019

@author: aurelienclairais
"""

from PyQt5 import uic, QtWidgets, QtCore
import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
FORM_CLASS, _ = uic.loadUiType(os.path.join(dir_path, 'General_widget.ui'))

class GeneralWidget(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, values, parent = None):
        super(GeneralWidget, self).__init__()
        # setup the ui from the Qt designer
        self.setupUi(self)

        self.setWindowTitle("Change General parameters")

        # setup the text in LE
        self.start_LE.setText(str(values[1]))
        self.end_LE.setText(str(values[2]))
        self.step_LE.setText(str(values[3]))
        self.upcapacity_RB.setChecked(bool(int(values[4])))
        self.streamDir_LE.setText(values[5])

        # display the window
        self.show()

        # setup the buttons
        self.ok_button.clicked.connect(self.processOK)
        self.getDir_PB.clicked.connect(self.getStreamDir)

        #init the result
        self.res = ''

    @QtCore.pyqtSlot()
    def processOK(self):
        try:
            start = int(self.start_LE.text())
            end = int(self.end_LE.text())
            step = int(self.step_LE.text())
            upcap = self.upcapacity_RB.isChecked()
            dir = self.streamDir_LE.text()
        except:
            self.message_LE.setText("Erreur de syntaxe dans les cases à remplir")
            self.update()
            return

        self.val = {"SimulationStart" : start , "SimulationEnd" : end, "TimeStep" : step, "ActiveUpstreamCapacity" : upcap, "StreamDirectory" : dir}
        self.accept()

    def getStreamDir(self):
        streamFolder = str(QtWidgets.QFileDialog.getExistingDirectory(None, "Select Stream Directory"))
        if streamFolder != '':
            self.streamDir_LE.setText(streamFolder)
        self.update()

if __name__ == '__main__':
    d = GeneralWidget()

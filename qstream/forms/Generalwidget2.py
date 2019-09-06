#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 18:56:32 2019

@author: aurelienclairais
"""

from PyQt5 import uic, QtWidgets, QtCore
#import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
FORM_CLASS, _ = uic.loadUiType(os.path.join(dir_path, 'General_widget2.ui'))

def convertToSeconds(qtime):
    return qtime.hour() * 3600 + qtime.minute() * 60 + qtime.second()

def convertToQTime(seconds):
    hours = int(seconds/3600)
    minutes = int((seconds % 3600)/60)
    secs = int(seconds % 60)
    return QtCore.QTime(hours, minutes, secs)

class GeneralWidget2(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, values, parent = None):
        super(GeneralWidget2, self).__init__()
        # setup the ui from the Qt designer
        self.setupUi(self)

        self.setWindowTitle("Change General parameters")

        # setup the text in LE
        self.beg_TE.setTime(convertToQTime(values[1]))
        self.end_TE.setTime(convertToQTime(values[2]))
        self.per_TE.setTime(convertToQTime(values[3]))
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
            start = convertToSeconds(self.beg_TE.time())
            end = convertToSeconds(self.end_TE.time())
            step = convertToSeconds(self.per_TE.time())
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
    d = GeneralWidget2([0, 25000,26580, 900,0, ''])
    if d.exec_ () == QtWidgets.QDialog.Accepted:
            res = d.val
    print(res)

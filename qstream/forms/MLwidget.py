#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 18:56:32 2019

@author: aurelienclairais
"""

from PyQt5 import uic, QtWidgets, QtCore
import json
import os

#import os
dir_path = os.path.dirname(os.path.realpath(__file__))
FORM_CLASS, _ = uic.loadUiType(os.path.join(dir_path, 'ML_widget.ui'))

class MLWidget(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, linksFid, selectedFid, classDict, previousInfos = None,parent = None ):
        super(MLWidget, self).__init__()
        # setup the ui from the Qt designer
        #uic.loadUi('ML_widget.ui', self)
        self.setupUi(self)

        self.setWindowTitle("Edition de voie réservée")

        self.classDict = classDict
        self.linksFid = linksFid

        for id in list(classDict.keys()):
            self.class_CB.addItem(str(id) + ' - ' + classDict[id])

        # setup the values in the lineEdits
        if previousInfos==None:
            self.selectedFid = selectedFid
        else:
            self.selectedFid = [str(fid) for fid in previousInfos['Links']]
            self.times_LE.setText(','.join([str(time) for time in previousInfos['Times']]))
            self.class_CB.setCurrentIndex(previousInfos['Class'])
            if 'Capacity' in list(previousInfos.keys()):
                self.capacity_LE.setText(str(previousInfos['Capacity']))
                self.keep_check.setChecked(True)
                self.check_callback()
        self.links_LE.setText(','.join(self.selectedFid))

        self.show()

        # setup the buttons
        self.keep_check.toggled.connect(self.check_callback)
        self.ok_button.clicked.connect(self.processOK)

        #init the result
        self.res = ''

    def check_callback(self):
        if self.keep_check.isChecked():
            self.capa_label.setEnabled(True)
            self.capacity_LE.setEnabled(True)
        else:
            self.capa_label.setEnabled(False)
            self.capacity_LE.setEnabled(False)
            self.capacity_LE.setText('')

    @QtCore.pyqtSlot()
    def processOK(self):
        try:
            #theClass = int(self.class_LE.text())
            theClass = int(self.class_CB.currentText().split(' - ')[0])
            times = [int(value) for value in self.times_LE.text().split(',')]
            links = [int(value) for value in self.links_LE.text().split(',')]
        except:
            self.message_LE.setText("Erreur de syntaxe dans Liens ou Temps ou cases vides")
            self.update()
            return

        try:
            capacity = float(self.capacity_LE.text())
        except:
            capacity = -1

        #test if the links in LEs are in the Links layer
        if all(x in self.linksFid for x in links):
            res = {"Class" : theClass , "Times" : times, "Links" : links}
            if capacity >= 0:
                res.update({'Capacity' : capacity})
            self.val = json.dumps(res)
            self.accept()
        else:
            self.message_LE.setText("Lien(s) stipulé(s) introuvable(s)")
            self.update()
            return

if __name__ == '__main__':
    d = MLWidget()

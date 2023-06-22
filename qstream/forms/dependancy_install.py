#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 18:56:32 2019

@author: aurelienclairais
"""

from PyQt5 import uic, QtWidgets, QtCore
import sys
import os
import requests
import subprocess

dir_path = os.path.dirname(os.path.realpath(__file__))
FORM_CLASS, _ = uic.loadUiType(os.path.join(dir_path, 'dependancy_install.ui'))

class DependancyInstall(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, modules, parent = None):
        super(DependancyInstall, self).__init__()
        # setup the ui from the Qt designer
        self.setupUi(self)

        model = QtCore.QStringListModel()
        model.setStringList(modules)
        self.module_list.setModel(model)

        self.modules = modules

        self.installer_PB.clicked.connect(self.install_all)
        self.OK_PB.clicked.connect(self.OK_callback)
        self.Annuler_PB.clicked.connect(self.annuler_callback)

        self.init_QProcess()
    
    def install_all(self):
        self.installer_PB.setEnabled(False)
        self.module_count = 0
        self.install_module(self.modules[self.module_count])

    def install_module(self,module):
        if module == 'stream':
            self.install_stream()
        else:
            self.p.start("pip", ["install", module])
    
    def message(self, s):
        self.message_container.appendPlainText(s)

    def init_QProcess(self):
        self.p = QtCore.QProcess()
        #self.p.stateChanged.connect(self.handle_state)
        self.p.finished.connect(self.handle_process_finished)
        self.p.readyReadStandardOutput.connect(self.handle_stdout)
        self.p.readyReadStandardError.connect(self.handle_stderr)

    def install_stream(self):
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Sauvegarder le zip de Stream", "", "Archives ZIP (*.zip)")
        if fileName:
            # Download the zip file
            response = requests.get('https://github.com/AureClai/stream-python/archive/refs/tags/v.3.2.2.zip')
            with open(fileName, 'wb') as file:
                file.write(response.content)
            self.p.start("pip", ["install", fileName])

    def handle_stdout(self):
        data = QtCore.QByteArray()
        while self.p.canReadLine():
            data += self.p.readLine()
        stdout = data.data().decode()
        self.message(stdout)

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)

    def handle_process_finished(self):
        self.module_count += 1
        if self.module_count == len(self.modules):
            self.message("Installation terminée")
            self.OK_PB.setEnabled(True)
        else:
            self.install_module(self.modules[self.module_count])
    
    def OK_callback(self):
        # Accept and close the dialog
        self.accept()

    # ChatGPT: Fill the function
    def annuler_callback(self):
        # Cancel and close the dialog
        self.reject()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    d = DependancyInstall(['pyexcel_ods', 'stream'])

      # Run the dialog and check the result
    result = d.exec()
    if result:
        print("Dialog accepted")
    else:
        print("Dialog canceled")


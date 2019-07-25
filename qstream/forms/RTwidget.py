# -*- coding: utf-8 -*-
"""
Created on Thu May 16 08:16:47 2019

@author: aurelien.clairais
"""
import os

from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import (QIntValidator as QIntValidator)

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

import numpy as np

from .mplwidget import MplWidget


dir_path = os.path.dirname(os.path.realpath(__file__))
FORM_CLASS, _ = uic.loadUiType(os.path.join(dir_path, 'RT_widget.ui'))
matplotlib.rcParams.update({'font.size': 6})

class RTWidget(QDialog, FORM_CLASS):
    
    def __init__(self, rtdict):
        super(RTWidget, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Gérer les types de routes")
        self.setFixedSize(self.size())
        self.rtdict = rtdict
        self.update_CB()
        self.MplWidget = MplWidget(self)
        #self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))
        
        #..
        #Update signal
        self.rt_CB.currentIndexChanged.connect(self.update_RT)    
        self.remove_PB.clicked.connect(self.removeRT)
        self.add_PB.clicked.connect(self.addRT)
        self.modif_PB.clicked.connect(self.modifPBcallback)
        self.u_LE.textEdited.connect(self.uChanged)
        self.kx_LE.textEdited.connect(self.kxChanged)
        self.C_LE.textEdited.connect(self.CChanged)
        self.validate_PB.clicked.connect(self.validateAll)
        
        #...
        self.onlyInt = QIntValidator()
        self.u_LE.setValidator(self.onlyInt)
        self.C_LE.setValidator(self.onlyInt)
        self.kx_LE.setValidator(self.onlyInt)
        
        #...
        self.update_les()
        self.update_graph()
    
    def update_graph(self):
        infos = self.get_infos()
        u = infos[1]
        kx = infos[3]
        C = infos[2]
        if not any([elem==0 for elem in [u, kx, C]]):           
            self.MplWidget.canvas.axes.clear()
            self.MplWidget.canvas.axes.plot([0, C/u], [0, C], color = 'lime')
            self.MplWidget.canvas.axes.plot([C/u, kx], [C, 0], color = 'red')
            self.MplWidget.canvas.axes.set_ylim([0,1.1*C])
            self.MplWidget.canvas.axes.grid(True)
            self.MplWidget.canvas.draw()
        else:
            self.MplWidget.canvas.axes.clear()
            self.MplWidget.canvas.draw()
        
    def update_les(self):
        if len(self.rtdict)!=0:
            currIndex = int(self.rt_CB.currentText().split(' - ')[0])
            infos = self.rtdict[currIndex]
            u = infos['u']
            kx = infos['kx']
            C = infos['C']
            name = infos['name']
            #put param in lineEdit
            self.u_LE.setText(str(u))
            self.C_LE.setText(str(C))
            self.kx_LE.setText(str(kx))
            self.name_LE.setText(str(name))
        else:
            #put param in lineEdit
            self.u_LE.setText('')
            self.C_LE.setText('')
            self.kx_LE.setText('')
            self.name_LE.setText('')
            
    def switchRT(self):
        return
    
    def addRT(self):
        infos = self.get_infos()
        name = infos[0]
        if name in [self.rtdict[key]['name'] for key in list(self.rtdict.keys())]:
            name = name + '_copie'
        identifiant = max(list(self.rtdict.keys())) + 1
        self.rtdict.update({identifiant : {'name' : name, 'u' : infos[1], 'C' : infos[2], 'kx' : infos[3]}})
        self.update_CB()
        return
    
    def removeRT(self):
        currIndex = int(self.rt_CB.currentText().split(' - ')[0])
        del self.rtdict[currIndex]
        self.rt_CB.removeItem(self.rt_CB.currentIndex())
        return
    
    def update_CB(self):
        self.rt_CB.clear()
        #put the info in the combo box
        for id in list(self.rtdict.keys()):
            self.rt_CB.addItem(str(id) + ' - ' + self.rtdict[id]['name'])
            
    def update_RT(self):
        if self.rt_CB.currentIndex() != -1:
            self.update_les()
            self.update_graph()
            
        
    def get_infos(self):
        try:
            u = int(self.u_LE.text())
        except:
            u = 0
        try:
            C = int(self.C_LE.text())
        except:
            C = 0
        try:
            kx = int(self.kx_LE.text())
        except:
            kx = 0
        name = self.name_LE.text()
        
        return [name, u , C, kx]
    
    def modifPBcallback(self):
        infos = self.get_infos()
        identifiant = int(self.rt_CB.currentText().split(' - ')[0])
        name = infos[0]
        listID = list(self.rtdict.keys())
        listID.remove(identifiant)
        if name in [self.rtdict[key]['name'] for key in listID]:
            name = name + '_copie'
        self.rtdict.update({identifiant : {'name' : name, 'u' : infos[1], 'C' : infos[2], 'kx' : infos[3]}})
        self.update_CB()
        return
    
    def uChanged(self):
        self.update_graph()
        return
    
    def kxChanged(self):
        self.update_graph()
        return
    
    def CChanged(self):
        self.update_graph()
        return
    
    def validateAll(self):
        self.modifPBcallback()
        self.val = self.rtdict
        self.accept()
        return
    
        
#
if __name__ == '__main__':
    rtdict = {1 : {'name' : 'Autoroute', 'u' : 130, 'C' : 2200, 'kx' : 140}, 2: {'name' : 'Bretelle', 'u' : 90, 'C' : 1800, 'kx' : 140}}
    d = RTWidget(rtdict)
        
#res = ''
#rtdict = {1 : {'name' : 'Autoroute', 'u' : 130, 'C' : 2200, 'kx' : 140}, 2: {'name' : 'Bretelle', 'u' : 90, 'C' : 1800, 'kx' : 140}}
#dial = RTWidget(rtdict)
#dial.setAttribute(QtCore.Qt.WA_DeleteOnClose)
#if dial.exec_() == QDialog.Accepted:
#    res = dial.val
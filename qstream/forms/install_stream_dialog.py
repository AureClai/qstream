from PyQt5 import uic, QtWidgets, QtCore
#import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
FORM_CLASS, _ = uic.loadUiType(os.path.join(dir_path, 'install_stream_dialog.ui'))

class InstallStreamDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        super(InstallStreamDialog, self).__init__()
        # setup the ui from the Qt designer
        self.setupUi(self)
        self.val = None
    
        self.setWindowTitle("Change General parameters")

        self.parcourir_PB.clicked.connect(self.selectFolder)


    def selectFolder(self):
        file_dialog = QtWidgets.QFileDialog()
        selected_directory = file_dialog.getExistingDirectoryUrl(parent = self, caption="Sélectionner un dossier de téléchargement")

        if selected_directory:
            self.folder_LE.setText(selected_directory.toLocalFile())
            self.val = selected_directory.toLocalFile()
import os

from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal

FORM_CLASS_DS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'dataset_form.ui'))

FORM_CLASS_INF, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'information.ui'))

class DatasetForm(QtWidgets.QDialog, FORM_CLASS_DS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(DatasetForm, self).__init__(parent)
        self.setupUi(self)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
        
class InformationForm(QtWidgets.QDialog,FORM_CLASS_INF):
    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(InformationForm, self).__init__(parent)
        self.setupUi(self)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
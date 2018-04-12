#!/usr/bin/env python

import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMessageBox,QLabel
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage, QRegExpValidator, QDoubleValidator, QIntValidator, QMovie, QColor
from Algorithme import *



#listener of lauch button pressed
def SimulationListener():
    Qtot = ui.Qtot.text()
    eam = ui.eam.text()
    if(Qtot =="" or eam ==""or ui.Qt1.text() ==""or ui.Qt2.text() ==""or ui.Qt3.text() ==""or ui.Qt4.text() ==""or ui.Qt5.text() ==""):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Veuillez bien remplir tous les champs")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

        return 0;
    eam=eam.replace(',', '.')
    Qlim = [180,int(ui.Qt1.text()),int(ui.Qt2.text()),int(ui.Qt3.text()),int(ui.Qt4.text()),int(ui.Qt5.text())]
    
    if(ui.Discretisation2.isChecked()):
        turbine, puissance = runSimulation(int(Qtot), float(eam), Qlim, True)
    else:
        turbine, puissance = runSimulation(int(Qtot), float(eam), Qlim, False)
    ui.Q1.setText(str(turbine[1]))
    ui.Q2.setText(str(turbine[2]))
    ui.Q3.setText(str(turbine[3]))
    ui.Q4.setText(str(turbine[4]))
    ui.Q5.setText(str(turbine[5]))
    
    ui.P1.setText(str(round(costFunction(turbine[1],1,int(Qtot),float(eam)),3)))
    ui.P2.setText(str(round(costFunction(turbine[2],2,int(Qtot),float(eam)),3)))
    ui.P3.setText(str(round(costFunction(turbine[3],3,int(Qtot),float(eam)),3)))
    ui.P4.setText(str(round(costFunction(turbine[4],4,int(Qtot),float(eam)),3)))
    ui.P5.setText(str(round(costFunction(turbine[5],5,int(Qtot),float(eam)),3)))
    
    ui.Qvanne.setText(str(turbine[0]))
    ui.puissance.setText(str(round(puissance,3)))

#listener of all turbine flow checkboxes
def state_changed(int):
    if not ui.T1.isChecked():
        ui.Qt1.setText("0")
        ui.Qt1.setDisabled(True)
    else:
        if ui.Qt1.text()=="0":
            ui.Qt1.setText(str(180))
        ui.Qt1.setDisabled(False)
    if not ui.T2.isChecked():
        ui.Qt2.setText("0")
        ui.Qt2.setDisabled(True)
    else:
        if ui.Qt2.text()=="0":
            ui.Qt2.setText(str(180))
        ui.Qt2.setDisabled(False)
    if not ui.T3.isChecked():
        ui.Qt3.setText("0")
        ui.Qt3.setDisabled(True)
    else:
        if ui.Qt3.text()=="0":
            ui.Qt3.setText(str(180))
        ui.Qt3.setDisabled(False)
    if not ui.T4.isChecked():
        ui.Qt4.setText("0")
        ui.Qt4.setDisabled(True)
    else:
        if ui.Qt4.text()=="0":
            ui.Qt4.setText(str(180))
        ui.Qt4.setDisabled(False)
    if not ui.T5.isChecked():
        ui.Qt5.setText("0")
        ui.Qt5.setDisabled(True)
    else:
        if ui.Qt5.text()=="0":
            ui.Qt5.setText(str(180))
        ui.Qt5.setDisabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = loadUi('main.ui')
    validatorDouble =  QDoubleValidator()
    validatorInt =  QIntValidator()
    ui.Qt1.setValidator(validatorInt)
    ui.Qt2.setValidator(validatorInt)
    ui.Qt3.setValidator(validatorInt)
    ui.Qt4.setValidator(validatorInt)
    ui.Qt5.setValidator(validatorInt)
    ui.Qtot.setValidator(validatorInt)
    ui.eam.setValidator(validatorDouble)
    ui.Qt1.setText(str(180))
    ui.Qt2.setText(str(180))
    ui.Qt3.setText(str(180))
    ui.Qt4.setText(str(180))
    ui.Qt5.setText(str(180))
    ui.T1.stateChanged.connect(state_changed)
    ui.T2.stateChanged.connect(state_changed)
    ui.T3.stateChanged.connect(state_changed)
    ui.T4.stateChanged.connect(state_changed)
    ui.T5.stateChanged.connect(state_changed)
    ui.run.clicked.connect(SimulationListener)
    pixmap = QPixmap('Centrale.jpg')
    ui.image.setPixmap(pixmap)
    ui.show()

sys.exit(app.exec_())



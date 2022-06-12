import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow,
)
import numpy as np
import pandas as pd
from main_window_ui import Ui_MainWindow
from random import randint
from calculo_model import globalCalculate

from table_configuration import TableModel


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.agregarOpcionesComboBox()
        self.configurarTablaVariantes()

        # self.connectSignalsSlots()

    def configurarTablaVariantes(self):
        data = pd.DataFrame([
            ['Efecto 1', 0.12, 0.43, 0.65, 0.98, 0.5],
            ['Efecto 2', 0.12, 0.43, 0.65, 0.98, 0.5],
        ], columns=['',
                    'Flujos de liquidos (kg/h)',
                    'Flujos de vapor (kg/h)',
                    'Fracciones masicas de solutos en los líquidos (m/n)',
                    'U (kW/°C*m^2)',
                    'Temperatura saturación (c)'
                    ]
        )
        model_tabla_variantes = TableModel(data)
        self.table_variantes.setModel(model_tabla_variantes)
        self.calcular_button.clicked.connect(self.calculate)

    def calcularPabsres(self):
        eleccion = self.selector_presion.currentText()
        print(eleccion)
        Pman = round(float(self.input_presion_efecto.text()))
        if eleccion == 'Manométrica':
            return 101.325 + Pman
        else:
            return round(Pman, 2)

    def calculate(self):
        num_efectos = int(self.input_numero_efectos.text())
        Tst = float(self.input_temperatura_vapor_saturado.text())
        Pabsres = self.calcularPabsres()
        L = np.zeros((num_efectos+1, 5))
        L[0, 0] = float(self.input_flujo_alimentacion.text())
        L[0, 1] = float(self.input_fraccion_masica_alimentacion.text())
        L[num_efectos, 1] = float(self.input_fraccion_masica_producto.text())
        L[0, 2] = float(self.input_temperatura_alimentacion.text())
        V = np.zeros((num_efectos+1, 5))
        inputs = [
            L,
            num_efectos,
            Tst,
            V,
            [],
            Pabsres
        ]
        print(inputs)
        globalCalculate(inputs)

    def agregarOpcionesComboBox(self):
        self.selector_presion.addItem('Manométrica', 'm')
        self.selector_presion.addItem('Absoluta', 'a')

    def connectSignalsSlots(self):
        pass
        # self.pushButton.clicked.connect(self.changeDisplay)

    def changeDisplay(self):
        pass
        self.lcdNumber.display(randint(0, 50))

    def findAndReplace(self):
        pass
        # dialog = FindReplaceDialog(self)
        # dialog.exec()


# class FindReplaceDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         loadUi("ui/find_replace.ui", self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('sPyQt5 App')
window.setGeometry(200, 200, 280, 100)
window.move(60, 15)
helloMsg = QLabel('<h1> Hola! culo y tetas</h1>', parent=window)
helloMsg.move(60, 15)

window.show()


sys.exit(app.exec_())
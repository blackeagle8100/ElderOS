import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPalette, QColor

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)
        

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.showFullScreen()
        
        self.setWindowTitle("TV and music")
        lv = QVBoxLayout()
        lh = QHBoxLayout()
        
        lofoto = QGridLayout()

               

        lofoto.addWidget(Color('red'), 0, 0)
        lofoto.addWidget(Color('red'), 0, 1)
        lofoto.addWidget(Color('red'), 0, 2)
        lofoto.addWidget(Color('green'), 1, 0)
        lofoto.addWidget(Color('green'), 1, 1)
        lofoto.addWidget(Color('green'), 1, 2)
        lofoto.addWidget(Color('purple'), 2, 0)
        lofoto.addWidget(Color('purple'), 2, 1)
        lofoto.addWidget(Color('purple'), 2, 2)

        lh.addWidget(Color('blue'))
        lh.addLayout(lofoto) 
        lh.addWidget(Color('blue'))
        

        lv.addWidget(Color('pink'))
        lv.addLayout(lh)

        widget = QWidget()
        widget.setLayout(lv)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
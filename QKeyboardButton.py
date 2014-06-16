
from PyQt4.QtGui import QPushButton 
from PyQt4.QtCore import Qt



class QKeyboardButton(QPushButton):
    
    def __init__ (self, parent):
        QPushButton.__init__(self, parent)
        self.setFocusPolicy(Qt.NoFocus)
        
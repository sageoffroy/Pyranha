from QKeyboardButton import QKeyboardButton
from PyQt4.QtTest import QTest

class QCharButton(QKeyboardButton):
    
    char = ''
    
    def __init__ (self, parent):
        QKeyboardButton.__init__(self,parent)
    
    
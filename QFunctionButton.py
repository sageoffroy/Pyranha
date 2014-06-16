from QKeyboardButton import QKeyboardButton
from PyQt4.QtTest import QTest

class QFunctionButton(QKeyboardButton):
    
    function = ''
    
    def __init__ (self, parent):
        QKeyboardButton.__init__(self,parent)
from QKeyboardButton import QKeyboardButton
from PyQt4.QtTest import QTest

class QModeButton(QKeyboardButton):
    
    enabled = False
    
    def __init__ (self, parent,x,y,objectName,keySize =1):
        QKeyboardButton.__init__(self,parent,x,y,objectName,keySize)
        self.setStyleSheet('QPushButton {color: gray}')
            
    def enable(self):
        self.enabled = True
        self.setStyleSheet('QPushButton {color: green}')
        
    def disable(self):
        self.activated = False
        self.setStyleSheet('QPushButton {color: gray}')
    
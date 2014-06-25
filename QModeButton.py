from QKeyboardButton import QKeyboardButton

class QModeButton(QKeyboardButton):
    
    mode = ""
    
    def __init__ (self, parent, mode):
        QKeyboardButton.__init__(self,parent)
        self.mode = mode
            

from QKeyboardButton import QKeyboardButton

class QModeButton(QKeyboardButton):
    
    mode = ""
    
    def __init__ (self, parent):
        QKeyboardButton.__init__(self,parent)
        
            

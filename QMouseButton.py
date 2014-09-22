from QKeyboardButton import QKeyboardButton

class QMouseButton(QKeyboardButton):
    
    action = ""
    
    def __init__ (self, parent):
        QKeyboardButton.__init__(self,parent)
        
            

from QKeyboardButton import QKeyboardButton

class QMoveButton(QKeyboardButton):
    
    move_function = ""
    
    def __init__ (self, parent, move_function):
        QKeyboardButton.__init__(self,parent)
        self.move_function = move_function
            

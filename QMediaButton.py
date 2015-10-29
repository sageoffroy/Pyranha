from QKeyboardButton import QKeyboardButton

class QMediaButton(QKeyboardButton):
    
    media = ''
    
    def __init__ (self, parent):
        QKeyboardButton.__init__(self,parent)
from QKeyboardButton import QKeyboardButton

class QWebButton(QKeyboardButton):
    
    web_function = ""
    
    def __init__ (self, parent, web_function):
        QKeyboardButton.__init__(self,parent)
        self.web_function = web_function
            

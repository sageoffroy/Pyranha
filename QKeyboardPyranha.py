# -*- encoding: utf-8 -*-
from operator import itemgetter
from PyQt4.QtGui import QWidget, QApplication, QCursor
from keyboardMousePyranha import Ui_Form
from PyQt4.QtCore import Qt, QTimer, QPoint
from PyQt4.QtTest import QTest

#En los caso que se use python 3 QString no existe
try:  
    from PyQt4.QtCore import QString  
except ImportError:  
    QString = str  

# Formato Utf8
try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)
    

class QKeyboardPyranha(QWidget):
    
    
    predectiveLineEditArray = []
    charModeArray = []
    funButtonArray = []
    charButtonArray = []
    
    charArrow1 = []
    charArrow2 = []
    charArrow3 = []
    
    mouseArrow1 = []
    mouseArrow2 = []
    mouseArrow3 = []
        
    mouseButtonArray = []
    moveButtonArray = []
    numButtonArray = []
    webButtonArray = []
    modeButtonArray = []
    
    buttonArray = []
    
    charDict = {'a':26,'b':11,'c':16,'d':19,'e':27,'f':6,'g':8,'h':10,'i':21,'j':7,'k':2,'l':20,'m':15,'n':23,'ñ':4,'o':25,'p':14,'q':13,'r':22,'s':24,'t':17,'u':18,'v':9,'w':1,'x':3,'y':12,'z':5}
    
    functionDict ={'May':5, 'Ent':8, 'Sup':7, 'Bsp':6, 'Tab':5, 'Esc':4, 'Ins':3, 'Ctl':2, 'Alt':1}
    
    numDict = {'0':1,'1':2,'2':3,'3':4,'4':5,'5':10,'6':6,'7':8,'8':9,'9':15}
    
    operNumDict = {'+':1,'-':2,'/':3,'*':4}
    
    def __init__(self, browser):
        QWidget.__init__(self)
        print("se creo keyboard")
        self.setMinimumSize(860,250)
        
        #Referencia al navegador para obtener el foco
        self.browser = browser
        #Cargando interfaz y configurando botones
        self.keyboardUI = Ui_Form()
        self.keyboardUI.setupUi(self)
        self.setArray()
        self.setButtonFocusPolicy()
        #Comenzamos con la funcion mayuscula desactivada
        self.uppercase = False
        #Configuramos las teclas
        self.configCharKeys()
        self.configFunctionKeys()
        self.configNumKeys()
        self.configModeKeys()
        self.configMouseKeys()
        #Configuramos los modos
        self.configCharMode()
        self.configMouseMode()
        
        self.setKeyStyleSheet()
        
        self.mode = "char1"
        self.activeClick = False
        self.currentKey = None
        #self.setDefaultStyle(self.arrow3)
        self.setArrayStyle(self.predectiveLineEditArray)
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(2000)
        
        self.mouseTimer = QTimer()
        self.mouseTimer.timeout.connect(self.mouseTick)
        
        self.mouseStop = False
        
    def setKeyStyleSheet(self):
        self.setDefaultStyle(self.predectiveLineEditArray)
        self.setDefaultStyle(self.mouseButtonArray)
        self.setDefaultStyle(self.moveButtonArray)
        self.setDefaultStyle(self.webButtonArray)
        self.setDefaultStyle(self.numButtonArray)
        self.setDefaultStyle(self.modeButtonArray)
        self.setDefaultStyle(self.funButtonArray)
        self.setDefaultStyle(self.charButtonArray)
    
        
    def click(self):
        if (self.activeClick):
            print ("Segundo Click")
            self.activeClick = False
            print(self.currentKey)
            self.currentKey.clicked.emit(True)
            self.timer.timeout.disconnect(self.tick2)
            self.timer.timeout.connect(self.tick)    
        else:
            print ("Primer Click")
            self.activeClick = True
            self.timer.timeout.disconnect(self.tick)
            self.timer.timeout.connect(self.tick2)
        self.i = 0
    
    def tick(self):
        print("tick")
        self.setDefaultStyle(self.array)
        
        if(self.mode == "char1"):
            print("Char 2")
            self.mode = "char2"
            self.setArrayStyle(self.modeButtonArray)
        elif (self.mode == "char2"):
            print("Char 3")
            self.setArrayStyle(self.funButtonArray)
            self.mode = "char3"
        elif (self.mode == "char3"):
            print("Char 4_1")
            self.mode = "char4_1"
            self.setArrayStyle(self.charArrow1)
        elif (self.mode == "char4_1"):
            print("Char 4_2")
            self.mode = "char4_2"
            self.setArrayStyle(self.charArrow2)
        elif (self.mode == "char4_2"):
            print("Char 4_3")
            self.mode = "char4_3"
            self.setArrayStyle(self.charArrow3)
        elif (self.mode == "char4_3"):
            print("Char 1")
            self.mode = "char1"
            self.setArrayStyle(self.predectiveLineEditArray)
        elif (self.mode == "mouse1"):
            self.mouseStop = False
            print("mouse2")
            self.mode = "mouse2"
            self.setArrayStyle(self.mouseArrow2)
        elif (self.mode == "mouse2"):
            print("mouse3")
            self.mode = "mouse3"
            self.setArrayStyle(self.mouseArrow3)
        elif (self.mode == "mouse3"):
            print("mouse1")
            self.mode = "mouse1"
            self.setArrayStyle(self.mouseArrow1)
        elif (self.mode == "mouseMove"):
            if (self.mouseStop):
                self.mode = "mouse1"
                self.setArrayStyle(self.mouseArrow1)
            self.timer.stop()
            self.setKeyStyle(self.keyboardUI.mouseButton_c)
            self.click()
            
            
    def tick2(self):
        print("tick 2")
        if (self.i > len(self.array)-1):
            
            self.timer.timeout.disconnect(self.tick2)
            self.i = 0
            self.timer.timeout.connect(self.tick)
            self.mode = "char4_3"
            self.setDefaultStyle(self.array)
        
        else:
            self.setArrayStyle(self.array)
            self.currentKey = self.array[self.i] 
            self.array[self.i].setStyleSheet('''
                                color: #44d51C;
                                border-radius: 8px;
                                border-style: outset; 
                                border-width: 1px;
                                border-color:blue;
                                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #888888, stop: 0.1 #222222);    
                                ''')
            self.i+=1
        
    
    def setDefaultStyle(self, array):
        for widget in array:
            widget.setStyleSheet('''
                                color: #44d51C;
                                border-radius: 8px;
                                border-style: outset; 
                                border-width: 1px;
                                border-color:white;
                                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #888888, stop: 0.1 #222222);    
                                ''')               
        
    def setArrayStyle(self, array):
        #print("New Style for "+str(len(array)) + " keys" )
        self.array = array
        for widget in array:
            self.setKeyStyle(widget)

    def setKeyStyle(self, w):
        w.setStyleSheet(''' color: #44d51C;
                            border-radius: 8px;
                            border-style: outset;
                            border-width: 1px;
                            border-color:red;
                            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #888888, stop: 0.1 #222222);    
                        ''')
        
    
    def configMouseMode(self):
        for key in self.mouseButtonArray:
            None
            if (key.pos().y()==10):
                self.mouseArrow1.append(key)
            elif (key.pos().y()==50):
                self.mouseArrow2.append(key)
            elif (key.pos().y()==90):
                self.mouseArrow3.append(key)
    
    def configCharMode(self):
        #self.setCharModeArray()
        for key in self.charButtonArray:
                None
                if (key.pos().y()==130):
                    self.charArrow1.append(key)
                elif (key.pos().y()==170):
                    self.charArrow2.append(key)
                elif (key.pos().y()==210):
                    self.charArrow3.append(key)
      
    def configMouseKeys(self):
        for key in self.mouseButtonArray:
            key.clicked.connect(self.mouseButtonClicked)
            
            
    def configModeKeys(self):
        for key in self.modeButtonArray:
            key.clicked.connect(self.modeButtonClicked)
        
    def configCharKeys(self):
        charList = sorted(self.charDict.items(), key=itemgetter(1),reverse=True)
        print (charList)
        for key,char in zip(self.charButtonArray, charList):
            key.char =char[0]
            key.setText(_translate("Form", char[0], None)) 
            key.clicked.connect(self.charButtonClicked)
    
    def configFunctionKeys(self):
        functionList = sorted(self.functionDict.items(), key=itemgetter(1),reverse=True)
        print (functionList)
        
        for key,fun in zip(self.funButtonArray, functionList):
            key.function =fun[0]
            key.setText(_translate("Form", fun[0], None)) 
            key.clicked.connect(self.functionButtonClicked)
    
    def configNumKeys(self):
        numList = sorted(self.numDict.items(), key=itemgetter(1),reverse=True)
        operList = sorted(self.operNumDict.items(), key=itemgetter(1),reverse=True)
        numList = numList + operList
        #operAndNumDict = self.numDict
        #operAndNumDict.update(self.operNumDict)
        print (numList)
        #print (operAndNumDict)
        for key,num in zip(self.numButtonArray, numList):
            key.char =num[0]
            key.setText(_translate("Form", num[0], None)) 
            key.clicked.connect(self.charButtonClicked)
    
    def mouseButtonClicked(self):
        #print(self.sender().action + " clicked")
        act = self.sender().action
        self.mouseX = 0
        self.mouseY = 0
        self.mouseTimer.start(20)
        if(act == "u"):
            self.mouseY = -1  
            self.mode = "mouseMove"
        elif(act == "l"):
            self.mouseX = -1
        elif(act == "r"):
            self.mouseX = 1
        elif(act == "d"):
            self.mouseY = 1
        elif(act == "c"):
            self.mouseTimer.stop()
            self.mouseStop = True
            
            
        
        
        
    def mouseTick(self):
        self.mouseCursor = QCursor()
        self.mousePos = self.mouseCursor.pos()
        self.mouseCursor.setPos(QPoint(self.mousePos.x()+self.mouseX,self.mousePos.y()+self.mouseY))
        
    
    
    def modeButtonClicked(self):
        print(self.sender().mode + " clicked")
        self.mode = self.sender().mode+"3"
        if self.sender().mode == "gear":
	  #Aca tenes que hacer la voz
	  opc = self.browser.voice.start(["pesta"])
	  self.browser.commandHandler(opc,'')
	elif self.sender().mode == "mouse":
            self.mode = "mouse3"
            
    def mediaButtonClicked(self):
        if self.sender().media == "play":
            print("Media play presionada")
            QTest.keyClick(self.browser.focusWidget(),Qt.Key_Play)
        if self.sender().media == "pause":
            QTest.keyClick(self.browser.focusWidget(),Qt.Key_Pause)
            print("Media pause presionada")
        if self.sender().media == "stop":
            QTest.keyClick(self.browser.focusWidget(),Qt.Key_Stop)
            print("Media stop presionada")          
    
    def charButtonClicked(self):
        print("Char Clicked")
        if self.uppercase:
            QTest.keyClick(self.browser.focusWidget(), self.sender().char.upper())
        else:
            QTest.keyClick(self.browser.focusWidget(), self.sender().char)
        
    def functionButtonClicked(self):
        if self.sender().function == "May":
            print("Funcion May presionada")
            if self.uppercase:
                self.uppercase = False
                self.charButtonsLower(self)
                #self.sender().setDefaultStyleSheet('color: gray')
            else:
                #self.sender().setDefaultStyleSheet('color: green')
                self.uppercase = True
                self.charButtonsUpper(self)
        
        if self.sender().function == "Ent":
            print("Funcion Ent presionada")
            QTest.keyClick(self.browser.focusWidget(), Qt.Key_Enter)
        
        if self.sender().function == "Sup":
            print("Funcion Sup presionada")
            QTest.keyClick(self.browser.focusWidget(), Qt.Key_Delete)
        
        if self.sender().function == "Bsp":
            print("Funcion Bsp presionada")
            QTest.keyClick(self.browser.focusWidget(), Qt.Key_Backspace)
            
        if self.sender().function == "Esc":
            print("Funcion Esc presionada")
            QTest.keyClick(self.browser.focusWidget(), Qt.Key_Escape)
        
        if self.sender().function == "ins":
            print("Funcion Ins presionada")
            QTest.keyClick(self.browser.focusWidget(), Qt.Key_Insert)
        
        if self.sender().function == "Ctl":
            print("Funcion Ctl presionada")
            QTest.keyClick(self.browser.focusWidget(), Qt.Key_Control)
        
        if self.sender().function == "Alt":
            print("Funcion Ctl presionada")
            QTest.keyClick(self.browser.focusWidget(), Qt.Key_Alt)
        
        if self.sender().function == "Shift":
            print("Funcion Ctl presionada")
            QTest.keyClick(self.browser.focusWidget(), Qt.Key_Shift)
    
    def charButtonsUpper(self, Form):
        for key in self.charButtonArray:
            key.setText(_translate("Form", key.char.upper(), None))
            
    def charButtonsLower(self, Form):
        for key in self.charButtonArray:
            key.setText(_translate("Form", key.char, None))
    
    def setButtonFocusPolicy(self):
        for e in self.buttonArray:
            for b in e:
                b.setFocusPolicy(Qt.NoFocus)
        
        for p in self.predectiveLineEditArray:
            p.setFocusPolicy(Qt.NoFocus)  
    
    
    def setArray(self):
        #Cargando caracteres
        self.charButtonArray.append(self.keyboardUI.charButton_1_1)
        self.charButtonArray.append(self.keyboardUI.charButton_1_2)
        self.charButtonArray.append(self.keyboardUI.charButton_2_1)
        self.charButtonArray.append(self.keyboardUI.charButton_1_3)
        self.charButtonArray.append(self.keyboardUI.charButton_2_2)
        self.charButtonArray.append(self.keyboardUI.charButton_3_1)
        self.charButtonArray.append(self.keyboardUI.charButton_1_4)
        self.charButtonArray.append(self.keyboardUI.charButton_2_3)
        self.charButtonArray.append(self.keyboardUI.charButton_3_2)
        self.charButtonArray.append(self.keyboardUI.charButton_1_5)
        self.charButtonArray.append(self.keyboardUI.charButton_2_4)
        self.charButtonArray.append(self.keyboardUI.charButton_3_3)
        self.charButtonArray.append(self.keyboardUI.charButton_1_6)
        self.charButtonArray.append(self.keyboardUI.charButton_2_5)
        self.charButtonArray.append(self.keyboardUI.charButton_3_4)
        self.charButtonArray.append(self.keyboardUI.charButton_1_7)
        self.charButtonArray.append(self.keyboardUI.charButton_2_6)
        self.charButtonArray.append(self.keyboardUI.charButton_3_5)
        self.charButtonArray.append(self.keyboardUI.charButton_1_8)
        self.charButtonArray.append(self.keyboardUI.charButton_2_7)
        self.charButtonArray.append(self.keyboardUI.charButton_3_6)
        self.charButtonArray.append(self.keyboardUI.charButton_1_9)
        self.charButtonArray.append(self.keyboardUI.charButton_2_8)
        self.charButtonArray.append(self.keyboardUI.charButton_3_7)        
        self.charButtonArray.append(self.keyboardUI.charButton_2_9)
        self.charButtonArray.append(self.keyboardUI.charButton_3_8)
        self.charButtonArray.append(self.keyboardUI.charButton_3_9)
        
        #Cargando botones web
        self.webButtonArray.append(self.keyboardUI.webButton_1_1)
        self.webButtonArray.append(self.keyboardUI.webButton_1_2)
        self.webButtonArray.append(self.keyboardUI.webButton_1_3)
        self.webButtonArray.append(self.keyboardUI.webButton_1_4)
        self.webButtonArray.append(self.keyboardUI.webButton_1_5)
        
        self.webButtonArray.append(self.keyboardUI.webButton_2_1)
        self.webButtonArray.append(self.keyboardUI.webButton_2_2)
        self.webButtonArray.append(self.keyboardUI.webButton_2_3)
        self.webButtonArray.append(self.keyboardUI.webButton_2_4)
        self.webButtonArray.append(self.keyboardUI.webButton_2_5)
        
        self.webButtonArray.append(self.keyboardUI.webButton_3_1)
        self.webButtonArray.append(self.keyboardUI.webButton_3_2)
        self.webButtonArray.append(self.keyboardUI.webButton_4_1)
        self.webButtonArray.append(self.keyboardUI.webButton_3_3)
        self.webButtonArray.append(self.keyboardUI.webButton_4_2)
        self.webButtonArray.append(self.keyboardUI.webButton_3_4)
        self.webButtonArray.append(self.keyboardUI.webButton_4_3)
        self.webButtonArray.append(self.keyboardUI.webButton_3_5)
        self.webButtonArray.append(self.keyboardUI.webButton_4_4)
        self.webButtonArray.append(self.keyboardUI.webButton_back)
        
        #Cargando botones Move
        self.moveButtonArray.append(self.keyboardUI.moveButton_1_1)
        self.moveButtonArray.append(self.keyboardUI.moveButton_1_2)
        self.moveButtonArray.append(self.keyboardUI.moveButton_1_3)
        self.moveButtonArray.append(self.keyboardUI.moveButton_1_4)
        self.moveButtonArray.append(self.keyboardUI.moveButton_1_5)
        self.moveButtonArray.append(self.keyboardUI.moveButton_2_1)
        self.moveButtonArray.append(self.keyboardUI.moveButton_2_2)
        self.moveButtonArray.append(self.keyboardUI.moveButton_2_3)
        self.moveButtonArray.append(self.keyboardUI.moveButton_2_4)
        self.moveButtonArray.append(self.keyboardUI.moveButton_back)
        
        #Cargando botones Mouse
        self.mouseButtonArray.append(self.keyboardUI.mouseButton_l_u)
        self.mouseButtonArray.append(self.keyboardUI.mouseButton_u)
        self.mouseButtonArray.append(self.keyboardUI.mouseButton_r_u)
        self.mouseButtonArray.append(self.keyboardUI.mouseButton_l)
        self.mouseButtonArray.append(self.keyboardUI.mouseButton_c)
        self.mouseButtonArray.append(self.keyboardUI.mouseButton_r)
        self.mouseButtonArray.append(self.keyboardUI.mouseButton_l_d)
        self.mouseButtonArray.append(self.keyboardUI.mouseButton_d)
        self.mouseButtonArray.append(self.keyboardUI.mouseButton_r_d)
        self.mouseButtonArray.append(self.keyboardUI.mouseButton_c_l)
        self.mouseButtonArray.append(self.keyboardUI.mouseButton_c_r)
        self.mouseButtonArray.append(self.keyboardUI.mouseButton_back)
        #Cargando botones numericos
        self.numButtonArray.append(self.keyboardUI.numButton_1_1)
        self.numButtonArray.append(self.keyboardUI.numButton_1_2)
        self.numButtonArray.append(self.keyboardUI.numButton_2_1)
        self.numButtonArray.append(self.keyboardUI.numButton_1_3)
        self.numButtonArray.append(self.keyboardUI.numButton_2_2)
        self.numButtonArray.append(self.keyboardUI.numButton_1_4)
        self.numButtonArray.append(self.keyboardUI.numButton_2_3)
        self.numButtonArray.append(self.keyboardUI.numButton_1_5)
        self.numButtonArray.append(self.keyboardUI.numButton_2_4)
        self.numButtonArray.append(self.keyboardUI.numButton_2_5)
        self.numButtonArray.append(self.keyboardUI.numButton_3_1)
        self.numButtonArray.append(self.keyboardUI.numButton_3_2)
        self.numButtonArray.append(self.keyboardUI.numButton_3_3)
        self.numButtonArray.append(self.keyboardUI.numButton_3_4)
        self.numButtonArray.append(self.keyboardUI.numButton_back)
        #Cargando botones de funcion
        self.funButtonArray.append(self.keyboardUI.funButton_1_1)
        self.funButtonArray.append(self.keyboardUI.funButton_1_2)
        self.funButtonArray.append(self.keyboardUI.funButton_1_3)
        self.funButtonArray.append(self.keyboardUI.funButton_1_4)
        self.funButtonArray.append(self.keyboardUI.funButton_1_5)
        self.funButtonArray.append(self.keyboardUI.funButton_1_6)
        self.funButtonArray.append(self.keyboardUI.funButton_1_7)
        self.funButtonArray.append(self.keyboardUI.funButton_1_8)
        self.funButtonArray.append(self.keyboardUI.funButton_1_9)
        #Cargando los botones de modo
        self.modeButtonArray.append(self.keyboardUI.modeButtonMouse)
        self.modeButtonArray.append(self.keyboardUI.modeButtonMove)
        self.modeButtonArray.append(self.keyboardUI.modeButtonWeb)
        self.modeButtonArray.append(self.keyboardUI.modeButtonSym)
        self.modeButtonArray.append(self.keyboardUI.modeButtonNum)
        self.modeButtonArray.append(self.keyboardUI.modeButtonEmot)
        self.modeButtonArray.append(self.keyboardUI.modeButtonF)
        self.modeButtonArray.append(self.keyboardUI.modeButtonGear)
        self.modeButtonArray.append(self.keyboardUI.modeButtonOff)
        
        #Cargando los line edit del texto predictivo
        self.predectiveLineEditArray.append(self.keyboardUI.predectiveLineEdit_1)
        self.predectiveLineEditArray.append(self.keyboardUI.predectiveLineEdit_2)
        self.predectiveLineEditArray.append(self.keyboardUI.predectiveLineEdit_3)
        
        self.buttonArray.append(self.charButtonArray)
        self.buttonArray.append(self.mouseButtonArray)
        self.buttonArray.append(self.moveButtonArray)
        self.buttonArray.append(self.webButtonArray)
        self.buttonArray.append(self.funButtonArray)
        self.buttonArray.append(self.modeButtonArray)
        self.buttonArray.append(self.numButtonArray)
        
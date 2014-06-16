# -*- encoding: utf-8 -*-
from operator import itemgetter
from PyQt4.QtGui import QWidget, QApplication
from keyboardPyranha import Ui_Form
from PyQt4.QtCore import Qt, QTimer
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
    
    arrow1 = []
    arrow2 = []
    arrow3 = []
        
    
    mediaButtonArray = []
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
        self.setMinimumSize(860,280)
        
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
        self.configCharMode()
        self.configFunctionKeys()
        self.configNumKeys()
        self.configMediaKeys()
        
        self.setKeyStyleSheet()
        
        self.mode = "char1"
        self.click
        self.setDefaultStyle(self.arrow3)
        self.setNewStyle(self.predectiveLineEditArray)
        
        
        #configuramos y largamos el timer
        self.timer = QTimer()
        # Lo conectamos a f
        self.timer.timeout.connect(self.tick)
        # Llamamos a f() cada 5 segundos
        self.timer.start(2000)
        
    def setKeyStyleSheet(self):
        self.setDefaultStyle(self.predectiveLineEditArray)
        self.setDefaultStyle(self.mediaButtonArray)
        self.setDefaultStyle(self.webButtonArray)
        self.setDefaultStyle(self.numButtonArray)
        self.setDefaultStyle(self.modeButtonArray)
        self.setDefaultStyle(self.funButtonArray)
        self.setDefaultStyle(self.charButtonArray)
    
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
    
    def click(self):
        self.timer.timeout.disconnect(self.tick)
        self.i = 0
        self.timer.timeout.connect(self.tick2)
        
    
    def tick(self):
        if(self.mode == "char1"):
            self.mode = "char2"
            self.setDefaultStyle(self.predectiveLineEditArray)
            self.setNewStyle(self.modeButtonArray)
        elif (self.mode == "char2"):
            self.setDefaultStyle(self.modeButtonArray)
            self.setNewStyle(self.funButtonArray)
            self.mode = "char3"
        elif (self.mode == "char3"):
            self.mode = "char4_1"
            self.setDefaultStyle(self.funButtonArray)
            self.setNewStyle(self.arrow1)
        elif (self.mode == "char4_1"):
            self.mode = "char4_2"
            self.setDefaultStyle(self.arrow1)
            self.setNewStyle(self.arrow2)
        elif (self.mode == "char4_2"):
            self.mode = "char4_3"
            self.setDefaultStyle(self.arrow2)
            self.setNewStyle(self.arrow3)
        elif (self.mode == "char4_3"):
            self.mode = "char1"
            self.setDefaultStyle(self.arrow3)
            self.setNewStyle(self.predectiveLineEditArray)     
    
    def tick2(self):
        print("Tick 2" + " - i: " + str(self.i))
        
        if (self.i > len(self.array)-1):
            self.timer.timeout.disconnect(self.tick2)
            self.i = 0
            self.timer.timeout.connect(self.tick)
            self.mode = "char4_3"
            self.setDefaultStyle(self.array)
        
        else:
            self.setNewStyle(self.array)
            self.array[self.i].setStyleSheet('''
                                color: #44d51C;
                                border-radius: 8px;
                                border-style: outset; 
                                border-width: 1px;
                                border-color:blue;
                                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #888888, stop: 0.1 #222222);    
                                ''')
            self.i+=1
        
            
        
    def setNewStyle(self, array):
        self.array = array
        for widget in array:
            widget.setStyleSheet('''
                                color: #44d51C;
                                border-radius: 8px;
                                border-style: outset; 
                                border-width: 1px;
                                border-color:red;
                                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #888888, stop: 0.1 #222222);    
                                ''')

    def clearArray(self):
        None
    
    def configCharMode(self):
        self.setCharModeArray()
        charList = sorted(self.charDict.items(), key=itemgetter(1),reverse=True)
        print (charList)
        
        for key,char in zip(self.charButtonArray, charList):
            key.char =char[0]
            key.setText(_translate("Form", char[0], None)) 
            key.clicked.connect(self.charClicked)
        
        for key in self.charButtonArray:
                None
                if (key.pos().y()==145):
                    self.arrow1.append(key)
                elif (key.pos().y()==190):
                    self.arrow2.append(key)
                elif (key.pos().y()==235):
                    self.arrow3.append(key)
        
    def configFunctionKeys(self):
        functionList = sorted(self.functionDict.items(), key=itemgetter(1),reverse=True)
        print (functionList)
        
        for key,fun in zip(self.funButtonArray, functionList):
            key.function =fun[0]
            key.setText(_translate("Form", fun[0], None)) 
            key.clicked.connect(self.functionClicked)
            if fun[0] == 'May':
                key.setStyleSheet('color: gray')
        
    
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
            key.clicked.connect(self.charClicked)
            
            
    def configMediaKeys(self):
        self.keyboardUI.mediaButton_1_1.media = 'play'
        self.keyboardUI.mediaButton_1_2.media = 'stop'
        self.keyboardUI.mediaButton_1_3.media = 'pause'
        self.keyboardUI.mediaButton_1_4.media = 'rw'
        self.keyboardUI.mediaButton_1_5.media = 'ffw'
        self.keyboardUI.mediaButton_2_1.media = 'back'
        self.keyboardUI.mediaButton_2_2.media = 'mute'
        self.keyboardUI.mediaButton_2_3.media = 'vol_down'
        self.keyboardUI.mediaButton_2_4.media = 'vol_up'
        
        for key in self.mediaButtonArray:
            key.clicked.connect(self.mediaClicked)
        
    def mediaClicked(self):
        if self.sender().media == "play":
            print("Media play presionada")
            QTest.keyClick(self.browser.focusWidget(),Qt.Key_Play)
        if self.sender().media == "pause":
            QTest.keyClick(self.browser.focusWidget(),Qt.Key_Pause)
            print("Media pause presionada")
        if self.sender().media == "stop":
            QTest.keyClick(self.browser.focusWidget(),Qt.Key_Stop)
            print("Media stop presionada")
            
    
    def charClicked(self):
        print("Char Clicked")
        if self.uppercase:
            QTest.keyClick(self.browser.focusWidget(), self.sender().char.upper())
        else:
            QTest.keyClick(self.browser.focusWidget(), self.sender().char)
        
    def functionClicked(self):
        if self.sender().function == "May":
            print("Funcion May presionada")
            if self.uppercase:
                self.uppercase = False
                self.charButtonsLower(self)
                self.sender().setDefaultStyleSheet('QPushButton {color: gray}')
            else:
                self.sender().setDefaultStyleSheet('QPushButton {color: green}')
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
        self.webButtonArray.append(self.keyboardUI.webButton_4_5)
        
        self.webButtonArray.append(self.keyboardUI.webButton_5_1)
        self.webButtonArray.append(self.keyboardUI.webButton_5_2)
        self.webButtonArray.append(self.keyboardUI.webButton_5_3)
        self.webButtonArray.append(self.keyboardUI.webButton_5_4)
        self.webButtonArray.append(self.keyboardUI.webButton_5_5)
        self.webButtonArray.append(self.keyboardUI.webButton_6_1)
        self.webButtonArray.append(self.keyboardUI.webButton_6_2)
        self.webButtonArray.append(self.keyboardUI.webButton_6_3)
        self.webButtonArray.append(self.keyboardUI.webButton_6_4)
        self.webButtonArray.append(self.keyboardUI.webButton_6_5)
        
        #Cargando botones multimedia
        self.mediaButtonArray.append(self.keyboardUI.mediaButton_1_1)
        self.mediaButtonArray.append(self.keyboardUI.mediaButton_1_2)
        self.mediaButtonArray.append(self.keyboardUI.mediaButton_2_1)
        self.mediaButtonArray.append(self.keyboardUI.mediaButton_1_3)
        self.mediaButtonArray.append(self.keyboardUI.mediaButton_2_2)
        self.mediaButtonArray.append(self.keyboardUI.mediaButton_1_4)
        self.mediaButtonArray.append(self.keyboardUI.mediaButton_2_3)
        self.mediaButtonArray.append(self.keyboardUI.mediaButton_1_5)
        self.mediaButtonArray.append(self.keyboardUI.mediaButton_2_4)
        self.mediaButtonArray.append(self.keyboardUI.mediaButton_2_5)
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
        self.numButtonArray.append(self.keyboardUI.numButton_3_5)
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
        self.modeButtonArray.append(self.keyboardUI.modeButtonF)
        self.modeButtonArray.append(self.keyboardUI.modeButtonMedia)
        self.modeButtonArray.append(self.keyboardUI.modeButtonNum)
        self.modeButtonArray.append(self.keyboardUI.modeButtonSym)
        self.modeButtonArray.append(self.keyboardUI.modeButtonWeb)
        #Cargando los line edit del texto predictivo
        self.predectiveLineEditArray.append(self.keyboardUI.predectiveLineEdit_1)
        self.predectiveLineEditArray.append(self.keyboardUI.predectiveLineEdit_2)
        self.predectiveLineEditArray.append(self.keyboardUI.predectiveLineEdit_3)
        
        self.buttonArray.append(self.charButtonArray)
        self.buttonArray.append(self.mediaButtonArray)
        self.buttonArray.append(self.webButtonArray)
        self.buttonArray.append(self.funButtonArray)
        self.buttonArray.append(self.modeButtonArray)
        self.buttonArray.append(self.numButtonArray)
    
    def setCharModeArray(self):
        arrow1 = []
        arrow1.append(self.keyboardUI.predectiveLineEdit_1)
        arrow1.append(self.keyboardUI.predectiveLineEdit_2)
        arrow1.append(self.keyboardUI.predectiveLineEdit_3)
        arrow2 = []
        arrow2.append(self.keyboardUI.modeButtonSym)
        arrow2.append(self.keyboardUI.modeButtonWeb)
        arrow2.append(self.keyboardUI.modeButtonNum)
        arrow2.append(self.keyboardUI.modeButtonMedia)
        arrow2.append(self.keyboardUI.modeButtonF)
        arrow3 = []
        arrow3.append(self.keyboardUI.funButton_1_1)
        arrow3.append(self.keyboardUI.funButton_1_2)
        arrow3.append(self.keyboardUI.funButton_1_3)
        arrow3.append(self.keyboardUI.funButton_1_4)
        arrow3.append(self.keyboardUI.funButton_1_5)
        arrow3.append(self.keyboardUI.funButton_1_6)
        arrow3.append(self.keyboardUI.funButton_1_7)
        arrow3.append(self.keyboardUI.funButton_1_8)
        arrow3.append(self.keyboardUI.funButton_1_9)
        arrow4 = []
        arrow4.append(self.keyboardUI.charButton_1_1)
        arrow4.append(self.keyboardUI.charButton_1_2)
        arrow4.append(self.keyboardUI.charButton_1_3)
        arrow4.append(self.keyboardUI.charButton_1_4)
        arrow4.append(self.keyboardUI.charButton_1_5)
        arrow4.append(self.keyboardUI.charButton_1_6)
        arrow4.append(self.keyboardUI.charButton_1_7)
        arrow4.append(self.keyboardUI.charButton_1_8)
        arrow4.append(self.keyboardUI.charButton_1_9)
        arrow5 = []
        arrow5.append(self.keyboardUI.charButton_2_1)
        arrow5.append(self.keyboardUI.charButton_2_2)
        arrow5.append(self.keyboardUI.charButton_2_3)
        arrow5.append(self.keyboardUI.charButton_2_4)
        arrow5.append(self.keyboardUI.charButton_2_5)
        arrow5.append(self.keyboardUI.charButton_2_6)
        arrow5.append(self.keyboardUI.charButton_2_7)
        arrow5.append(self.keyboardUI.charButton_2_8)
        arrow5.append(self.keyboardUI.charButton_2_9)
        arrow6 = []
        arrow6.append(self.keyboardUI.charButton_3_1)
        arrow6.append(self.keyboardUI.charButton_3_2)
        arrow6.append(self.keyboardUI.charButton_3_3)
        arrow6.append(self.keyboardUI.charButton_3_4)
        arrow6.append(self.keyboardUI.charButton_3_5)
        arrow6.append(self.keyboardUI.charButton_3_6)
        arrow6.append(self.keyboardUI.charButton_3_7)
        arrow6.append(self.keyboardUI.charButton_3_8)
        arrow6.append(self.keyboardUI.charButton_3_9)
        
        
        self.charModeArray.append(arrow1)
        self.charModeArray.append(arrow2)
        self.charModeArray.append(arrow3)
        self.charModeArray.append(arrow4)
        self.charModeArray.append(arrow5)
        self.charModeArray.append(arrow6)
        
        
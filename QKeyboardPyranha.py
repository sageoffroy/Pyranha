# -*- encoding: utf-8 -*-

from operator import itemgetter
from PyQt4.QtGui import QWidget, QApplication, QCursor, QMouseEvent, QPushButton
from keyboardPyranha import Ui_Form
from PyQt4.QtCore import Qt, QTimer, QPoint, QEvent, QCoreApplication, pyqtSlot
from PyQt4.QtTest import QTest
from QWebButton import QWebButton
from QMoveButton import QMoveButton
from QNumberButton import QNumberButton
from pymouse import PyMouse

from PyranhaPredict import *

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
    
  verde='#44d51c'
  celeste='#5599c8'
  violeta='#865098'
  rojo='#FF0000'
    
  predectiveLineEditArray = []
  charModeArray = []
  funButtonArray = []
  charButtonArray = []
  
  
  charArray1 = []
  charArray2 = []
  charArray3 = []
  
  numArray1 = []
  numArray2 = []
  numArray3 = []
  
  mouseArray1 = []
  mouseArray2 = []
  mouseArray3 = []

  webArray1 = []
  webArray2 = []
  webArray3 = []
  webArray4 = []
  
  moveArray1 = []
  moveArray2 = []
      
  mouseButtonArray = []
  moveButtonArray = []
  numButtonArray = []
  webButtonArray = []
  modeButtonArray = []
  
  buttonArray = []
  
  charDict = {"a":26,"b":11,"c":16,"d":19,"e":27,"f":6,"g":8,"h":10,"i":21,"j":7,"k":2,"l":20,"m":15,"n":23,"ñ":4,"o":25,'p':14,'q':13,'r':22,'s':24,'t':17,'u':18,'v':9,'w':1,'x':3,'y':12,'z':5}
  
  functionDict ={'May':5, 'Ent':8, 'Sup':7, 'Bsp':6, 'Tab':5, 'Esc':4, 'Ins':3, 'Ctl':2, 'Alt':1}
  
  numDict = {'0':1,'1':2,'2':23,'3':4,'4':5,'5':10,'6':6,'7':8,'8':9,'9':15}
  
  operNumDict = {'+':1,'-':2,'/':3,'*':4}

  #=======Atributos Configurables===========
  time_controller = 0
  is_sortable = False
  mouse_speed = 0
  #=========================================
  
  def __init__(self, browser):
    QWidget.__init__(self)
    print("QKeyboardPyrana: iniciando teclado")
    self.setMinimumSize(860,250)
    #Referencia al navegador para obtener el foco
    self.browser = browser
    #Configurar desde el xml
    keyboard_cfg = self.browser.keyboard_cfg
    self.time_controller = int(keyboard_cfg.findtext('time_controller'))
    self.is_sortable = keyboard_cfg.findtext('is_sortable') in ['true', '1', 't', 'y', 'yes', 'si', 'certainly', 'True']
    self.mouse_speed = int(keyboard_cfg.findtext('mouse_speed'))

    #Cargando interfaz y configurando botones
    self.keyboardUI = Ui_Form()
    self.keyboardUI.setupUi(self)
    self.setArray()
    self.setButtonFocusPolicy()
    print("QKeyboardPyrana: iniciando texto predictivo")
    #Instanciamos el predict
    self.predict = PyranhaPredict()
    self.buffer = QString()
    self.refreshPredict('')
    
    #Comenzamos con la funcion mayuscula desactivada
    self.uppercase = False
    
    #Configuramos las teclas
    self.configCharKeys()
    self.configFunctionKeys()
    self.configNumKeys()
    self.configModeKeys()
    self.configMouseKeys()
    self.configWebKeys()
    self.configMoveKeys()
    
    #Configuramos los modos
    self.configCharMode()
    self.configMouseMode()
    self.configWebMode()
    self.configMoveMode()
    self.configNumMode()
    
    self.setKeyStyleSheet()
    self.mouse = PyMouse()
    self.mode = "char1"
    self.activeClick = False
    self.currentKey = None
    
    self.setArrayStyle(self.predectiveLineEditArray,'red')
    self.timer = QTimer()
    self.timer.timeout.connect(self.tick)
    self.timer.start(self.time_controller)
    
    self.mouseTimer = QTimer()
    self.mouseTimer.timeout.connect(self.mouseTick)
    self.mouseY = 0
    self.mouseX = 0
    self.mouseStop = False
        
  def setKeyStyleSheet(self):
    self.setArrayStyle(self.predectiveLineEditArray)
    self.setArrayStyle(self.mouseButtonArray)
    self.setArrayStyle(self.moveButtonArray)
    self.setArrayStyle(self.webButtonArray)
    self.setArrayStyle(self.numButtonArray)
    self.setArrayStyle(self.modeButtonArray)
    self.setArrayStyle(self.funButtonArray)
    self.setArrayStyle(self.charButtonArray)
    
        
  def click(self):
    #print(self.mode)
    if(self.mode == "off"):
      print("Teclado On")
      self.browser.showKeyboard()
      self.mode = "char1"
    elif (self.currentKey == self.keyboardUI.mouseButton_c):
      self.currentKey.clicked.emit(True)
    else:
      if (self.activeClick):
        #print ("Segundo Click")
        self.activeClick = False
        self.currentKey.clicked.emit(True)
        self.timer.timeout.disconnect(self.tick2)
        self.timer.timeout.connect(self.tick)    
      else:
        #print ("Primer Click")
        self.activeClick = True
        self.timer.timeout.disconnect(self.tick)
        self.timer.timeout.connect(self.tick2)
      self.i = 0
    
  def tick(self):

    self.setArrayStyle(self.array)        
    
    if(self.mode == "char1"):
      #print("Char 2")
      self.mode = "char2"
      self.setArrayStyle(self.modeButtonArray, 'red')
    elif (self.mode == "char2"):
      #print("Char 3")
      self.setArrayStyle(self.funButtonArray,'red')
      self.mode = "char3"
    elif (self.mode == "char3"):
        #print("Char 4_1")
        self.mode = "char4_1"
        self.setArrayStyle(self.charArray1,'red')
    elif (self.mode == "char4_1"):
        #print("Char 4_2")
        self.mode = "char4_2"
        self.setArrayStyle(self.charArray2,'red')
    elif (self.mode == "char4_2"):
        #print("Char 4_3")
        self.mode = "char4_3"
        self.setArrayStyle(self.charArray3,'red')
    elif (self.mode == "char4_3"):
        #print("Char 1")
        self.mode = "char1"
        self.setArrayStyle(self.predectiveLineEditArray,'red')
    elif (self.mode == "mouse1"):
        self.mouseStop = False
        self.mode = "mouse2"
        self.setArrayStyle(self.mouseArray1,'red')
    elif (self.mode == "mouse2"):
        self.mode = "mouse3"
        self.setArrayStyle(self.mouseArray2,'red')
    elif (self.mode == "mouse3"):
        self.mode = "mouse1"
        self.setArrayStyle(self.mouseArray3,'red')
    elif (self.mode == "web1"):
        print("web1")
        self.mode = "web2"
        self.setArrayStyle(self.webArray1,'red')
    elif (self.mode == "web2"):
        print("web2")
        self.mode = "web3"
        self.setArrayStyle(self.webArray2,'red')
    elif (self.mode == "web3"):
        print("web3")
        self.mode = "web4"
        self.setArrayStyle(self.webArray3,'red')
    elif (self.mode == "web4"):
        print("web4")
        self.mode = "web1"
        self.setArrayStyle(self.webArray4,'red')
    elif (self.mode == "move1"):
        print("move1")
        self.mode = "move2"
        self.setArrayStyle(self.moveArray1,'red')
    elif (self.mode == "move2"):
        print("move2")
        self.mode = "move1"
        self.setArrayStyle(self.moveArray2,'red')
    elif (self.mode == "num1"):
        self.mode = "num2"
        self.setArrayStyle(self.numArray1,'red')
    elif (self.mode == "num2"):
        self.mode = "num3"
        self.setArrayStyle(self.numArray2,'red')
    elif (self.mode == "num3"):
        self.mode = "num1"
        self.setArrayStyle(self.numArray3,'red')
    elif (self.mode == "off"):
        None
        
          
  def tick2(self):
    #print("tick 2")
    if (self.i > len(self.array)-1):
        self.i = 0
    
    self.setArrayStyle(self.array, 'red')
    self.currentKey = self.array[self.i] 
    self.setKeyStyle(self.array[self.i],'blue')
    
    self.i+=1
      
  
  def setArrayStyle(self, array, border_color='white'):
    self.array = array
    for widget in array:
        self.setKeyStyle(widget, border_color)

  def setKeyStyle(self, k, border_color='white'):
    color = self.verde
    
    if(type(self.array[0]) is QWebButton):
       color = self.celeste
    
    if(type(self.array[0]) is QMoveButton):
       color = self.violeta
    
    if(type(self.array[0]) is QNumberButton):
       color = self.rojo
    
    style = 'color:'+color+';border-radius: 8px;border-style: outset;border-width: 1px;border-color:'+border_color+';background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #888888, stop: 0.1 #222222);'
    k.setStyleSheet(style)
      
  #-- Metodo que refresca el texto predictivo --#
  def refreshPredict(self, s):
    s = QString(s)
    print (s.length())
    self.buffer.append(s)
    self.listPredict = self.predict.prediction (self.buffer)
    print(self.listPredict)
    if(len(self.listPredict)>= 1):
        self.keyboardUI.predectiveLineEdit_1.setText(self.listPredict[0])
    if(len(self.listPredict)>= 2): 
        self.keyboardUI.predectiveLineEdit_2.setText(self.listPredict[1])
    if(len(self.listPredict)== 3):
        self.keyboardUI.predectiveLineEdit_3.setText(self.listPredict[2])

#======================================================================================================#
#====================================MOUSE MODE========================================================#
#======================================================================================================#
  def configMouseMode(self):
      for key in self.mouseButtonArray:
          None
          if (key.pos().y()==10):
              self.mouseArray1.append(key)
          elif (key.pos().y()==50):
              self.mouseArray2.append(key)
          elif (key.pos().y()==90):
              self.mouseArray3.append(key)
  
  def configMouseKeys(self):
      for key in self.mouseButtonArray:
          if (key.accessibleName()=="back"):
              key.clicked.connect(self.backButtonClicked)
          else:
              key.clicked.connect(self.mouseButtonClicked)
  
  @pyqtSlot()
  def mouseButtonClicked(self):
      act = self.sender().action
      print("Action = "+ act)
      if((act != "c") and (act != "cl") and (act != "cr")):
          print ("necesita frenar")
          self.mouseTimer.start(self.mouse_speed)
          self.timer.stop()
          self.setArrayStyle(self.array, 'white')
          self.currentKey = self.keyboardUI.mouseButton_c
          self.setKeyStyle(self.currentKey, 'blue')
      
      if(act == "u"):
          self.mouseX = 0
          self.mouseY = -1  
      elif(act == "l"):
          self.mouseX = -1
          self.mouseY = 0
      elif(act == "r"):
          self.mouseX = 1
          self.mouseY = 0
      elif(act == "d"):
          self.mouseX = 0
          self.mouseY = 1
      elif(act == "lu"):
          self.mouseY = -1
          self.mouseX = -1
      elif(act == "ru"):
          self.mouseY = -1
          self.mouseX = 1
      elif(act == "ld"):
          self.mouseY = 1
          self.mouseX = -1
      elif(act == "rd"):
          self.mouseY = 1
          self.mouseX = 1
      elif(act == "c"):
          if ((self.mouseX != 0) or (self.mouseY != 0)):
              self.mouseY = 0
              self.mouseX = 0
              self.timer.start(self.time_controller)
              self.mouseTimer.stop()
              self.setKeyStyle(self.currentKey, 'white')
              self.currentKey = None
          else:
              print("EL mouse esta quieto")
      elif(act == "cr"):
          print("Click derecho")
          self.mouse.click(self.mousePos.x(), self.mousePos.y(), 2)
      elif(act == "cl"):
          print("Click izquierdo")
          self.mouse.click(self.mousePos.x(), self.mousePos.y(), 1)
  
  def mouseTick(self):
    self.mouseCursor = QCursor()
    self.mousePos = self.mouseCursor.pos()
    self.mouseCursor.setPos(QPoint(self.mousePos.x()+self.mouseX,self.mousePos.y()+self.mouseY))
#======================================================================================================#
#=====================================CHAR MODE========================================================#
#======================================================================================================#
  def configCharMode(self):
    for key in self.charButtonArray:
      if (key.pos().y()==130):
          self.charArray1.append(key)
      elif (key.pos().y()==170):
          self.charArray2.append(key)
      elif (key.pos().y()==210):
          self.charArray3.append(key)
                
  def configCharKeys(self):
      charList = sorted(self.charDict.items(), key=itemgetter(1),reverse=True)
      for key,char in zip(self.charButtonArray, charList):
          key.char =char[0]
          key.setText(_translate("Form", char[0], None)) 
          key.clicked.connect(self.charButtonClicked)
          
      
  def charButtonClicked(self):
      print("Char Clicked")
      
      if self.uppercase:
          key =  self.sender().text().toUpper()
      else:
          key =  self.sender().text()
      self.refreshPredict(key)
      print(self.is_sortable)
      if (len(key) == 1) and (self.is_sortable):
          print("ACTUALIZANDO TECLADO CHAR")
          val = self.charDict.get(str(key))
          print("Letra "+ key + " y su peso es: " + str(self.charDict.get(str(key))))
          val+=1
          self.charDict[str(key)]=val
          #print("Peso de la letra "+ key + ": " + str(self.charDict.get(str(key))))
          charList = sorted(self.charDict.items(), key=itemgetter(1),reverse=True)
          for k,c in zip(self.charButtonArray, charList):
              k.char =c[0]
              k.setText(_translate("Form", c[0], None))
          
      for c in key:
        QTest.keyClick(self.browser.focusWidget(), c)
      
#======================================================================================================#
#=====================================NUMBER MODE========================================================#
#======================================================================================================#        
  def configNumMode(self):
      print ("Configurando el modo numerico")
      for key in self.numButtonArray:
              if (key.pos().y()==130):
                  self.numArray1.append(key)
              elif (key.pos().y()==170):
                  self.numArray2.append(key)
              elif (key.pos().y()==210):
                  self.numArray3.append(key)
      
  
  def configNumKeys(self):
      numList = sorted(self.numDict.items(), key=itemgetter(1),reverse=True)
      operList = sorted(self.operNumDict.items(), key=itemgetter(1),reverse=True)
      numList = numList + operList
      numList.append(("b",0))
      print (numList)
      for key,num in zip(self.numButtonArray, numList):
          if (key.accessibleName()=="back"):
              key.clicked.connect(self.backButtonClicked)
          else:
              key.char =num[0]
              key.setText(_translate("Form", num[0], None)) 
              key.clicked.connect(self.numButtonClicked)
  
  
  def numButtonClicked(self):
      key =  self.sender().text()
      QTest.keyClick(self.browser.focusWidget(), key)
      if self.numDict.has_key(str(key)):
          print("es un numero")
          val = self.numDict.get(str(key))
          val+=1
          self.numDict[str(key)]=val
      else:
          print("es un operador")
          val = self.operNumDict.get(str(key))
          val+=1
          self.operNumDict[str(key)]=val
          
      numList = sorted(self.numDict.items(), key=itemgetter(1),reverse=True)
      operList = sorted(self.operNumDict.items(), key=itemgetter(1),reverse=True)
      numList = numList + operList
      print (numList)
      for k,c in zip(self.numButtonArray, numList):
          k.char =c[0]
          k.setText(_translate("Form", c[0], None))
      
      
      
  
#======================================================================================================#
#===================================FUNCTION MODE======================================================#
#======================================================================================================#
  def configFunctionKeys(self):
      functionList = sorted(self.functionDict.items(), key=itemgetter(1),reverse=True)
      print (functionList)
      
      for key,fun in zip(self.funButtonArray, functionList):
          key.function =fun[0]
          key.setText(_translate("Form", fun[0], None)) 
          key.clicked.connect(self.functionButtonClicked)
  
      self.predectiveLineEditArray[0].clicked.connect(self.charButtonClicked)
      self.predectiveLineEditArray[1].clicked.connect(self.charButtonClicked)
      self.predectiveLineEditArray[2].clicked.connect(self.charButtonClicked)
  
  def functionButtonClicked(self):
      if self.sender().function == "May":
          print("Funcion May presionada")
          if self.uppercase:
              self.uppercase = False
              self.charButtonsLower(self)
          else:
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
  
#======================================================================================================#
#======================================WEB MODE========================================================#
#======================================================================================================#
  def configWebMode(self):
      for key in self.webButtonArray:
          if (key.pos().y()==90):
              self.webArray1.append(key)
          elif (key.pos().y()==130):
              self.webArray2.append(key)
          elif (key.pos().y()==170):
              self.webArray3.append(key)
          elif (key.pos().y()==210):
              self.webArray4.append(key)
  
  def configWebKeys(self):
      for key in self.webButtonArray:
          if (key.accessibleName()=="back"):
              key.clicked.connect(self.backButtonClicked)
          else:
              key.clicked.connect(self.webButtonClicked)
  
  def webButtonClicked(self):
      print("Mode Web")
      if(self.sender().web_function=="go"):
          print "go"
      if(self.sender().web_function=="home"):
          self.browser.loadURL(self.browser.web, self.browser.default_url)
      elif(self.sender().web_function=="new_tab"):
          self.browser.createTab(self.browser.default_url)
      elif(self.sender().web_function=="stop"):
          self.browser.stop()
      elif(self.sender().web_function=="refresh"):
          self.browser.reload()
      elif(self.sender().web_function=="zoom_out"):
          self.browser.zoomIn()
      elif(self.sender().web_function=="zoom_in"):
          self.browser.zoomOut()
      elif(self.sender().web_function=="config"):
          None
      elif(self.sender().web_function=="next"):
          self.browser.goNext()
      elif(self.sender().web_function=="back"):
          self.browser.goBack()
      else:
          for c in self.sender().web_function:
              QTest.keyClick(self.browser.focusWidget(), c)
          
#======================================================================================================#
#=====================================MOVE MODE========================================================#
#======================================================================================================#
  def configMoveMode(self):
      for key in self.moveButtonArray:
          if (key.pos().y()==10):
              self.moveArray1.append(key)
          elif (key.pos().y()==50):
              self.moveArray2.append(key)
          
  def configMoveKeys(self):
      for key in self.moveButtonArray:
          if (key.accessibleName()=="back"):
              key.clicked.connect(self.backButtonClicked)
          else:
              key.clicked.connect(self.moveButtonClicked)
  
  def moveButtonClicked(self):
      print(self.sender().move_function + " clicked")
      
      if self.sender().move_function == 'tab':
          QTest.keyClick(self.browser.focusWidget(), Qt.Key_Tab)
      if self.sender().move_function == 'fin':
          QTest.keyClick(self.browser.focusWidget(), Qt.Key_End)
      if self.sender().move_function == 'ini':
          QTest.keyClick(self.browser.focusWidget(), Qt.Key_Home)
      if self.sender().move_function == 'rep':
          QTest.keyClick(self.browser.focusWidget(), Qt.Key_PageUp)
      if self.sender().move_function == 'avp':
          QTest.keyClick(self.browser.focusWidget(), Qt.Key_PageDown)
      if self.sender().move_function == 'left':
          QTest.keyClick(self.browser.focusWidget(), Qt.Key_Left)
      if self.sender().move_function == 'right':
          QTest.keyClick(self.browser.focusWidget(), Qt.Key_Right)
      if self.sender().move_function == 'up':
          QTest.keyClick(self.browser.focusWidget(), Qt.Key_Up)
      if self.sender().move_function == 'down':
          QTest.keyClick(self.browser.focusWidget(), Qt.Key_Down)
      """elif self.sender().mode == "hand":
          opc = self.browser.handDetector.start()        
          self.browser.commandHandler(opc,'')
      elif self.sender().mode == "off":
          self.mode = "off"
          self.browser.hideKeyboard()
      else:
          self.mode = self.sender().mode+'1'"""
  
  
              
#======================================================================================================#
#====================================OTROS=============================================================#
#======================================================================================================#
  
  def configModeKeys(self):
      for key in self.modeButtonArray:
          key.clicked.connect(self.modeButtonClicked)
      
  
  
  def modeButtonClicked(self):
      print(self.sender().mode + " clicked")
      if self.sender().mode == "voice":
          opc = self.browser.voice.start(self.browser.COMMAND)
          self.browser.commandHandler(opc,'')
      elif self.sender().mode == "hand":
          opc = self.browser.handDetector.start()        
          self.browser.commandHandler(opc,'')
      elif self.sender().mode == "off":
          print ("Teclado Off")
          self.mode = "off"
          self.browser.hideKeyboard()
      else:
          self.mode = self.sender().mode+"1"
          
  def backButtonClicked(self):
      self.mode = "char4_3"
  
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
    self.modeButtonArray.append(self.keyboardUI.modeButtonVoice)
    self.modeButtonArray.append(self.keyboardUI.modeButtonMouse)
    self.modeButtonArray.append(self.keyboardUI.modeButtonMove)
    self.modeButtonArray.append(self.keyboardUI.modeButtonWeb)
    self.modeButtonArray.append(self.keyboardUI.modeButtonSym)
    self.modeButtonArray.append(self.keyboardUI.modeButtonNum)
    self.modeButtonArray.append(self.keyboardUI.modeButtonEmot)
    self.modeButtonArray.append(self.keyboardUI.modeButtonHand)
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
    
    
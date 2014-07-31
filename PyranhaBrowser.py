import sys
from PyQt4.QtCore import Qt, QUrl
from PyQt4.QtGui import QLineEdit, QMainWindow, QIcon, QWidget, QVBoxLayout, QHBoxLayout, QKeyEvent, QToolButton, QTabWidget, QApplication
from PyQt4.QtWebKit import QWebView

#from urllib.request import urlopen
from urllib2 import urlopen

import os

from QKeyboardPyranha import QKeyboardPyranha

from vox import Vox
from hand import Hand

JQUERY_URL = 'http://code.jquery.com/jquery-1.11.0.min.js'
JQUERY_FILE = JQUERY_URL.split('/')[-1]
JQUERY_PATH = os.path.join(os.path.dirname(__file__), JQUERY_FILE)


def getJquery(jquery_url=JQUERY_URL, jquery_path=JQUERY_PATH):
        if not os.path.exists(jquery_path):
            jquery = urlopen(jquery_url).read()
            f = open(jquery_path, 'w')
            f.write(jquery)
            f.close()
        else:
            f = open(jquery_path)
            jquery = f.read()
            f.close()
        return jquery

def getFuncionesJs():
    js_path=os.path.join(os.path.dirname(__file__), 'funciones.js')
    f = open(js_path)
    js = f.read()
    f.close()
    return js


class QPyranhaWebView(QWebView):

    def __init__(self):
        QWebView.__init__(self)
        #self.settings().setAttribute(QWebSettings.PluginsEnabled, True)
        #Form.setStyleSheet(_fromUtf8("color:#3ea700")) VERDE
        #self.modeButtonNum.setStyleSheet(_fromUtf8("color:#ff0000")) ROJO
        #self.modeButtonMedia.setStyleSheet(_fromUtf8("color:#fd750f")) NARANJA
        #self.modeButtonF.setStyleSheet(_fromUtf8("color:#ff0000")) ROJO
        #self.modeButtonWeb.setStyleSheet(_fromUtf8("color:#2496b6")) TURQUESA

class MyLineEdit(QLineEdit):
    def __init__(self, *args):
        QLineEdit.__init__(self, *args)
        
        
    
class PyranhaBrowser(QMainWindow):
    COMMAND = ['inicio','pesta','detener','recarga']
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(1024, 800)
        self.setWindowIcon(QIcon('img/logo5.png'))
        self.setWindowTitle('Pyranha Browser')
        self.default_url="http://www.google.com.ar"
        self.initGui()
        self.voice = Vox()
        self.handDetector = Hand()
        self.loadHome()
        self.jquery = getJquery()
        self.funcionesJs=getFuncionesJs()
        self.resizeEvent = self.onResize
        self.activeKey = False;

    def initGui(self):
        self.centralwidget = QWidget(self)
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setMargin(0)
        self.mainLayout.setSpacing(0)
        self.createTabBar()
        
        self.keyboard = QKeyboardPyranha(self)
        self.mainLayout.addWidget(self.keyboard)
        self.centerWidget(self.mainLayout, self.keyboard)
       
        #self.createNavBar()
        self.setCss()
        self.setCentralWidget(self.centralwidget)
        
    def keyPressEvent(self, event):
        if(event.isAutoRepeat()):
            None
        else:
            if type(event) == QKeyEvent and event.key() == Qt.Key_AltGr: 
                print("Pulsador")
                self.keyboard.click()
            else:
                QLineEdit.keyPressEvent(self.focusWidget(), event)
        
    def onResize(self, event):
        self.centerWidget(self.tabLayout, self.keyboard)

    def loadHome(self):
        #self.createTab(self.default_url)
        self.createTab("https://www.google.com")
        #self.createTab("http://www.ole.com.ar")
        #self.createTab("http://www.tekoavirtual.chubut.edu.ar")
        #self.createTab("http://www.chubut.edu.ar")

    def createTabBar(self):
        self.tabBarWidget = QTabWidget(self)
        self.tabBarWidget.setMovable(True)
        self.tabBarWidget.setTabsClosable(True)
        self.tabBarWidget.currentChanged.connect(self.tabChanged)
        self.tabBarWidget.tabCloseRequested.connect(self.closeTab)
        self.addtabButton = QToolButton()
        self.addtabButton.setIcon(QIcon('img/addTab.png'))
        self.addtabButton.clicked.connect(lambda: self.createTab(self.default_url))
        self.tabBarWidget.setCornerWidget(self.addtabButton,Qt.TopRightCorner)
        self.mainLayout.addWidget(self.tabBarWidget)

    def createTab(self, url):
        self.tabLayout = QVBoxLayout()
        self.tabLayout.setMargin(0)
        self.tabLayout.setSpacing(0)
        tab = QWidget()
        tab.setLayout(self.tabLayout)

        #-- Creando NavBar
        navBar = QWidget()
        navBar.setMaximumHeight(27)
        backButton = QToolButton()
        backButton.setIcon(QIcon('img/goBack5.png'))
        nextButton = QToolButton()
        nextButton.setIcon(QIcon('img/goNext5.png'))
        stopButton = QToolButton()
        stopButton.setIcon(QIcon('img/stopLoad5.png'))
        buttonGO = QToolButton()
        buttonGO.setIcon(QIcon('img/goGo5.png'))
        self.urlBox = MyLineEdit()

        navBarLayout = QHBoxLayout()
        navBarLayout.setMargin(0)
        navBarLayout.setSpacing(0)
        navBarLayout.addWidget(backButton)
        navBarLayout.addWidget(nextButton)
        navBarLayout.addWidget(stopButton)
        navBarLayout.addWidget(self.urlBox)
        navBarLayout.addWidget(buttonGO)
        navBar.setLayout(navBarLayout)
        
        self.tabLayout.addWidget(navBar)

        #-- Creando la vista Web
        self.web = QPyranhaWebView()
        self.tabLayout.addWidget(self.web)
        
        #-- Cargando keyboard
        #self.keyboardLayout=QHBoxLayout()
        #self.keyboardLayout.setMargin(0)
        #self.keyboardLayout.setSpacing(0)
        ##tabLayout.addLayout(self.keyboardLayout)
        #print (self.width())
        #print (self.height())
        
        
        #-- Signals
        self.urlBox.returnPressed.connect(lambda: self.loadURL(self.web, self.urlBox.displayText()))
        buttonGO.clicked.connect(lambda: self.loadURL(self.web, self.urlBox.displayText()))
        backButton.clicked.connect(lambda: self.goBack(self.web, self.urlBox))
        nextButton.clicked.connect(lambda: self.goBack(self.web, self.urlBox))
        #stopButton.clicked.connect(self.stopLoad)
        self.web.loadFinished.connect(lambda:self.loadFinished(self.web,self.urlBox))
        self.web.linkClicked.connect(self.handleLinkClicked)

        #web.urlChanged.connect(self.updateUrlBox)
        #web.connect(web, QtCore.SIGNAL('loadFinished(bool)'), self.loadFinished)
        self.tabBarWidget.setCurrentIndex(self.tabBarWidget.addTab(tab, 'Cargando...'))
        self.web.load(QUrl(str(url)))

        #Set Focus URL Box
        self.urlBox.setFocus()
        self.urlBox.selectAll()

    def centerWidget(self, layout, widget):
        layout.setAlignment(widget, Qt.AlignCenter)
    
    def closeTab(self, num):
        self.tabBarWidget.removeTab(num)

    def tabChanged(self, num):

        for child in self.tabBarWidget.widget(num).findChildren(QWebView):
            self.setWindowTitle("Pyranha  " + child.title())
            #for child in self.tabBarWidget.widget(num).findChildren(QLineEdit):
            #self.focusURLBox(child)

    def loadFinished(self, web, urlBox):
        print("Load Finished")
        urlBox.setText(web.url().scheme()+"://" + web.url().host())


        espacios = ""

        for child in self.tabBarWidget.currentWidget().findChildren(QWebView):
            if len(child.title()) > 20:
                str = child.title()[0:17] + "..."
            elif len(child.title()) <= 20:
                for x in range(1, 21 - len(child.title())):
                    espacios = espacios +" "
                str = child.title()+espacios
            self.setWindowTitle("Pyranha  " + child.title())
            self.tabBarWidget.setTabText(self.tabBarWidget.currentIndex(),str)

        #doc = web.page().mainFrame().documentElement()

        web.page().mainFrame().evaluateJavaScript(self.jquery)
        web.page().mainFrame().evaluateJavaScript(self.funcionesJs)

        """inputCollection = doc.findAll("input")

        inputList = inputCollection.toList()
        t = []
        for we in inputList:
            print("---> "+we.toOuterXml())
            #print("ACA: ---> "+t.toOuterXml())
        for we in inputList:
            if we.toOuterXml().contains("submit", 1):
                print("Sacando Boton")
            if we.toOuterXml().contains("hidden", 1):
                print("Sacando Input Oculto")
            if we.toOuterXml().contains("radio", 1):
                print("Sacando Radio")
            if we.toOuterXml().contains("checkbox", 1):
                print("Sacando Checkbox")
            else:
                t.append(we)
        for h in t:
            print("Ejecutando JS A: "+h.toOuterXml())

            if h.hasFocus():
                print("FOCO---> "+h.toOuterXml())"""


    """def updateTitle(self):
        for tab in range(self.tabWidget.count()):
                self.setWindowTitle(self.tabWidget.widget(tab).title())
            self.tabWidget.setTabText(tab,self.tabWidget.widget(tab).title())"""


    """ Aca se deberia mostrar el teclado """
    def showKeyboard(self):
        print("Mostrar Teclado")


    def commandHandler(self,opc,extra):
        
        if opc == 1:
	    if extra == '':
	        self.createTab(self.default_url)
	    else:
	        self.createTab(extra)
	elif opc == 2:
	    self.loadHome()
	elif opc == 3:
	    self.stop()
	elif opc == 4:
	    self.reload()
	else:
	    print "No hay comando reconocido"

    #----- NavBar Function -----#

    def handleLinkClicked(self, url):
        print(url.toString())


    def loadURL(self, web, text):
        if 1 == 1:
            text = str(text)
            if not text.startswith("http://") and not text.startswith("https://") and not text.startswith("~") and not os.path.isdir(text) and not text.startswith("file://") and not text.startswith("javascript:") and not text.startswith("about:"):
                text = "http://" + text
            if os.path.isdir(text):
                text = "file://" + text
                self.directoryLoader(text)
            elif text.startswith("file://") and os.path.isdir(text.replace("file://","")):
                self.directoryLoader(text)
            elif text == "file://":
                self.directoryLoader("file:///")
            elif text == "~":
                self.directoryLoader(os.path.expanduser("~"))
            else:
                web.load(QUrl(str(text)))

    def goBack(self, web, urlBox):
        web.back()
        #focusURLBox(urlbox)

    def goNext(self, web, urlBox):
        web.forward()
        url = self.web.url()
        url = url.toString()
        url = str(url)
        urlBox.setText(url)
        self.focusURLBox(urlBox)

    def stopLoad(self):
        self.web.stop()

    def updateUrlBox(self):
        url = self.web.url()
        url = url.toString()
        url = str(url)
        self.urlBox.setText(url)

    #---- set Style Css ----- #
    def setCss(self):
        #-- Fondo:             #46483E
        #-- Fondo Oscuro:      #33342D
        #-- Objetos Verdes:    #8CC84B
        #-- Objetos Naranjas:  #ed6400
        #-- Gradient Effect:   background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);

        css = """

        QToolTip
        {
             border: 1px solid black;
             /*background-color: #ffa02f;*/
             padding: 1px;
             border-radius: 3px;
             opacity: 100;
        }

        QWidget
        {
            /*color: #b1b1b1;*/
            /*background-color: #323232;*/
        }

        QWidget:item:hover
        {
            background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #ca0619);
            color: #000000;
        }

        QWidget:item:selected
        {
            /*background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);*/
        }

        QWidget:disabled
        {
            color: #404040;
            background-color: #323232;
        }

        QAbstractItemView
        {
            background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0.1 #646464, stop: 1 #5d5d5d);
        }

        QWidget:focus
        {
            /*border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);*/
        }

        QLineEdit
        {
            background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);
            padding: 1px;
            border-style: solid;
            border: 1px solid #1e1e1e;
            color: #8CC84B;
            selection-background-color: #8CC84B;
            border-radius: 5;
        }

        QToolButton
        {
            background: transparent;
        }


        QTextEdit:focus
        {
            border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
        }


        QTextEdit
        {
            background-color: #242424;
        }

        QPlainTextEdit
        {
            background-color: #242424;
        }

        QMainWindow {
            background-color: #323232;

        }
        QMainWindow::separator
        {
            /*background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);*/

            color: white;
            padding-left: 4px;
            border: 1px solid #4c4c4c;
            spacing: 3px; /* spacing between items in the tool bar */
        }

        QMainWindow::separator:hover
        {

            /*background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d7801a, stop:0.5 #b56c17 stop:1 #ffa02f);*/
            
            color: white;
            padding-left: 4px;
            border: 1px solid #6c6c6c;
            spacing: 3px; /* spacing between items in the tool bar */
        }

        QTabBar::tab {
            background: transparent;
            color: #b1b1b1;
            border: 1px solid #444;
            border-bottom-style: none;
            background-color: #323232;
            padding-left: 10px;
            padding-right: 10px;
            padding-top: 3px;
            padding-bottom: 2px;
            margin-right: -1px;
        }

        QTabWidget::pane {
            border: 1px solid #444;
            top: 1px;
        }

        QTabBar::tab:last
        {
            margin-right: 0; /* the last selected tab has nothing to overlap with on the right */
            border-top-right-radius: 3px;
        }

        QTabBar::tab:first:!selected
        {
            margin-left: 0px; /* the last selected tab has nothing to overlap with on the right */
            border-top-left-radius: 3px;
        }

        QTabBar::tab:!selected
        {
            color: #b1b1b1;
            border-bottom-style: solid;
            margin-top: 3px;
            background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:.4 #343434);
        }

        QTabBar::tab:selected
        {
            border-top-left-radius: 3px;
            border-top-right-radius: 3px;
            margin-bottom: 0px;
        }

        QTabBar::tab:!selected:hover
        {
            border-top-left-radius: 3px;
            border-top-right-radius: 3px;
            background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:0.4 #424242, stop:0.2 #636363, stop:0.1 #848484);
        }


        """

        self.setAutoFillBackground(True)
        self.setStyleSheet(css)



# ///////////////////////////////////////////////////////////////////////////////////////////////#
# MAIN
# ///////////////////////////////////////////////////////////////////////////////////////////////#
def main():
    app = QApplication(sys.argv)
    browser = PyranhaBrowser()
    browser.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

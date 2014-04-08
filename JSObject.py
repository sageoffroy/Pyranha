from PyQt4 import QtCore, QtGui, QtWebKit, Qt
import sys


class JSObject(QtCore.QObject):

    #@Qt.pyqtSignature('QWebElement')
    @QtCore.pyqtSlot(QtWebKit.QWebElement)
    def test(self, webelement):
        print('Comunication with jsobject worked!')
              # print(webelement.tagName()) #test if actually returned a
              # webelement

    def loadJSObject(self):
        webview.page().mainFrame().evaluateJavaScript('')

    def _pyVersion(self):
        """Return the Python version."""
        return sys.version

    """Python interpreter version property."""
    pyVersion = QtCore.pyqtProperty(str, fget=_pyVersion)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    webview = QtWebKit.QWebView()
    QtWebKit.QWebSettings.globalSettings().setAttribute(
        QtWebKit.QWebSettings.DeveloperExtrasEnabled, True
    )
    py_bridge = JSObject()

    def attachObject():
        print ("Attaching instance")
        webview.page().mainFrame().addToJavaScriptWindowObject("py_bridge", py_bridge)

    webview.page().mainFrame().javaScriptWindowObjectCleared.connect(attachObject)
    #webview.page().connect(
    #    webview.page(), QtCore.SIGNAL('loadFinished(bool)'), js_obj.loadJSObject)
    webview.setHtml('''
        <html>
        <head>
            <title></title>
            <script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
        </head>
        <body><p>This is a test html!
        <script>

            $(function () {
                console.log("Creando cosas");
                $(document).click(function () {
                    console.log("Click");
                    $('body').append("Probando");
                    window.py_bridge.test(event.target);
                });
            });
        </script>
        </body></html>
    ''')

    webview.show()
    sys.exit(app.exec_())
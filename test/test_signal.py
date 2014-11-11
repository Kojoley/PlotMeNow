from PyQt4.QtCore import QObject, SIGNAL
class A:
    def main(self,text):
        print "Object A recived:",text
class B(QObject):
    def send(self,text):
        print "Object B sends:",text
        self.emit( SIGNAL("main(PyQt_PyObject)"), text )
if __name__=="__main__":
    a = A()
    b = B()
    QObject.connect( b, SIGNAL("main(PyQt_PyObject)"), a.main )
    b.send("Ololo")
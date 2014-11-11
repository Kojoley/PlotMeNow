from PyQt4.QtCore import QObject, SIGNAL
class A:
    def __init__(self, b):
        b.connect( b, SIGNAL("main"), self.main )

    def main(self,text):
        print "Object A recived:",text

class B(QObject):
    def send(self,text):
        print "Object B sends:",text
        self.emit( SIGNAL("main"), text )

if __name__=="__main__":
    b = B()
    a = A(b)
    b.send("Ololo")
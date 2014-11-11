# -*- mode: python -*-
# -*- coding: utf-8 -*-

from PyQt4 import Qt
from PyQt4 import QtCore
#from PyQt4 import QtGui
#import PyQt4.Qwt5 as Qwt
#from PyQt4.Qwt5.anynumpy import array_equal
#from PyQt4.Qwt5.anynumpy import subtract
from pmn.Plotter import Plotter

class Epsilon(Plotter):
    """Creates a Epsilon plotting
    """
    def __init__(self, plot, a=None, b=None):
        #print 'create Epsilon', a.__class__.__name__, b.__class__.__name__
        # Initialize some local variables
        self.__a = None
        self.__b = None
        # Call parent constructor
        Plotter.__init__(self, plot)
        self.curve.setPen(Qt.QPen(Qt.Qt.blue, 1))
        # Connect signals
        self.setAB(a, b)
        # Replot
        self.replot()

    # __init__()
    '''
    def setBounds(self, minX, maxX, minY, maxY):
        Plotter.setBounds(self, minX, maxX, minY, maxY)

#        if self.__a.dataX == self.__b.dataX:
#            self.replot()
        self.replot()
    '''
    # setBounds()

    def destroy(self, *args):
        Plotter.destroy(self, *args)
        QtCore.QObject.disconnect(self.__a, QtCore.SIGNAL("dataChanged"), self.update)
        QtCore.QObject.disconnect(self.__b, QtCore.SIGNAL("dataChanged"), self.update)

    # destroy()

    def reconnect(self):
        """ FIXME: This makes Epsilon.changedBounds slot be called latest in queue
            Qt Docs: If a signal is connected to several slots,
            the slots are activated in the same order as the order
            the connection was made, when the signal is emitted. """
        QtCore.QObject.disconnect(self.plot, QtCore.SIGNAL("changedBounds"), self.changedBounds)
        QtCore.QObject.connect(self.plot, QtCore.SIGNAL("changedBounds"), self.changedBounds)

    # reconnect()

    def update(self):
        a = self.__a
        b = self.__b
        if a is None or a.dataX is None or \
           b is None or b.dataX is None or \
           b.ppc != a.ppc or \
           a.dataX[0] != b.dataX[0]:
            self.curve.setData([], [])
        else:
            self.dataX = a.dataX
            self.dataY = b.dataY - a.dataY
            self.curve.setData(self.dataX, self.dataY)

    # update()

    def __setSome(self, watch, curve=None):
        if watch is not None:
            QtCore.QObject.disconnect(watch, QtCore.SIGNAL("dataChanged"), self.update)
        if curve is not None:
            QtCore.QObject.connect(curve, QtCore.SIGNAL("dataChanged"), self.update)
        return curve

    # __setSome()

    def setA(self, a=None):
        print self.__class__.__name__, 'setA', a
        self.__a = self.__setSome(self.__a, a)
        self.update()
        return self

    # setA()

    def setB(self, b=None):
        print self.__class__.__name__, 'setB', b
        self.__b = self.__setSome(self.__b, b)
        self.update()
        return self

    # setB()

    def setAB(self, a=None, b=None):
        self.setA(a)
        self.setB(b)
        return self

    # setAB()

# class Epsilon

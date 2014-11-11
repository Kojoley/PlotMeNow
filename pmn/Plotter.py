# -*- mode: python -*-
# -*- coding: utf-8 -*-

from PyQt4 import QtCore
import PyQt4.Qwt5 as Qwt

class Plotter(QtCore.QObject):
    """Creates a Plotter
    """
#    def __init__(self, *args):
    def __init__(self, plot):
        QtCore.QObject.__init__(self)

        self.plot = plot
        self.ppc = lambda: 2 * plot.width()
        self.canvasMap = self.plot.canvasMap

        self.minX = None
        self.maxX = None
        self.minY = None
        self.maxY = None

        self.curve = Qwt.QwtPlotCurve()
        self.curve.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased, True)
        self.curve.attach(plot)

        self.changedBounds(*plot.getBounds())

        QtCore.QObject.connect(self.plot, QtCore.SIGNAL("mouseClick"), self.mouseClick)
        QtCore.QObject.connect(self.plot, QtCore.SIGNAL("changedBounds"), self.changedBounds)

    # __init__()

    def __del__(self, *args):
        data = self.serialize()
        print self.__class__.__name__, 'is deleting now!', data
        # Send signal with serialized curve (used by redo operation)
        QtCore.QObject.emit(self, QtCore.SIGNAL("curveDestroy"), data)
        # Detach curve from plot
        if self.curve:
            self.curve.detach()
            del self.curve

    # __del__()

    def destroy(self):
        QtCore.QObject.disconnect(self.plot, QtCore.SIGNAL("mouseClick"), self.mouseClick)
        QtCore.QObject.disconnect(self.plot, QtCore.SIGNAL("changedBounds"), self.changedBounds)

    # destroy()

    def changedBounds(self, minX, maxX, minY, maxY):
        '''
        #if not isSet:
        #    print abs(maxX - minX) / abs(self.maxX - self.minX)
        #    print self.d, minX, self.minX, maxX, self.maxX
        #if not hasattr(self, 'd') or minX <= self.minX or maxX >= self.maxX or abs(maxX - minX) / abs(self.maxX - self.minX) < 0.5:
        #print abs(1.0 - (maxX - minX) / (self.maxX - self.minX))
        if (self.maxX - self.minX) / (maxX - minX) > 1.01:
            self.d = d = abs(maxX - minX) / 4
            self.setBounds(minX - d , maxX + d, minY, maxY)
        '''
        self.setBounds(minX, maxX, minY, maxY)

    # setBounds()

    def setBounds(self, minX, maxX, minY, maxY):
        self.minX, self.maxX, self.minY, self.maxY = minX, maxX, minY, maxY
        self.update()

    # setBounds()

    def mouseClick(self, event):
        pass

    # mouseClick()

    def update(self):
        pass

    # update()

    def replot(self):
        self.update()
        self.plot.replot()

    # replot()

    def serialize(self):
        pass

    # serialize()

    def unserialize(self, data):
        pass

    # unserialize()

# class Plotter

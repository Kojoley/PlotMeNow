# -*- mode: python -*-
# -*- coding: utf-8 -*-

from PyQt4 import Qt
from PyQt4 import QtCore
import PyQt4.Qwt5 as Qwt
from numpy import empty, ones, linspace, polyval, append, insert, delete, reshape, fromstring
from pmn.Plotter import Plotter
from scipy.interpolate import lagrange

class Lagrange(Plotter):
    """Creates a Lagrange plotting
    """
    def __init__(self, *args):
        # Initialize some local variables
        self.__SIZE = 7
        self.__editable = False
        self.movingPoint = None
        self.pointX = empty(0)
        self.pointY = empty(0)
        self.markers = []
        self.dataX = None
        self.dataY = None
        self.__lagrangeUpdate()
        self.symbol = Qwt.QwtSymbol(Qwt.QwtSymbol.Ellipse, Qt.QBrush(Qt.Qt.gray, Qt.Qt.SolidPattern), Qt.QPen(Qt.Qt.blue, 1, Qt.Qt.SolidLine, Qt.Qt.RoundCap, Qt.Qt.RoundJoin), Qt.QSize(self.__SIZE, self.__SIZE))
        # Call parent constructor
        Plotter.__init__(self, *args)
        self.curve.setPen(Qt.QPen(Qt.Qt.red, 2))
        # Connect signals
        QtCore.QObject.connect(self.plot, QtCore.SIGNAL("mousePressed"), self.mousePressed)
        QtCore.QObject.connect(self.plot, QtCore.SIGNAL("mouseReleased"), self.mouseReleased)
        QtCore.QObject.connect(self.plot, QtCore.SIGNAL("mouseMove"), self.mouseMove)

    # __init__()

    def __del__(self, *args):
        Plotter.__del__(self, *args)

        for marker in self.markers:
            marker.detach()
            del marker
        self.markers = []

    # __del__()

    def destroy(self, *args):
        Plotter.destroy(self, *args)
        QtCore.QObject.disconnect(self.plot, QtCore.SIGNAL("mousePressed"), self.mousePressed)
        QtCore.QObject.disconnect(self.plot, QtCore.SIGNAL("mouseReleased"), self.mouseReleased)
        QtCore.QObject.disconnect(self.plot, QtCore.SIGNAL("mouseMove"), self.mouseMove)

    # destroy()

    def __lagrangeUpdate(self):
        if len(self.pointX) > 0:
            self.lagrange = lagrange(self.pointX, self.pointY)
        else:
            self.lagrange = None
            self.__strfy = None

    # __lagrangeUpdate()

    def __genString(self):
        pointX = self.pointX
        pointY = self.pointY
        n = len(pointX)

        precalc = ones(n)
        for i in xrange(n):
            for j in xrange(n):
                if j != i:
                    precalc[i] *= pointX[i] - pointX[j]
            precalc[i] = pointY[i] / precalc[i]

        self.__strfy = ["(%s)" % ''.join("%+g/(x%+g)" % (precalc[i], -pointX[i]) for i in xrange(n))]

        append = self.__strfy.append
        for i in xrange(n):
            append("(x%+g)" % -pointX[i])

        self.__strfy = '*'.join(self.__strfy)

    # toString()

    def toString(self):
        if self.lagrange is None:
            return None
        elif len(self.pointX) == 1:
            return str(self.pointY[0])
        elif self.__strfy is None:
            self.__genString()

        return self.__strfy

    def update(self):
        #print 'self.lagrange', self.toString(), '\n', self.lagrange
        if self.lagrange is None:
            self.curve.setData([], [])
            self.dataX, self.dataY = None, None
        else:
            x = linspace(self.minX, self.maxX, self.ppc())
            y = polyval(self.lagrange, x)
            self.curve.setData(x, y)
            self.dataX, self.dataY = x, y

    # update()

    def overPoint(self, event):
        smX, smY = self.canvasMap(Qwt.QwtPlot.xBottom), self.canvasMap(Qwt.QwtPlot.yLeft)
        dx, dy = smX.invTransform(self.__SIZE) - smX.invTransform(0), smY.invTransform(self.__SIZE) - smY.invTransform(0)
        x, y = smX.invTransform(event.x()), smY.invTransform(event.y())

        for i in xrange(len(self.markers)):
            if self.markers[i].boundingRect().adjusted(-dx, -dy, dx, dy).contains(x, y):
                return i

        return None

    # overPoint()

    def mousePressed(self, event):
        if event.button() != Qt.Qt.LeftButton:
            return

        self.movingPoint = movingPoint = self.overPoint(event)

        if movingPoint is not None:
            self.__pos = self.pointX[movingPoint], self.pointY[movingPoint]
            self.plot.setMovable(False)
            self.__editable = False

    # mousePressed()

    def mouseReleased(self, event):
        if event.button() != Qt.Qt.LeftButton:
            return

        if self.movingPoint is not None:
            QtCore.QObject.emit(self, QtCore.SIGNAL("dataChanged"), self.pointSet, self.__pos, self.movingPoint)
            self.plot.setMovable()
            self.__editable = True
            self.movingPoint = None

    # mouseReleased()

    def mouseMove(self, event):
        '''if bool(event.buttons() & Qt.Qt.LeftButton):
            return'''

        if self.movingPoint is None:
            return

        x = self.canvasMap(Qwt.QwtPlot.xBottom).invTransform(event.x())
        y = self.canvasMap(Qwt.QwtPlot.yLeft).invTransform(event.y())

        self.pointSet((x, y), self.movingPoint, True)

    # mouseReleased()

    def mouseClick(self, event):
        if not self.__editable:
            return None

        i = self.overPoint(event)

        if i is None:
            if event.button() == Qt.Qt.LeftButton:
                x = self.canvasMap(Qwt.QwtPlot.xBottom).invTransform(event.x())
                y = self.canvasMap(Qwt.QwtPlot.yLeft).invTransform(event.y())
                self.pointAdd((x, y))

        elif event.button() == Qt.Qt.RightButton:
            self.pointDelete(i)

    # mouseClick()

    def __createMarker(self, x, y, point=None):
        marker = Qwt.QwtPlotMarker()
        marker.setSymbol(self.symbol)
        marker.setValue(x, y)
        marker.attach(self.plot)
        if point is None:
            self.markers.append(marker)
        else:
            self.markers.insert(point, marker)

    # __createMarker()

    def pointAdd(self, pos, point=None):
        if pos is None:
            return None

        x, y = pos
        if x is None or y is None:
            return None

        # TODO: rewrite without append (may be insert too)
        if point is None:
            point = len(self.pointX)
            self.pointX = append(self.pointX, x)
            self.pointY = append(self.pointY, y)
        else:
            self.pointX = insert(self.pointX, point, x)
            self.pointY = insert(self.pointY, point, y)
        self.__lagrangeUpdate()

        self.__createMarker(x, y, point)

        self.update()
        QtCore.QObject.emit(self, QtCore.SIGNAL("dataChanged"), self.pointDelete, point)
        self.plot.replot()

    # pointAdd()

    def pointDelete(self, point):
        if point is None:
            return None

        pos = self.pointX[point], self.pointY[point]
        self.pointX = delete(self.pointX, point)
        self.pointY = delete(self.pointY, point)
        self.__lagrangeUpdate()

        marker = self.markers.pop(point)
        marker.detach()
        del marker

        self.update()
        QtCore.QObject.emit(self, QtCore.SIGNAL("dataChanged"), self.pointAdd, pos, point)
        self.plot.replot()

    # pointDelete()

    def pointSet(self, pos, point, move=False):
        x, y = pos
        if point is None or x is None or y is None:
            return None

        posPrev = self.pointX[point], self.pointY[point]
        if pos == posPrev:
            return None

        self.pointX[point] = x
        self.pointY[point] = y
        self.markers[point].setValue(x, y)

        self.__lagrangeUpdate()
        self.update()
        if move:
            QtCore.QObject.emit(self, QtCore.SIGNAL("dataChanged"))
        else:
            QtCore.QObject.emit(self, QtCore.SIGNAL("dataChanged"), self.pointSet, posPrev, point)
        self.plot.replot()

        return posPrev

    # pointSet()

    def count(self):
        return len(self.pointX)

    # count()

    def setEditing(self, b=True):
        self.__editable = not not b

    # setEditing()

    def isEditing(self):
        return self.__editable

    # isEditing()

    def serialize(self):
        return reshape(append(self.pointX, self.pointY), (2, -1)).tostring()

    # serialize()

    def unserialize(self, data):
        self.pointX, self.pointY = reshape(fromstring(data), (2, -1))
        for marker in self.markers:
            marker.detach()
            del marker
        self.markers = []
        for i in xrange(len(self.pointX)):
            self.__createMarker(self.pointX[i], self.pointY[i])
        self.__lagrangeUpdate()
        self.replot()

        return self

    # unserialize()

# class Lagrange

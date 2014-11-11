# -*- mode: python -*-
# -*- coding: utf-8 -*-

from PyQt4 import Qt
from PyQt4 import QtCore
import PyQt4.Qwt5 as Qwt


class CartesianAxis(Qwt.QwtPlotItem):
    """Supports a coordinate system similar to 
    http://en.wikipedia.org/wiki/Image:Cartesian-coordinate-system.svg
    """

    def __init__(self, masterAxis, slaveAxis):
        """Valid input values for masterAxis and slaveAxis are QwtPlot.yLeft,
        QwtPlot.yRight, QwtPlot.xBottom, and QwtPlot.xTop. When masterAxis is
        an x-axis, slaveAxis must be an y-axis; and vice versa.
        """
        Qwt.QwtPlotItem.__init__(self)
        self.__axis = masterAxis
        if masterAxis in (Qwt.QwtPlot.yLeft, Qwt.QwtPlot.yRight):
            self.setAxis(slaveAxis, masterAxis)
        else:
            self.setAxis(masterAxis, slaveAxis)
        self.scaleDraw = Qwt.QwtScaleDraw()
        self.scaleDraw.setAlignment((Qwt.QwtScaleDraw.LeftScale,
                                     Qwt.QwtScaleDraw.RightScale,
                                     Qwt.QwtScaleDraw.BottomScale,
                                     Qwt.QwtScaleDraw.TopScale)[masterAxis])

    # __init__()

    def draw(self, painter, xMap, yMap, rect):
        """Draw an axis on the plot canvas
        """
        if self.__axis in (Qwt.QwtPlot.yLeft, Qwt.QwtPlot.yRight):
            self.scaleDraw.move(round(xMap.xTransform(0.0)), yMap.p2())
            self.scaleDraw.setLength(yMap.p1() - yMap.p2())
        elif self.__axis in (Qwt.QwtPlot.xBottom, Qwt.QwtPlot.xTop):
            self.scaleDraw.move(xMap.p1(), round(yMap.xTransform(0.0)))
            self.scaleDraw.setLength(xMap.p2() - xMap.p1())
        self.scaleDraw.setScaleDiv(self.plot().axisScaleDiv(self.__axis))
        self.scaleDraw.draw(painter, self.plot().palette())

    # draw()

# class CartesianAxis


class CartesianPlot(Qwt.QwtPlot):
    """Creates a coordinate system similar system 
    http://en.wikipedia.org/wiki/Image:Cartesian-coordinate-system.svg
    """

    def __init__(self, *args):
        Qwt.QwtPlot.__init__(self, *args)
        # create a plot with a white canvas
        self.setCanvasBackground(Qt.Qt.white)
        # set plot layout
        self.plotLayout().setMargin(0)
        self.plotLayout().setCanvasMargin(0)
        self.plotLayout().setAlignCanvasToScales(True)
        # attach a grid
        grid = Qwt.QwtPlotGrid()
        grid.attach(self)
        grid.setPen(Qt.QPen(Qt.Qt.black, 0, Qt.Qt.DotLine))
        # attach a x-axis
        xaxis = CartesianAxis(Qwt.QwtPlot.xBottom, Qwt.QwtPlot.yLeft)
        xaxis.attach(self)
        self.enableAxis(Qwt.QwtPlot.xBottom, False)
        # attach a y-axis
        yaxis = CartesianAxis(Qwt.QwtPlot.yLeft, Qwt.QwtPlot.xBottom)
        yaxis.attach(self)
        self.enableAxis(Qwt.QwtPlot.yLeft, False)
        # set default grid bounds
        self.setAxisScale(Qwt.QwtPlot.xBottom, -10, 10)
        self.setAxisScale(Qwt.QwtPlot.yLeft, -10, 10)
        self.replot()
        # enable drawing hint for qwt
        self.canvas().setPaintAttribute(True, Qwt.QwtPlotCurve.ClipPolygons)
        # attach eventFilter
        self.installEventFilter(self)
        # initialize local variables
        self.__movable = True

    # __init__()

    def eventFilter(self, watched, event):
        if event.type() == Qt.QEvent.MouseButtonPress:
            if event.button() == Qt.Qt.LeftButton:
                self.pressedLMBPos = self.lastLMBPos = event.pos()
            elif event.button() == Qt.Qt.RightButton:
                self.pressedRMBPos = self.lastRMBPos = event.pos()
            QtCore.QObject.emit(self, QtCore.SIGNAL("mousePressed"), event)
        elif event.type() == Qt.QEvent.MouseMove:
            QtCore.QObject.emit(self, QtCore.SIGNAL("mouseMove"), event)
            if event.buttons() == Qt.Qt.LeftButton and self.__movable:
                self.moveBy(event.pos() - self.lastLMBPos)
                self.lastLMBPos = event.pos()
            elif event.buttons() == Qt.Qt.RightButton:
                offset = event.pos() - self.lastRMBPos
                self.zoomBy(offset.x() * 0.02, offset.y() * 0.02)
                self.lastRMBPos = event.pos()
        elif event.type() == Qt.QEvent.MouseButtonRelease:
            QtCore.QObject.emit(self, QtCore.SIGNAL("mouseReleased"), event)
            if event.button() == Qt.Qt.LeftButton and self.pressedLMBPos == event.pos() or event.button() == Qt.Qt.RightButton and self.pressedRMBPos == event.pos():
                QtCore.QObject.emit(self, QtCore.SIGNAL("mouseClick"), event)
            return True
        elif event.type() == Qt.QEvent.Wheel:
            self.zoomBy(event.delta() / 120.0)

        return False
        #return QtCore.QObject.eventFilter(self, object, event)
        #return super(CartesianPlot, self).eventFilter(object, event)

    # eventFilter()

    def getBounds(self):
        # return minX, maxX, minY, maxY
        smX = self.canvasMap(Qwt.QwtPlot.xBottom)
        smY = self.canvasMap(Qwt.QwtPlot.yLeft)
        return smX.s1(), smX.s2(), smY.s1(), smY.s2()

    # getBounds()

    def moveBy(self, offset):
        minX, maxX, minY, maxY = self.getBounds()

        offsetX = (minX - maxX) / self.width() * offset.x()
        offsetY = (maxY - minY) / self.height() * offset.y()

        minX, maxX, minY, maxY = minX + offsetX, maxX + offsetX, minY + offsetY, maxY + offsetY

        self.setAxisScale(Qwt.QwtPlot.xBottom, minX, maxX)
        self.setAxisScale(Qwt.QwtPlot.yLeft, minY, maxY)

        QtCore.QObject.emit(self, QtCore.SIGNAL("changedBounds"), minX, maxX, minY, maxY)

        self.replot()

    # moveBy()

    def rescale(self, factor):
        if factor == 1.0 or factor == 0.0:
            return

        doReplot = False

        autoReplot = self.autoReplot()
        self.setAutoReplot(False)

        for axisId in xrange(self.axisCnt):
            scaleDiv = self.axisScaleDiv(axisId)
            #if isAxisEnabled(axisId) and scaleDiv.isValid():
            if scaleDiv.isValid():
                center = scaleDiv.lowerBound() + scaleDiv.range() / 2
                width_2 = scaleDiv.range() / 2 * factor
       
                self.setAxisScale(axisId, center - width_2, center + width_2)
                doReplot = True

        self.setAutoReplot(autoReplot)

        if doReplot:
            self.replot()


    def zoomBy(self, factorX, factorY=None):
        factorX = 0.9**factorX
        if factorY is None:
            factorY = factorX
        else:
            factorY = 0.9**factorY

        doReplot = False
        factor = [factorY] * 2 + [factorX] * 2
        for axisId in xrange(self.axisCnt):
            scaleDiv = self.axisScaleDiv(axisId)
            if scaleDiv.isValid():
                center = scaleDiv.lowerBound() + scaleDiv.range() / 2
                width_2 = scaleDiv.range() / 2 * factor[axisId]

                self.setAxisScale(axisId, center - width_2, center + width_2)
                doReplot = True

        if doReplot:
            # i know, thats bad, bad
            self.replot()

            QtCore.QObject.emit(self, QtCore.SIGNAL("changedBounds"), *self.getBounds())

            self.replot()

    # zoomBy()

    def setMovable(self, b=True):
        self.__movable = bool(b)

    # setMovable()

    def isMovable(self):
        return self.__movable

    # isMovable()

    def closeEvent(self, event):
        print 'closing!!!'
        event.accept()

    # closeEvent()

    def resizeEvent(self, event):
        Qwt.QwtPlot.resizeEvent(self, event)
        #size = event.size()
        #size.width(), size.height()
        QtCore.QObject.emit(self, QtCore.SIGNAL("changedBounds"), *self.getBounds())

        self.replot()

    # resizeEvent()

# class CartesianPlot

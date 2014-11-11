# -*- mode: python -*-
# -*- coding: utf-8 -*-

from PyQt4 import Qt
from PyQt4 import QtCore
from numpy import pi, e, linspace
from numexpr import evaluate
from pmn.Plotter import Plotter

"""Supported functions

 ['sin', 'cos', 'exp', 'log',
  'expm1', 'log1p',
  'pow', 'div',
  'sqrt', 'inv',
  'sinh', 'cosh', 'tanh',
  'arcsin', 'arccos', 'arctan',
  'arccosh', 'arcsinh', 'arctanh',
  'arctan2', 'abs']:
"""

class EvalPlot(Plotter):
    """Creates a EvalPlot plotting
    """
    def __init__(self, plot, func=None):
        # Initialize some local variables
        self.dataX = None
        self.dataY = None
        self.__expr = None
        # Call parent init function
        Plotter.__init__(self, plot)
        self.curve.setPen(Qt.QPen(Qt.Qt.black, 2))
        # Init
        self.__setExpression(func)

    # __init__()
    
    def update(self):
        if self.__expr is None:
            self.curve.setData([], [])
            self.dataX, self.dataY = None, None
        else:
            x = linspace(self.minX, self.maxX, self.ppc())
            y = evaluate(self.__expr)
            if y is None:
                raise Exception("Unknown eval problem", y, self.__expr)
            else:
                self.dataX, self.dataY = x, y
                self.curve.setData(x, y)

    # update()

    def __setExpression(self, expr):
        if expr is None or len(expr) == 0:
            self.__expr = None
        else:
            self.__expr = str(expr).replace("^","**")
        self.update()

    # __setExpression()

    def setExpression(self, s):
        print self.__class__.__name__, 'setExpression', s
        past = self.__expr
        self.__setExpression(s)
        QtCore.QObject.emit(self, QtCore.SIGNAL("dataChanged"), self.setExpression, past)
        self.plot.replot()

    # setExpression()

    def getExpression(self):
        print self.__class__.__name__, 'getExpression', self.__expr
        return self.__expr

    # getExpression()

    def serialize(self):
        return self.getExpression()

    # serialize()

    def unserialize(self, data):
        print self.__class__.__name__, 'unserialize', data
        self.__setExpression(data)
        self.plot.replot()

        return self

    # unserialize()

# class EvalPlot

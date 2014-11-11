from numpy import zeros, ones, linspace, polyval, prod, sin
from time import time
from random import random
from scipy.interpolate import lagrange

class test0:
    def __init__(self, pointX, pointY):
        self.lagrange = lagrange(pointX, pointY)

    def compute(self, x):
        return polyval(self.lagrange, x)


class test1:
    def __init__(self, pointX, pointY):
        n = len(pointX)

        if n == 1:
            return lambda x: pointY[0]

        precalc = ones(n)
        for i in xrange(n):
            for j in xrange(n):
                if j != i:
                    precalc[i] *= pointX[i] - pointX[j]
            precalc[i] = pointY[i] / precalc[i]

        def preprod(x):
            ret = zeros(n)
            for j in xrange(n):
                ret[j] = x - pointX[j]
            return prod(ret)

        self.lagrange = lambda x: sum(precalc[i] / (x - pointX[i]) for i in xrange(n)) * preprod(x)

    def compute(self, x):
        return map(self.lagrange, x.copy())

class test2:
    def __init__(self, pointX, pointY):
        n = len(pointX)

        if n == 1:
            self.precalc = ones(n) * pointY[0]
            return

        precalc = ones(n)
        for i in xrange(n):
            for j in xrange(n):
                if j != i:
                    precalc[i] *= pointX[i] - pointX[j]
            precalc[i] = pointY[i] / precalc[i]

        self.precalc = precalc
        self.pointX = pointX

    def compute(self, x):
        n = len(x)
        y = zeros(n)
        pointX = self.pointX
        precalc = self.precalc
        nodes = len(pointX)

        for i in xrange(n):
            ret = zeros(n)
            for j in xrange(nodes):
                ret[j] = x[i] - pointX[j]
            y[i] = sum(precalc[k] / (x[i] - pointX[k]) for k in xrange(nodes)) * prod(ret)

        return y

def profile(cls, runs=10, computes=10, *args):
    ret = []
    append = ret.append
    x = linspace(-10, 10, 800)
    for i in xrange(runs):
        t = time()
        l = cls(*args)
        for j in xrange(computes):
            p = l.compute(x)
            #print sum(p)
        del l
        l = None
        append(time() - t)
    return min(ret), max(ret), sum(ret), sum(p)

if __name__ == '__main__':
    tests = [test0, test1, test2]
    n = 20
    dataX = zeros(n)
    dataY = zeros(n)
    x = linspace(0, 1, n)
    for i in xrange(n):
        dataX[i] = x[i]
        dataY[i] = sin(x[i])

    for runs in [3]:
        for computes in [1, 10, 25]:
            print '-'.join([''] * 80)
            print '%d runs, %d computes' % (runs, computes)
            for test in tests:
                print test.__name__, "\t%.10g\t%.10g\t%.10g\t%g" % profile(test, runs, computes, dataX, dataY)


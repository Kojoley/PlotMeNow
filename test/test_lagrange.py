import numpy as np

from PyQt4.Qwt5.anynumpy import *
import time, random
from scipy.interpolate import lagrange

def example1(samples):
        X = 0 # the tuple index of the X variable in the samples
        Y = 1 # the tuple index of the Y variable in the samples
        n = len(samples)
    
        precalc = ones(n)
        for i in xrange(n):
            for j in xrange(n):
                if j != i:
                    precalc[i] *= samples[i][X] - samples[j][X]

        def boost(x):
            ret = 1.0
            for j in xrange(n):
                ret *= x - samples[j][X]
            return ret

        return lambda x: sum(precalc[i] / (x - samples[i][X]) for i in xrange(n)) * boost(x)

def exampl12(dataX, dataY, n):
        precalc = ones(n)
        for i in xrange(n):
            for j in xrange(n):
                if j != i:
                    precalc[i] *= dataX[i] - dataX[j]

        def boost(x):
            ret = 1.0
            for j in xrange(n):
                ret *= x - dataX[j]
            return ret

        return lambda x: sum(precalc[i] / (x - dataX[i]) for i in xrange(n)) * boost(x)

def exampl13(dataX, dataY):
        p = lagrange(dataX, dataY)
        return lambda x: polyval(p, x)

def example2(samples):
        X = 0 # the tuple index of the X variable in the samples
        Y = 1 # the tuple index of the Y variable in the samples
        n = len(samples)
    
        precalc = ones(n)
        for i in xrange(n):
            for j in xrange(n):
                if j != i:
                    precalc[i] *= samples[i][X] - samples[j][X]

        def boost(x):
            ret = zeros(n)
            for j in xrange(n):
                ret[j] = x - samples[j][X]
            return prod(ret)

        return lambda x: sum(precalc[i] / (x - samples[i][X]) for i in xrange(n)) * boost(x)

def example3(samples):
        X = 0 # the tuple index of the X variable in the samples
        Y = 1 # the tuple index of the Y variable in the samples
        n = len(samples)
    
        precalc = ones(n)
        for i in xrange(n):
            for j in xrange(n):
                if j != i:
                    precalc[i] *= samples[i][X] - samples[j][X]

        return lambda x: sum(precalc[i] / (x - samples[i][X]) for i in xrange(n)) * prod([x - samples[j][X] for j in xrange(n)])

def example4(samples):
        X = 0 # the tuple index of the X variable in the samples
        Y = 1 # the tuple index of the Y variable in the samples
        n = len(samples)

        precalc = ones(n)
        for i in xrange(n):
            arr = []
            append = arr.append
            for j in xrange(n):
                if j != i:
                    append(samples[i][X] - samples[j][X])
            precalc[i] = prod(arr)

        def boost(x):
            ret = []
            append = ret.append
            for j in xrange(n):
                append(x - samples[j][X])
            return prod(ret)

        return lambda x: sum(precalc[i] / (x - samples[i][X]) for i in xrange(n)) * boost(x)

def profile(f, n=1000, *args):
    tick = time.time
    ret = []
    append = ret.append
    x = linspace(-10, 10, 800)
    for i in xrange(n):
        t = tick()
        p = f(*args)
        for j in x:
            p(j)
        append(tick() - t)
    return min(ret), max(ret), sum(ret)

if __name__ == '__main__':
    runs = 10
    n = 20
    dataX = zeros(n)
    dataY = zeros(n)
    points = []
    for i in linspace(-10, 10, n):
        x, y = i-random.random(), random.random()
        points.append((x, y))
        dataX[i] = x
        dataY[i] = y
    print "example1(): %.10g\t%.10g\t%.10g" % profile(example1, runs, points)
    print "exampl12(): %.10g\t%.10g\t%.10g" % profile(exampl12, runs, dataX, dataY, n)
    #print "exampl13(): %.10g\t%.10g\t%.10g" % profile(exampl13, runs, dataX, dataY)
    print "example2(): %.10g\t%.10g\t%.10g" % profile(example2, runs, points)
    print "example3(): %.10g\t%.10g\t%.10g" % profile(example3, runs, points)
    print "example4(): %.10g\t%.10g\t%.10g" % profile(example4, runs, points)

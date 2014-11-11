import numpy as np
from numpy import linspace
from time import time
from random import random

def mysum(data):
    ret = 0.0
    for i in data:
        ret += i
    return ret

def profile(f, runs=10, *args):
    ret = []
    append = ret.append
    x = linspace(-10, 10, 800)
    start = time()
    for i in xrange(runs):
        t = time()
        p = f(*args)
        l = None
        append(time() - t)
    end = time()

    return min(ret), max(ret), sum(ret), end - start, p

if __name__ == '__main__':
    tests = [np.sum, sum, mysum]
    n = 10**6
    data = linspace(-999999, 1000000, n)

    #for runs in [10**3, 10**4, 10**5]:
    for runs in [1]:
        print '-'.join([''] * 80)
        print '%d runs' % runs
        for test in tests:
            print test.__name__, "\t%.10g\t%.10g\t%.10g\t%.10g\t%g" % profile(test, runs, data)


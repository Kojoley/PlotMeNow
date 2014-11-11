#!/usr/bin/env python

import sys
from PyQt4 import Qt
from PyQt4 import QtCore, QtGui
import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5.anynumpy import *

# some extra maths functions
def fac(x):
	if type(x) != int or x < 0:
		raise ValueError
	if x==0:
		return 1
	for n in arange(2,x):
		x = x*n
	return x

# create a safe namespace for the eval()s in the graph drawing code
def sub_dict(somedict, somekeys, default=None):
	return dict([ (k, somedict.get(k, default)) for k in somekeys ])
# a list of the functions from math that we want.
safe_list = ['math', 'abs', 'log', 'log10', 'acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'sinc']
safe_dict = sub_dict(locals(), safe_list)
#safe_dict['fac'] = lambda x: map(lambda y: fac(y), x)

plot_str = "cos(-x**2)"

if __name__ == '__main__':
    safe_dict['x'] = 2.0
    compile_y = compile(plot_str, "", 'eval')
    y = eval(compile_y, {"__builtins__":{}}, safe_dict)
    print 'Pretest', y
    for i in safe_list:
      if not i in ['math', 'abs', 'acos', 'asin', 'atan', 'atan2', 'e', 'fmod', 'hypot', 'ldexp', 'pi', 'pow']:
        eval_str = '%s(x)' % i
        print 'Trying', eval_str
        compile_y = compile(eval_str, "", 'eval')
        y = eval(compile_y, {"__builtins__":{}}, safe_dict)
    a = 2
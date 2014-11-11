import numpy as np
import numexpr as ne

a = np.array([2,4])
print a
print ne.evaluate('a ** -2')

a = np.array([2,4], dtype='float')
print a
print ne.evaluate('a ** -2')

a = np.array([2,4])
print a
print ne.evaluate('a ** -2')


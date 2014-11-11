import numpy as np

if __name__ == '__main__':
	a = np.array([1,2,3])
	b = np.array([9,8,7])
	ab = np.append(a, b)
	print a
	print b
	print ab
        print 'reshape', np.reshape(ab, (2, -1)) #.tostring()
	print 'ndarray', np.ndarray((2,), buffer=ab)
from numpy import *

if __name__ == '__main__':
	data = empty(0)
	for i in xrange(5):
		data = append(data, i)
	print data

	data = delete(data, 2)
	print data

	data = insert(data, 2, 9)
	print data
	print len(data)

	print data[2:]
	print data[:2]
	print data[0:2]

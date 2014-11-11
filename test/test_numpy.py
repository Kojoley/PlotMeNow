import numpy as np

if __name__ == '__main__':

    a = np.empty([2, 0])
    print a
    a = np.insert(a, 0, (2, 3), axis=1)
    print a
    a = np.insert(a, 0, (2, 3), axis=1)
    print a
    a = np.insert(a, 0, [8, 9], axis=1)
    print a


    a = np.empty([2, 0])
    print a
    a = np.append(a, [2, 3], axis=1)
    print a
    a = np.append(a, [8, 9], axis=1)
    print a

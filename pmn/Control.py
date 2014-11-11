# -*- mode: python -*-
# -*- coding: utf-8 -*-

from PyQt4 import QtCore
import pmn
import json
import base64

class PlotControl(QtCore.QObject):
    """ Control curve, plot for changes
        Provide undo and redo functionality
    """
    def __init__(self, plot, undoSlot=None, redoSlot=None):
        self.__plot = plot
        self.__actions = []
        self.__current = -1
        self.__internal = False
        self.__changed = False
        self.__undo = undoSlot
        self.__redo = redoSlot
        self.__fileName = None
        self.__obj = []
        self.__update(False, False)

        QtCore.QObject.__init__(self)

    # __init__()

    def create(self, className, *args):
        """
rgb(0, 119, 204)
rgb(0, 170, 0)
rgb(240, 0, 240)
rgb(255, 136, 0)
rgb(136, 0, 136)
rgb(0, 136, 136)
rgb(136, 136, 0)
        """
        #obj = pmn[className](self.__plot, args)
        obj = getattr(pmn, className)(self.__plot, *args)
        self.attach(obj)
        return obj

    # create()

    def attach(self, obj):
        QtCore.QObject.connect(obj, QtCore.SIGNAL("dataChanged"), self.__storeAction)
        self.__obj.append(obj)

    # attach()

    def detach(self, obj):
        QtCore.QObject.disconnect(obj, QtCore.SIGNAL("dataChanged"), self.__storeAction)
        if obj in self.__obj:
            self.__obj.pop(self.__obj.index(obj))

    # detach()

    """
    def qwe(self, x, y):
        print x, y
        return x and y

    def isActEq(self, a, b):
        q = reduce(lambda x, y: x and y, [a[i] == b[i] for i in xrange(2)], True)
        print 'eq', q
        #print 'eq', a[0] == b[0], a[1] == b[1]
        return q
    """
    # isActEq()

    def __storeAction(self, *args):
        #print 'dataChanged', self.sender().__class__.__name__
        if args is None or len(args) == 0:
            return

        func = args[0]
        if func is None:
            return

        act = (self.sender(), func, args[1:])
        if self.__internal: # or len(self.__actions) > 0 and self.isActEq(act, self.__actions[self.__current]):
            print 'storeAction %d/%d [Upd] %s.%s%s' % (self.__current, len(self.__actions), act[0].__class__.__name__, act[1].__name__, act[2])
            # update history entry
            self.__actions[self.__current] = act
        else:
            # new history entry
            self.__current += 1
            del self.__actions[self.__current:]
            self.__actions.append(act)

            print 'storeAction %d/%d [New] %s.%s%s' % (self.__current, len(self.__actions), act[0].__class__.__name__, act[1].__name__, act[2])

            self.__update(True, False)	# can undo but no redo

        self.__changed = True

    # __storeAction()

    def __applyAction(self, i):
        obj, func, args = self.__actions[i]
        print 'applyAction %d/%d %s.%s%s' % (i, len(self.__actions), obj.__class__.__name__, func.__name__, args)
        self.__internal = True
        func(*args)
        self.__internal = False

    # __applyAction()

    def undo(self):
        print 'try Undo'
        if self.__canUndo:
            print 'perform Undo'
            self.__applyAction(self.__current)
            self.__current -= 1
            self.__update(self.__current >= 0, True)	# can redo

            return True

        return False

    # undo()

    def redo(self):
        print 'try Redo'
        if self.__canRedo:
            print 'perform Redo'
            self.__current += 1
            self.__applyAction(self.__current)
            self.__update(True, self.__current + 1 < len(self.__actions))	# can undo

            return True

        return False

    # redo()

    def __update(self, undo, redo):
        self.__canUndo = undo
        self.__canRedo = redo
        if self.__undo is not None:
            self.__undo(undo)
        if self.__redo is not None:
            self.__redo(redo)

    # __update()

    def historyDelete(self):
        self.__actions = []
        self.__update(False, False)	# no undo and redo

    # historyDelete()

    def new(self, fileName=None):
        print 'Control.new(+) elems=%s' % self.__obj
        self.__changed = False
        self.__fileName = fileName

        # delete attached objects
        for obj in self.__obj:
            self.detach(obj)
            obj.destroy()
            del obj
            obj = None
        self.__obj = []

        self.historyDelete()

        print 'Control.new(-) elems=%s' % self.__obj

        return True

    # new()

    def save(self, fileName=None):
        print 'Control.save(+) fileName=%s elems=%s' % (fileName, self.__obj)
        if fileName is None:
            if not self.onDisk():
                return False
        else:
            self.__fileName = fileName

        objs = [{'VERSION': '1'}]
        for obj in self.__obj:
            objs.append((obj.__class__.__name__, base64.b64encode(obj.serialize())))

        with open(self.__fileName, 'w') as f:
            f.write(json.dumps(objs))

        self.__changed = False

        print 'Control.save(-) fileName=%s elems=%s' % (fileName, self.__obj)

        return True

    # save()

    def load(self, fileName):
        print 'Control.load(+) fileName=%s elems=%s' % (fileName, self.__obj)
        if fileName is None:
            return False

        self.new(fileName)

        with open(fileName, 'r') as f:
            objs = json.loads("\n".join(f.readlines()))
        info = objs.pop(0)
        print info
        for className, data in objs:
            obj = self.create(className)
            data = base64.b64decode(data)
            print className, data
            obj.unserialize(data)

        self.historyDelete()

        print 'Control.load(-) fileName=%s elems=%s' % (fileName, self.__obj)

        return True

    # load()

    def isChanged(self):
        return self.__changed

    # isChanged()

    def onDisk(self):
        return self.__fileName is not None

    # onDisk()

    def getElements(self):
        return self.__obj

    # getElements()

    def getElementsByClassName(self, className):
        elems = []
        for obj in self.__obj:
            if obj.__class__.__name__ == className:
                elems.append(obj)

        return elems

    # getElementsByClassName()

# class PlotControl

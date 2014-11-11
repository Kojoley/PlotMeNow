# -*- mode: python -*-
# -*- coding: utf-8 -*-
"""
MainWindow of PlotMeNow
"""

from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import QtGui
import PyQt4.Qwt5 as Qwt
from pmn import CartesianPlot, PlotControl, Epsilon, EvalPlot, Lagrange
from report import generateReport
from helper import HelpDialog
from about import AboutDialog

class MainWindow(Qt.QMainWindow):
    def __init__(self, *args):
        Qt.QMainWindow.__init__(self, *args)

        self.resize(800, 600)
        self.setWindowTitle("PlotMeNow")

        centralWidget = QtGui.QWidget(self)
        gridLayout = QtGui.QGridLayout(centralWidget)
        gridLayout.setMargin(0)
        plot = CartesianPlot(centralWidget)
        gridLayout.addWidget(plot, 0, 0, 1, 1)
        self.setCentralWidget(centralWidget)

        def addToolBar(parent, name):
            toolBar = QtGui.QToolBar(parent)
            toolBar.setWindowTitle(name)
            parent.addToolBar(QtCore.Qt.TopToolBarArea, toolBar)
            return toolBar

        toolBar = addToolBar(self, u'Сессия')

        def genButton(name, res, *args):
            return toolBar.addAction(QtGui.QIcon(QtGui.QPixmap(":/image/%s.png" % res)), name, *args)

        def projSaveAs():
            print 'projSaveAs()', pc.isChanged()
            fileName = QtGui.QFileDialog.getSaveFileName(self, u'Сохранить сессию', '.', 'PlotMeNow (*.pmn)')
            if not fileName.isNull():
                return pc.save(unicode(fileName))

            return False

        def projSave():
            print 'projSave()', pc.isChanged()
            if not pc.onDisk():
                return projSaveAs()

            return pc.save()

        def projNew():
            print 'projNew()', pc.isChanged()
            if pc.isChanged():
                reply = QtGui.QMessageBox.question(self, u'Несохраненные изменения', u'Сохранить текущую сессию?', QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)
                if reply == QtGui.QMessageBox.Save:
                    projSave()
                elif reply == QtGui.QMessageBox.Cancel:
                    return

            self.e.setAB(None, None)
            print '1', pc.getElements()
            ret = pc.new()
            print '2', pc.getElements()
            if ret:
                for i in xrange(comboBoxF.count()):
                    comboBoxF.setItemData(i, None)
                print '3', pc.getElements()
                print 'comboBoxF.clear()'
                comboBoxF.clear()

                print '4', pc.getElements()
                self.l.destroy()
                del self.l
                self.l = None

                print '5', pc.getElements()
                self.l = pc.create(Lagrange.__name__)
                self.l.setEditing()
                print '6', pc.getElements()
                self.e.setAB(None, self.l)
                print 'Control elems', pc.getElements()

                self.e.reconnect()
                self.e.setB(self.l)

                plot.replot()
            else:
                if comboBoxF.count() > 0:
                    index = comboBoxF.currentIndex()
                    obj = comboBoxF.itemData(index).toPyObject()
                    self.e.setAB(obj, self.l)

            return ret

        def projOpen():
            print 'projOpen()', pc.isChanged()
            fileName = QtGui.QFileDialog.getOpenFileName(self, u'Открыть сессию', '.', 'PlotMeNow (*.pmn)')
            if not fileName.isNull():
                if pc.isChanged() and QtGui.QMessageBox.Save == QtGui.QMessageBox.question(self, u'Несохраненные изменения', u'Сохранить текущую сессию?', QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard, QtGui.QMessageBox.Save):
                    projSave()
                #return pc.load(unicode(fileName))

                self.e.setAB(None, None)
                print '1', pc.getElements()
                ret = pc.load(unicode(fileName))
                print '2', pc.getElements()
                if ret:
                    """
                    self.l.destroy()
                    self.ep.destroy()
                    pc.detach(self.l)
                    pc.detach(self.ep)
                    del self.l
                    del self.ep
                    self.l = None
                    self.ep = None
                    self.l = pc.getElementsByClassName(Lagrange.__name__).pop()
                    self.ep = pc.getElementsByClassName(EvalPlot.__name__).pop()
                    self.e.setAB(self.ep, self.l)
                    plot.replot()
                    """

                    """
                    for ep in pc.getElementsByClassName(EvalPlot.__name__):
                        pc.detach(ep)
                        ep.destroy()
                        del ep
                        ep = None
                    self.l.destroy()
                    pc.detach(self.l)
                    del self.l
                    self.l = None
                    """
                    self.l = pc.getElementsByClassName(Lagrange.__name__).pop()
                    print '3', pc.getElements()

                    print 'comboBoxF.clear()'
                    comboBoxF.clear()
                    print '4', pc.getElements()

                    print 'for ep in pc.getElementsByClassName(EvalPlot.__name__)'
                    for ep in pc.getElementsByClassName(EvalPlot.__name__):
                        f = ep.getExpression()
                        if f is None:
                            print 'Warning!', ep, 'has None function'
                        else:
                            comboBoxF.addItem(f, ep)
                    print '5', pc.getElements()

                if comboBoxF.count() > 0:
                    index = comboBoxF.currentIndex()
                    obj = comboBoxF.itemData(index).toPyObject()
                    self.e.setA(obj)
                self.e.reconnect()
                self.e.setB(self.l).replot()
                return ret

            return False

        projectNew = genButton(u"Новый", "new", projNew)
        projectOpen = genButton(u"Открыть", "open", projOpen)
        projectSave = genButton(u"Сохранить", "fileSave", projSave)
        projectSaveAs = genButton(u"Сохранить как", "fileSaveAs", projSaveAs)

        toolBar = addToolBar(self, u'Навигация')
        #toolBar.addSeparator()
        editUndo = genButton(u"Отменить действие", "editUndo", lambda: pc.undo())
        editRedo = genButton(u"Вернуть действие", "editRedo", lambda: pc.redo())

        toolBar = addToolBar(self, u'Выражения')
        #toolBar.addSeparator()
        comboBoxF = QtGui.QComboBox(toolBar)
        comboBoxF.setMinimumSize(QtCore.QSize(220, 0))
        #comboBoxF.addItems(['4*pi*sin(x)*cos(x)^2', 'x^2', 'e^(-x^2)'])
        comboBoxF.setEditable(True)
        comboBoxF.setIconSize(QtCore.QSize(16, 16))
        toolBar.addAction("f(x):")
        toolBar.addWidget(comboBoxF)
        #QtCore.QObject.connect(comboBoxF, QtCore.SIGNAL("editTextChanged(QString)"), lambda x: self.ep.setExpression(x))
        #QtCore.QObject.connect(comboBoxF, QtCore.SIGNAL("currentIndexChanged(QString)"), lambda x: self.ep.setExpression(x))
        #QtCore.QObject.connect(comboBoxF, QtCore.SIGNAL("currentIndexChanged(int)"), lambda i: self.e.setA(comboBoxF.itemData(i).toPyObject()).replot())
        def currentIndexChanged(index):
            print 'currentIndexChanged', index
            if index > -1:
                obj = comboBoxF.itemData(index).toPyObject()
                if obj is None:
                    obj = pc.create(EvalPlot.__name__, comboBoxF.itemText(index))
                    comboBoxF.setItemData(index, obj)
                    self.e.reconnect()
                self.e.setA(obj)
            else:
                self.e.setA(None)

            self.e.replot()
        #def editTextChanged(text):
        QtCore.QObject.connect(comboBoxF, QtCore.SIGNAL("currentIndexChanged(int)"), currentIndexChanged)
        #QtCore.QObject.connect(comboBoxF, QtCore.SIGNAL("editTextChanged(QString)"), editTextChanged)
        deleteButtonF = QtGui.QPushButton(QtGui.QIcon(QtGui.QPixmap(":/image/editDelete.png")), '', toolBar)
        deleteButtonF.setIconSize(QtCore.QSize(12, 12))
        deleteButtonF.setMaximumSize(QtCore.QSize(22, 22))
        #QtCore.QObject.connect(deleteButtonF, QtCore.SIGNAL("clicked()"), lambda: comboBoxF.removeItem(comboBoxF.currentIndex()))
        def deleteEP():
            if comboBoxF.count() == 0:
                return
            index = comboBoxF.currentIndex()
            obj = comboBoxF.itemData(index).toPyObject()
            pc.detach(obj)
            obj.destroy()
            del obj
            comboBoxF.removeItem(index)
        QtCore.QObject.connect(deleteButtonF, QtCore.SIGNAL("clicked()"), deleteEP)
        toolBar.addWidget(deleteButtonF)

        toolBar = addToolBar(self, u'Отчет')
        #toolBar.addSeparator()
        #generateReportAction = genButton(u"Составить отчет", "fileResource", lambda: generateReport(self, plot, [unicode(comboBoxF.itemText(i)) for i in xrange(comboBoxF.count())], [l]))
        generateReportAction = genButton(u"Составить отчет", "fileResource", lambda: generateReport(self, plot, pc.getElementsByClassName(EvalPlot.__name__), pc.getElementsByClassName(Lagrange.__name__)))

        toolBar = addToolBar(self, u'Справка')
        #toolBar.addSeparator()
        helpAction = genButton(u"Справка", "help", lambda: HelpDialog(self).show())
        aboutAction = genButton(u"О программе", "helpAbout", lambda: AboutDialog(self).show())

        pc = PlotControl(plot, editUndo.setEnabled, editRedo.setEnabled)

        #self.ep = EvalPlot(plot, '4*pi*sin(x)*cos(x)^2')
        self.l = Lagrange(plot)
        #self.e = Epsilon(plot, self.ep, self.l)
        self.l.setEditing()

        self.e = Epsilon(plot, None, self.l)
        func = ['4*pi*sin(x)*cos(x)^2', 'x^2', 'e^(-x^2)']
        for f in func:
            comboBoxF.addItem(f, pc.create(EvalPlot.__name__, f))
        self.e.reconnect()

        pc.attach(self.l)
        #pc.attach(self.ep)

        picker = Qwt.QwtPlotPicker(Qwt.QwtPlot.xBottom, Qwt.QwtPlot.yLeft,
                    Qwt.QwtPicker.DragSelection,
                    Qwt.QwtPlotPicker.CrossRubberBand, Qwt.QwtPicker.AlwaysOn,
                    plot.canvas())

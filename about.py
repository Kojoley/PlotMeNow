# -*- mode: python -*-
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import sys, os
import numpy
import numexpr

# Recommended minimum versions
minimum_numpy_version = "1.6"

def info():
    """Print the versions of software that numexpr relies on."""
    out = []
    if numpy.__version__ < minimum_numpy_version:
        out.append("*Warning*: NumPy version is lower than recommended: %s < %s" % \
              (numpy.__version__, minimum_numpy_version))
    out.append('Python version:    %s' % sys.version)
    out.append("NumPy version:     %s" % numpy.__version__)
    out.append("Numexpr version:   %s" % numexpr.__version__)
    if os.name == 'posix':
        (sysname, nodename, release, version, machine) = os.uname()
        out.append('Platform:          %s-%s' % (sys.platform, machine))
    out.append("AMD/Intel CPU?     %s" % numexpr.is_cpu_amd_intel)
    out.append("VML available?     %s" % numexpr.use_vml)
    if numexpr.use_vml:
        out.append("VML/MKL version:   %s" % numexpr.get_vml_version())
    out.append('Detected cores:    %s' % numexpr.ncores)

    return "<br />\n".join(out)


class AboutDialog(QtGui.QDialog):
    def __init__(self, *args):
        QtGui.QDialog.__init__(self, *args)
        self.resize(500, 500)
        self.setWindowTitle(u'О программе')
        self.gridLayout = QtGui.QGridLayout(self)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.textEdit = QtGui.QTextEdit(info(), self)
        self.textEdit.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard | QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextBrowserInteraction | QtCore.Qt.TextSelectableByKeyboard | QtCore.Qt.TextSelectableByMouse)
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)

# class AboutDialog

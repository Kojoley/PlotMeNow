#!/usr/bin/env python
# -*- mode: python -*-
# -*- coding: utf-8 -*-

import sys
from PyQt4 import Qt
from window import MainWindow

def main():
    """Entry point
    """
    app = Qt.QApplication(sys.argv)

    import res

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

    res.qCleanupResources()

if __name__ == '__main__':
    main()

# Local Variables: ***
# mode: python ***
# End: ***

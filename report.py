# -*- mode: python -*-
# -*- coding: utf-8 -*-
"""
Report generating module
"""

from PyQt4 import Qt
#import PyQt4.Qwt5 as Qwt
#from rtfng import *
from rtfng.Elements import Document, Section
from rtfng.Renderer import Renderer, TabPropertySet
from rtfng.document.paragraph import Paragraph, Table, Cell
from rtfng.object.picture import ImageFromString


def langMorph(num, morph):
    """Choose right tail for numerics
    """
    num = abs(num)

    exception = num >= 11 and num <= 15
    tail = num % 10

    if tail == 1 and not exception:
        return morph[1]
    if tail > 1 and tail < 5 and not exception:
        return morph[2]

    return morph[0]

# langMorph()

def getPlotImage(plot):
    image = Qt.QByteArray()
    buf = Qt.QBuffer(image)
    buf.open(Qt.QIODevice.WriteOnly)

    #for curve in plot.itemList():
    #    curve.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased, True)

    #size = plot.size()
    #plot.resize(size * 4)
    pixmap = Qt.QPixmap(plot.size())
    plot.render(pixmap)
    #plot.resize(size)
    #pixmap = pixmap.scaledToWidth(500, Qt.Qt.SmoothTransformation)
    pixmap = pixmap.copy(Qt.QRect(Qt.QPoint(0, 0), pixmap.size()).adjusted(2, 2, -2, -2))
    pixmap.save(buf, "PNG")

    #for curve in plot.itemList():
    #    curve.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased, False)

    return ImageFromString(image, "PNG")


def generateReport(window, plot, evals, lagranges):
    """Save session report to rtf document
    """
    fileName = Qt.QFileDialog.getSaveFileName(window, u'Сохранить отчет', '.', 'Word (*.doc)')
    if not fileName.isNull():
        doc     = Document()
        #ss      = doc.StyleSheet
        section = Section()
        doc.Sections.append(section)

        minX, maxX, minY, maxY = plot.getBounds()

        section.append(u'Полотно растеризации:')
        section.append('')
        table = Table(TabPropertySet.DEFAULT_WIDTH, \
                      TabPropertySet.DEFAULT_WIDTH * 3, \
                      TabPropertySet.DEFAULT_WIDTH * 3)
        table.AddRow(
            Cell(Paragraph(u'ось')),
            Cell(Paragraph(u'от')),
            Cell(Paragraph(u'до')))
        table.AddRow(
            Cell(Paragraph('x')),
            Cell(Paragraph(str(minX))),
            Cell(Paragraph(str(maxX))))
        table.AddRow(
            Cell(Paragraph('y')),
            Cell(Paragraph(str(minY))),
            Cell(Paragraph(str(maxY))))
        section.append(table)
        section.append(u'Детализация: %d %s на график' % (plot.width(), langMorph(plot.width(), (u'точек', u'точка', u'точки'))))

        section.append(Paragraph(getPlotImage(plot)))

        section.append('')
        section.append(u'%d %s:' % (len(evals), langMorph(len(evals), (u'функций', u'функция', u'функции'))))
        #for s in evals:
        #    section.append('f(x) = %s' % s)
        for i in evals:
            section.append('f(x) = %s' % i.getExpression())

        section.append('')
        section.append(u'%d %s Лагранжа' % (len(lagranges), langMorph(len(lagranges), (u'полиномов', u'полином', u'полинома'))))
        for i in lagranges:
            points = i.count()
            section.append(ur'\u2014' * 30)
            section.append(u'%d %s:' % (points, langMorph(points, (u'точек', u'точка', u'точки'))))
            table = Table(TabPropertySet.DEFAULT_WIDTH / 2, \
                          TabPropertySet.DEFAULT_WIDTH * 3, \
                          TabPropertySet.DEFAULT_WIDTH * 3)
            for j in xrange(points):
                table.AddRow(
                    Cell(Paragraph('%d' % j)),
                    Cell(Paragraph('%g' % i.pointX[j])),
                    Cell(Paragraph('%g' % i.pointY[j])))
            section.append(table)
            section.append(u'L(x) = %s' % i.toString())
    
        Renderer().Write(doc, file(unicode(fileName), 'w'))

# generateReport()


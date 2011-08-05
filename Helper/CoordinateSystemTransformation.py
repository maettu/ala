#!/usr/bin/python

from PyQt4.QtCore import (QPointF)

# Translates cartesian coordinates (from own coord. system)
# to item coordinates
# i.e. give it x = 2, y = 5 and receive 150,370 or something alike.
def toMainWidgetCoord(mainWidget, x, y):
    # number of items is max - min, 12 - -3 = 15 :-)
    numberXItems = mainWidget.xMax - mainWidget.xMin
    numberYItems = mainWidget.yMax - mainWidget.yMin
    
    # width / countNumber -> width of one item
    xItem = mainWidget.width / numberXItems * x
    yItem = - (mainWidget.height/ numberYItems * y)
    
    return QPointF(xItem, yItem)
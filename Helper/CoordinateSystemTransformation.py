#!/usr/bin/python

from PyQt4.QtCore import (QPointF)

# Translates cartesian coordinates (from own coord. system)
# to item coordinates
# i.e. give it x = 2, y = 5 and receive 150,370 or something alike.
def toCcsCoord(ccs, x, y):
    # number of items is max - min, 12 - -3 = 15 :-)
    numberXItems = ccs.xMax - ccs.xMin
    numberYItems = ccs.yMax - ccs.yMin
    
    # width / countNumber -> width of one item
    xItem =    ccs.width / numberXItems * x
    yItem = - (ccs.height/ numberYItems * y)
    
    return QPointF(xItem, yItem)
    
# Translates widget coordinates (back) to coordinates in
# own cartesian coordinates system coordinates.
# i.e. give it 150/370 and receive 2/5 or alike.
def fromCcsCoord(ccs, xItem,yItem):
    numberXItems = ccs.xMax - ccs.xMin
    numberYItems = ccs.yMax - ccs.yMin
    
    # attention: in python, if you first divide and then multiplicate,
    # the following calculations always result in 0.
    x =    numberXItems * xItem / ccs.width
    y = - (numberYItems * yItem / ccs.height)
    
    return QPointF(x,y)
    

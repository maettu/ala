#!/usr/bin/python

from PyQt4.QtCore import (QPointF)


# Translates cartesian coordinates (from own coord. system)
# to item coordinates
# i.e. give it x = 2, y = 5 and receive 150,370 or something alike.
def toCcsCoord(ccs, x, y, self = None, parent = None):
    # first, children of other elements need to get 
    # coordinates relative to their parent
    if self and parent:
        p = subtractParentCoordinates(self, parent, ccs)
        x = p.x()
        y = p.y()
    
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
def fromCcsCoord(ccs, xItem,yItem, self = None, parent = None):
    

    numberXItems = ccs.xMax - ccs.xMin
    numberYItems = ccs.yMax - ccs.yMin
    
    # attention: in python, if you first divide and then multiply,
    # the following calculations always result to 0.
    x =    numberXItems * xItem / ccs.width
    y = - (numberYItems * yItem / ccs.height)
    
    #~ print x, y
    
    if self and parent:
        p = addParentCoordinates(x,y,self,parent,ccs)
        x = p.x()
        y = p.y()
        #~ print "..."
        #~ print x,y
    
    return QPointF(x,y)
    
# subtracts parents' coordinates so that item is positioned according
# to ccs instead of parent.
def subtractParentCoordinates(self, parent, ccs):
    if parent != ccs:
        x = self.x - parent.x
        y = self.y - parent.y
        return QPointF(x,y)
    else:
        return QPointF(self.x, self.y)

        
def addParentCoordinates(x,y,self, parent, ccs):
    if parent != ccs:
        x = x + parent.x
        y = y + parent.y
        return QPointF(x,y)
    else:
        return QPointF(x, y)
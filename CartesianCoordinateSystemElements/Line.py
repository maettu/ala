#!/usr/bin/python

from PyQt4.QtCore import (Qt, QLineF, QRectF, QPointF)
from PyQt4.QtGui import (QGraphicsItem, QColor)

import Helper.CoordinateSystemTransformation as CST

class Line(QGraphicsItem):
    """Defines a line by two points. If points are moved, line follows these movements."""
    
    def __init__(self, startPoint, endPoint, ccs):
        super(Line, self).__init__(startPoint)
        
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.ccs = ccs
        
        # before painting widget coordinates need to be calculated
        p = CST.toCcsCoord(ccs, self.endPoint.x,self.endPoint.y)
        self.Rect = QRectF(QPointF(0,0), p)
        
        self.color = QColor(255,0,0)
        
        self.rot = 100
        
    def boundingRect(self):
        return self.Rect

        
        
    def paint(self, painter, option, widget=None):        
        painter.setPen(QColor("orange"))
        
        # as soon as dependent points are *not relative* to parent points any more,
        # this needs to be changed.

        ep = CST.toCcsCoord(self.ccs, self.endPoint.x, self.endPoint.y)
        
        painter.drawLine(QLineF(0, 0, ep.x(), ep.y() ))
#!/usr/bin/python

from PyQt4.QtCore import (Qt, QLineF, QRectF)
from PyQt4.QtGui import (QGraphicsItem, QColor)

class Line(QGraphicsItem):
    """Defines a line by two points. If points are moved, line follows these movements."""
    
    def __init__(self, startPoint, endPoint, coordinateSystem):
        super(Line, self).__init__(startPoint)
        
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.coordinateSystem = coordinateSystem
        
        self.Rect = QRectF(0,0,self.endPoint.x,self.endPoint.y)
        
        self.color = QColor(255,0,0)
        
        self.rot = 100
        
    def boundingRect(self):
        return self.Rect

        
        
    def paint(self, painter, option, widget=None):        
        painter.setPen(QColor("orange"))
        
        # as soon as dependent points are *not relative* to parent points any more,
        # this needs to be changed.
        painter.drawLine(QLineF(
                            0               +   self.startPoint.size/2, 
                            0               +   self.startPoint.size/2, 
                            
                            self.endPoint.x +   self.endPoint.size/2, 
                            self.endPoint.y +   self.endPoint.size/2
        ))
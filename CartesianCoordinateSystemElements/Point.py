#!/usr/bin/python

from PyQt4.QtCore import (Qt, QRectF, QPointF)
from PyQt4.QtGui import (QGraphicsItem, QColor, QBrush)

import Helper.CoordinateSystemTransformation as CST

class Point(QGraphicsItem):
    """Defines a movable point."""
    
    def __init__(self, ccs, parent, x, y, size, red=0, green=255, blue=0):
        super(Point, self).__init__(parent)
        
        # does not really work for children of other points
        # every time it is moved, it jumps back to 0/0 of its parent. (?!)
        #~ self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        
        self.Rect = QRectF(-size/2, -size/2, size, size)
        
        self.color = QColor(red, green, blue)
        self.parent = parent
        
        # x and y are in own cartesian coordinate system.
        self.x = x
        self.y = y
        
        self.size = size
        
        # we need coordinates relative to ccs, while chilren of other
        # points get coordinates relative to their parent.
        self.__calculateCoordinates(parent, ccs)
        
        # coordinates go through conversion when item is placed or painted.
        self.setPos(CST.toCcsCoord(ccs, self.x,self.y))
        
        self.ccs = ccs
        
        self.leftMouseButtonPressed = None
    
    # calculates coordinates so that item is positioned according
    # to ccs instead of parent.
    # To ensure quasi indefinite sub children this is made recursive
    def __calculateCoordinates(self, parent, ccs):
        if parent != ccs:
            self.x = self.x - parent.x
            self.y = self.y - parent.y
            self.__calculateCoordinates(parent.parent, ccs)
            
        
    def boundingRect(self):
        return self.Rect
        
    def paint(self, painter, option, widget=None):
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.color))
        painter.drawEllipse(self.Rect)
        
    # point moves on left click
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            # save where in item the mouse was clicked
            self.xOnWidget = e.pos().x()
            self.yOnWidget = e.pos().y()
            self.leftMouseButtonPressed = 1
            
    def mouseMoveEvent(self, e):
        
        if self.leftMouseButtonPressed:
        
            # these calculations are in widget coordinates.
            x_move = e.pos().x() - self.xOnWidget
            y_move = e.pos().y() - self.yOnWidget
            
            p = CST.toCcsCoord(self.ccs, self.x, self.y)
            
            x = p.x() + x_move
            y = p.y() + y_move
            
            self.setPos(QPointF(x, y))
            
            # self.x and self.y need to be adjusted, too.
            p = CST.fromCcsCoord(self.ccs, x,y)
            self.x = p.x()
            self.y = p.y()
            
            # if a points moves, the whole coordinate system is updated.
            # I will have to investigate how terrible the performance penalty is.
            self.ccs.update()
        
    def mouseReleaseEvent(self, e):
        self.leftMouseButtonPressed = None
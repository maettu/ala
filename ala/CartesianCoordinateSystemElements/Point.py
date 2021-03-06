#!/usr/bin/python

from PyQt4.QtCore import (Qt, QRectF, QPointF)
from PyQt4.QtGui import (QGraphicsItem, QColor, QBrush)

import ala.Helper.CoordinateSystemTransformation as CST

class Point(QGraphicsItem):
    """Defines a movable point."""
    
    def __init__(self, ccs, parent, x, y, size, red=0, green=255, blue=0):
        super(Point, self).__init__(parent)
               
        self.Rect = QRectF(-size/2, -size/2, size, size)
        
        self.color = QColor(red, green, blue)
        self.parent = parent
        
        # x and y are in cartesian coordinate system.
        self.x = x
        self.y = y
        
        self.ccs  = ccs
        self.size = size
        
        # coordinates go through conversion when item is placed or painted.
        self.setPos(CST.toCcsCoord(self.ccs, self.x,self.y, self, parent))
       
        self.leftMouseButtonPressed = None
        
        # All children of this point. These get updated when point
        # moves
        self.children = []
        
        # point is draggable by default. If you need a non-draggable
        # point, unset by callin set_draggable( False )
        self.draggable = True
        
        self.visible        = True

    def addChildPoint(self, child):
        self.children.append(child)

    def removeChildPoint(self, child):
        # TODO
        pass
        
    def boundingRect(self):
        return self.Rect

    def calculatePosition(self, e):
        """Calculates its position after a move. Can easily
        overwritten by subclasses to get different behaviour"""

        # these calculations are in widget coordinates.
        x_move = e.pos().x() - self.xOnWidget
        y_move = e.pos().y() - self.yOnWidget
            
        p = CST.toCcsCoord( self.ccs, self.x, self.y, self, self.parent )
           
        x = p.x() + x_move
        y = p.y() + y_move
           
        self.setPos(QPointF(x, y))
           
        # self.x and self.y need to be adjusted, too.
        p = CST.fromCcsCoord( self.ccs, x,y, self, self.parent )
        self.x = p.x()
        self.y = p.y()
        
    def paint(self, painter, option, widget=None):
        if self.visible == True:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(self.color))
            painter.drawEllipse(self.Rect)
        
    def mousePressEvent(self, e):
        # point moves on left click
        if e.button() == Qt.LeftButton:
            # save where in item the mouse was clicked
            self.xOnWidget = e.pos().x()
            self.yOnWidget = e.pos().y()
            self.leftMouseButtonPressed = 1
            
    def mouseMoveEvent(self, e):
        if self.leftMouseButtonPressed and self.draggable:
            x = self.x
            y = self.y
            self.calculatePosition(e)
            xDelta = self.x -x
            yDelta = self.y -y
            
            #upadate functionally dependent children
            self.updateChildren( xDelta, yDelta )

            # if a points moves, the whole coordinate system is updated.
            self.ccs.update()
        
    def mouseReleaseEvent(self, e):
        self.leftMouseButtonPressed = None
        
    def set_draggable( self, value ):
        self.draggable = value

    def set_x(self, x):
        xDelta = x - self.x
        self.x = x
        self.setPosition()
        #~ self.updateChildren( xDelta, 0 )

    def set_y(self, y):
        self.y = y
        self.setPosition()
        
    def setPosition( self, x = False, y = False ):
        if x == False and y == False:
            self.setPos ( CST.toCcsCoord(
                self.ccs, self.x, self.y )
            )
        else:
            self.setPos( CST.toCcsCoord(
                self.ccs, x, y )
            )
        
    def setVisible( self, value ):
        self.visible = value
        
    def updateChildren( self, xDelta, yDelta ):
        for child in self.children:
            child.updateYourself(xDelta, yDelta)


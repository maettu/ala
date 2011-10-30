#!/usr/bin/python

from PyQt4.QtCore import ( Qt, QLineF, QRectF, QPointF, QString )
from PyQt4.QtGui  import ( QGraphicsRectItem, QColor, QBrush )

import ala.Helper.CoordinateSystemTransformation as CST

class Rectangle( QGraphicsRectItem ):
    """Defines a rectangle by two points. If points are moved, rectangle follows these movements."""
    
    def __init__( self, startPoint, endPoint, ccs, color = 'blue', fillColor = 'lightBlue' ):
        super( Rectangle, self ).__init__( ccs )
        
        self.startPoint     = startPoint
        self.endPoint       = endPoint
        self.ccs            = ccs
        self.color          = color
        self.fillColor      = fillColor
        
        self.visible        = True

        
        self.Rect = QRectF( self.startPoint, self.endPoint )

    def boundingRect( self ):
        return self.Rect

    def paint( self, painter, option, widget=None ):
        
        if self.visible == True:
            painter.setPen( QColor( self.color ) )
            painter.setBrush( QColor( self.fillColor ) )

            self.sp = CST.toCcsCoord( self.ccs, self.startPoint.x(), self.startPoint.y() )
            self.ep = CST.toCcsCoord( self.ccs, self.endPoint.x(), self.endPoint.y() )
            
            self.Rect = QRectF( self.sp, self.ep )
            
            painter.drawRect( self.Rect )
    
    def setPosition( self, startPoint, endPoint ):
        self.startPoint = startPoint
        self.endPoint   = endPoint
                
    def setVisible( self, value ):
        self.visible = value
        
    def setColor( self, color ):
        self.color = color
        
    def setFillColor( self, fillColor ):
        self.fillColor = fillColor
        
    def updateYourself( self ):
        # There is no action needed, as a line gets its information
        # from startPoint and endPoint
        # Just adjust self.Rect to avoid case where line disappears mysteriously and after then,
        # paint() is never called again
        self.Rect = QRectF( self.startPoint.x(), self.startPoint.y(), self.endPoint.x(), self.endPoint.y() )





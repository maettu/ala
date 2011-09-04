#!/usr/bin/python

from PyQt4.QtCore import ( Qt, QLineF, QRectF, QPointF )
from PyQt4.QtGui  import ( QGraphicsLineItem, QColor )

import Helper.CoordinateSystemTransformation as CST

class Line( QGraphicsLineItem ):
    """Defines a line by two points. If points are moved, line follows these movements."""
    
    def __init__( self, startPoint, endPoint, ccs ):
        super( Line, self ).__init__( startPoint )
        
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.ccs = ccs
        
        self.Rect = QRectF( -ccs.width, -ccs.height, ccs.width*2,
                            ccs.height*2 )

    def boundingRect( self ):
        return self.Rect

    def paint( self, painter, option, widget=None ):
        painter.setPen( QColor( "orange" ) )

        sp = CST.toCcsCoord( self.ccs, self.startPoint.x, self.startPoint.y )
        ep = CST.toCcsCoord( self.ccs, self.endPoint.x, self.endPoint.y )
        
        painter.drawLine( QLineF(0, 0, ep.x()-sp.x(), ep.y()-sp.y() ) )

    def updateYourself( self, xDelta, yDelta ):
        ep = CST.toCcsCoord( self.ccs, self.endPoint.x, self.endPoint.y )
        
        # need to change Rect to force repaint?!
        self.setRect = QRectF( QPointF(0,0), ep )



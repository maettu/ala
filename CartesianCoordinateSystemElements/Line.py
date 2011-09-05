#!/usr/bin/python

from PyQt4.QtCore import ( Qt, QLineF, QRectF, QPointF, QString )
from PyQt4.QtGui  import ( QGraphicsLineItem, QColor )

import ala.Helper.CoordinateSystemTransformation as CST

class Line( QGraphicsLineItem ):
    """Defines a line by two points. If points are moved, line follows these movements."""
    
    def __init__( self, startPoint, endPoint, ccs, paintToBorder = False, showIncline = False, color = 'orange' ):
        super( Line, self ).__init__( ccs )
        
        self.startPoint     = startPoint
        self.endPoint       = endPoint
        self.ccs            = ccs
        self.paintToBorder  = paintToBorder
        self.showIncline    = showIncline
        self.color          = color
        
        self.Rect = QRectF(startPoint.x, startPoint.y, endPoint.x, endPoint.y )

    def boundingRect( self ):
        return self.Rect

    def paint( self, painter, option, widget=None ):
        painter.setPen( QColor( self.color ) )

        sp = CST.toCcsCoord( self.ccs, self.startPoint.x, self.startPoint.y )
        ep = CST.toCcsCoord( self.ccs, self.endPoint.x, self.endPoint.y )
        
        self.Rect = QRectF( sp, ep )
        
        line = QLineF( sp, ep )
        painter.drawLine( line )
        
        if self.paintToBorder == True:
            if line.length() > 2:
                # paint line to approximately the edge of the ccs.
                ep2 = line.pointAt( self.ccs.width / line.length() )
                painter.drawLine(ep,ep2)
                sp2 = line.pointAt(-self.ccs.width / line.length() )
                painter.drawLine(sp,sp2)
        
        if self.showIncline == True:
            if line.length() > 2:
                incline = ( self.endPoint.y - self.startPoint.y ) / ( self.endPoint.x - self.startPoint.x )
                # print text limited to 2 decimal digits.
                painter.drawText( ep.x() + 10, ep.y() + 10, QString ( '%.2f' %(incline) ) )
        
    def updateYourself( self, xDelta, yDelta ):
        # There is no action needed, as a line gets its information
        # from startPoint and endPoint
        pass




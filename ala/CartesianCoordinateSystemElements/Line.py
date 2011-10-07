#!/usr/bin/python

from PyQt4.QtCore import ( Qt, QLineF, QRectF, QPointF, QString )
from PyQt4.QtGui  import ( QGraphicsLineItem, QColor, QBrush )

import ala.Helper.CoordinateSystemTransformation as CST

class Line( QGraphicsLineItem ):
    """Defines a line by two points. If points are moved, line follows these movements."""
    
    def __init__( self, startPoint, endPoint, ccs, paintToBorder = False, showIncline = False, color = 'orange', minLength = 0 ):
        super( Line, self ).__init__( ccs )
        
        self.startPoint     = startPoint
        self.endPoint       = endPoint
        self.ccs            = ccs
        self.paintToBorder  = paintToBorder
        self.showIncline    = showIncline
        self.color          = color
        
        self.visible        = True
        
        self.minLength      =  minLength # pixel
        
        self.Rect = QRectF(self.startPoint.x, self.startPoint.y, self.endPoint.x, self.endPoint.y )

    def boundingRect( self ):
        return self.Rect

    def paint( self, painter, option, widget=None ):
        if self.visible == True:
            painter.setPen( QColor( self.color ) )

            self.sp = CST.toCcsCoord( self.ccs, self.startPoint.x, self.startPoint.y )
            self.ep = CST.toCcsCoord( self.ccs, self.endPoint.x, self.endPoint.y )
            
            self.Rect = QRectF( self.sp, self.ep )
            self.line = QLineF( self.sp, self.ep )
            
            if self.line.length() > self.minLength:
                
                painter.drawLine( self.line )
            
                if self.paintToBorder == True:

                    # paint line to approximately the edge of the ccs.
                    ep2 = self.line.pointAt( self.ccs.width / self.line.length() )
                    painter.drawLine(self.ep,ep2)
                    sp2 = self.line.pointAt(-self.ccs.width / self.line.length() )
                    painter.drawLine(self.sp,sp2)
            
                if self.showIncline == True:
                    incline = ( self.endPoint.y - self.startPoint.y ) / ( self.endPoint.x - self.startPoint.x )
                    # print text limited to 2 decimal digits.
                    painter.setBackground ( QBrush ( QColor( 'lightGrey' ) ) )
                    painter.setBackgroundMode (Qt.BGMode(1))
                    painter.setPen( QColor( 'black' ) )
                    #~ painter.drawText( self.ep.x() + 10, self.ep.y() + 10, QString ( '%.2f' %(incline) ) )
                
    def setVisible( self, value ):
        self.visible = value
        
    def updateYourself( self, xDelta, yDelta ):
        # There is no action needed, as a line gets its information
        # from startPoint and endPoint
        # Just adjust self.Rect to avoid case where line disappears mysteriously and after then,
        # paint() is never called again
        self.Rect = QRectF( self.startPoint.x, self.startPoint.y, self.endPoint.x, self.endPoint.y )





#!/usr/bin/python

from PyQt4.QtCore import ( Qt, QLineF, QRectF, QPointF )
from PyQt4.QtGui  import ( QGraphicsLineItem, QColor )

import Helper.CoordinateSystemTransformation as CST

class Line( QGraphicsLineItem ):
    """Defines a line by two points. If points are moved, line follows these movements."""
    
    def __init__( self, startPoint, endPoint, ccs ):
        #~ super( Line, self ).__init__( startPoint )
        super( Line, self ).__init__( ccs )
        
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.ccs = ccs
        
        #~ self.Rect = QRectF( -ccs.width, -ccs.height, ccs.width*2,
                            #~ ccs.height*2 )
        self.Rect = QRectF(startPoint.x, startPoint.y, endPoint.x, endPoint.y )
        

    def boundingRect( self ):
        return self.Rect

    def paint( self, painter, option, widget=None ):
        painter.setPen( QColor( "orange" ) )

        sp = CST.toCcsCoord( self.ccs, self.startPoint.x, self.startPoint.y )
        ep = CST.toCcsCoord( self.ccs, self.endPoint.x, self.endPoint.y )
        
        self.Rect = QRectF( sp, ep )
        
        #~ line = QLineF(0, 0, ep.x()-sp.x(), ep.y()-sp.y() )
        line = QLineF( sp, ep )
        painter.drawLine( line )
        
        #~ painter.setPen( QColor( 'black' ) )
      
        #~ painter.drawRect( self.Rect )
        
        #~ ep2 = line.pointAt ( 5)
        #~ painter.drawLine (ep.x()-sp.x(), ep.y()-sp.y(), ep2.x()-sp.x(), ep2.y()-sp.y() )
        
        if (line.dx() != 0): # prevent div by 0
            steigung = ( self.endPoint.y - self.startPoint.y ) / ( self.endPoint.x - self.startPoint.x )
            print "Steigung, selbst berechnet: ", steigung

    def updateYourself( self, xDelta, yDelta ):
        # There is no action needed, as a line gets its information
        # from startPoint and endPoint
        pass




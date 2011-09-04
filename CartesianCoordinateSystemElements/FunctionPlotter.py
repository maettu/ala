#!/usr/bin/python

from PyQt4.QtCore import (Qt, QLineF, QRectF, QPointF)
from PyQt4.QtGui import (QGraphicsLineItem, QColor)

import Helper.CoordinateSystemTransformation as CST

class FunctionPlotter( QGraphicsLineItem ):
    """Plots a function"""
    
    def __init__( self, ccs, function ):
        super( FunctionPlotter, self ).__init__()
        
        self.ccs = ccs
        #~ self.Rect = QRectF( -ccs.width/2, -ccs.height/2 , ccs.width, ccs.height)
        self.Rect = QRectF( 0,0, 100,100)
        
        print "init"
        
        self.setPos(QPointF(ccs.xAxis, ccs.yAxis))
        
        
    def boundingRect(self):
        return self.Rect
        
    def paint(self, painter, option, widget=None):
        print "juhuu"
        color = QPen(QColor(0, 100, 0))
        
        painter.drawRect( self.Rect )
        
        for i in range (ccs.xMin, css.xMax+1):
            print i
        
    
        
        




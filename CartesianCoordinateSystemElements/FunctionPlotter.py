#!/usr/bin/python

from PyQt4.QtCore import (Qt, QLineF, QRectF, QPointF)
from PyQt4.QtGui import (QGraphicsLineItem, QColor, QPen)

import Helper.CoordinateSystemTransformation as CST

class FunctionPlotter( QGraphicsLineItem ):
    """Plots a function"""
    
    def __init__( self, ccs, function ):
        super( FunctionPlotter, self ).__init__()
        
        self.ccs = ccs
        #~ self.Rect = QRectF( -ccs.width/2, -ccs.height/2 , ccs.width, ccs.height)
        self.Rect = QRectF( -100,-110, 100,100)
        
        self.setPos(QPointF(self.ccs.xAxis, self.ccs.yAxis))
        self.function = function
        
        self.alreadyPainted = 0
        
        
    def boundingRect(self):
        return self.Rect
        
    def paint(self, painter, option, widget=None):
        #~ print "repaint function ?!"
        #~ if self.alreadyPainted == 1:
            #~ return
            
        color = QPen(QColor(0, 100, 0))
        
        sp = CST.toCcsCoord( self.ccs, self.ccs.xMin, self.ccs.yMin)
        
        for xRaw in range ( self.ccs.xMin, self.ccs.xMax+1 ):
            for tiny in range ( 0 , 10 ):
                
                # I'm sorry, but I find this stupid for a high level language
                x = float(tiny) / 10 + xRaw
                                
                ep = CST.toCcsCoord( self.ccs, x, eval( self.function ) )
                painter.drawLine( QLineF(sp, ep ) )
                sp = ep
                
        self.alreadyPainted = 1
        
    def plot( self ):
        print "weehooo"
       
        
        




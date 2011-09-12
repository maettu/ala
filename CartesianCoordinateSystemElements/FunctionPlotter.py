#!/usr/bin/python

from PyQt4.QtCore import (Qt, QLineF, QRectF, QPointF)
from PyQt4.QtGui import (QGraphicsItem, QColor, QPen)

import ala.Helper.CoordinateSystemTransformation as CST

class FunctionPlotter( QGraphicsItem ):
    """Plots a function"""
    
    def __init__( self, ccs, function ):
        super( FunctionPlotter, self ).__init__(ccs)
        
        self.ccs = ccs
        self.Rect = QRectF( -ccs.width/2, -ccs.height/2 , ccs.width, ccs.height)
        
        self.setPos(QPointF(self.ccs.xAxis, self.ccs.yAxis))
        self.function = function
        
        self.alreadyPainted = 0
        
        
    def boundingRect(self):
        return self.Rect
        
    def paint(self, painter, option, widget=None):
            
        color = QPen(QColor(0, 100, 0))
        
        # x must be set, because function will most probably contain it.
        x = self.ccs.xMin
        try:
            sp = CST.toCcsCoord( self.ccs, x, eval( self.function ) )
        except:
            # silence errors like "raise negative number to fractional power"
            pass
        
        # ep needs to be set to prevent from
        # "assigned from before instantiated below"
        ep = None
        
        for xRaw in range ( self.ccs.xMin, self.ccs.xMax+1 ):
            for tiny in range ( 0 , 10 ):
                
                # don't forget to cast into float!
                x = float(tiny) / 10 + xRaw
                
                # try to set ep, which might fail due tu "raise to fractional power asf.
                try:                
                    ep = CST.toCcsCoord( self.ccs, x, eval( self.function ) )
                    if sp.y() != ep.y():
                        painter.drawLine( QLineF(sp, ep ) )
                    
                except:
                    pass
                
                sp = ep
                
        self.alreadyPainted = 1
        
    def redefine( self, function ):
        self.function = function
        self.setPos(QPointF(self.ccs.xAxis, self.ccs.yAxis))
        self.update()
        




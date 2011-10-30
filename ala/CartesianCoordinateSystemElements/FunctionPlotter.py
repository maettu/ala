#!/usr/bin/python

import math

from PyQt4.QtCore import (Qt, QLineF, QRectF, QPointF)
from PyQt4.QtGui import (QGraphicsItem, QColor, QPen)

import ala.Helper.CoordinateSystemTransformation as CST

class FunctionPlotter( QGraphicsItem ):
    """Plots a function"""
    
    def __init__( self, ccs, function ):
        super( FunctionPlotter, self ).__init__(ccs)
        
        self.ccs = ccs
        
        self.function = function
        
        self.Rect = QRectF( -self.ccs.width/2, -self.ccs.height/2 , self.ccs.width, self.ccs.height)
        self.setPos(QPointF(self.ccs.xAxis, self.ccs.yAxis))

    def boundingRect(self):
        return self.Rect
        
    def paint(self, painter, option, widget=None):
        
        self.Rect = QRectF( -self.ccs.width/2, -self.ccs.height/2 , self.ccs.width, self.ccs.height)
        
        self.setPos(QPointF(self.ccs.xAxis, self.ccs.yAxis))
            
        color = QPen(QColor(0, 100, 0))
        
        # x must be set, because function will most probably contain it.
        x = self.ccs.xMin
        try:
            sp = CST.toCcsCoord( self.ccs, x, eval( self.function ) )
        except:
            # silence errors like "raise negative number to fractional power"
            pass
        
        # ep needs to be set to prevent from
        # "assigned from before instantiated" below
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
                
    def getYMin( self, xMin, xMax, xStep, maxStep = 1000):
        ### return minimal y value in range xMin, xMax. xStep defines exactness. ###
        if xStep == 0:
            raise Exception( "xStep must not be 0" )
            
        if xMin > xMax:
            xMin, xMax = xMax, xMin
        if xStep < 0:
            xStep = xStep * -1
            
        x = xMin
        yMin = self._y( x )
        
        i = 0
        while x < xMax:
            y = self._y( x )
            
            if y < yMin:
                yMin = y
                
            # avoid "infinite" loop
            if i == maxStep:
                return yMin
            i+= 1
                
            x = x + xStep
    
        return yMin
        
    def getYMax( self, xMin, xMax, xStep, maxStep = 1000):
        ### return maximal x value in range xMin, xMax. xStep defines exactness. ###
        if xStep == 0:
            raise Exception( "xStep must not be 0" )
            
        if xMin > xMax:
            xMin, xMax = xMax, xMin
        if xStep < 0:
            xStep = xStep * -1
            
        x = xMin
        yMax = self._y( x )
        
        i = 0
        while x < xMax:
            y = self._y( x )
            
            if y > yMax:
                yMax = y
                
            # avoid "infinite" loop
            if i == maxStep:
                return yMax
            i+=1
                
            x = x + xStep
    
        return yMax
        
    def _y( self, x ):
        try:
            y = eval( self.function )
        except:
            y = False
            
        return y
         
        
    def redefine( self, function ):
        self.function = function
        self.setPos(QPointF(self.ccs.xAxis, self.ccs.yAxis))
        self.update()
        




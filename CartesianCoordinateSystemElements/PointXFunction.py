#!/usr/bin/python

from Point import Point
import Helper.CoordinateSystemTransformation as CST

class PointXFunction( Point ):
    """Defines a movable point with an y which is functionally
    dependent on its x value."""

    # TODO function as a parameter
    def __init__( self, ccs, parent, x, y, size, red=200, green=0,
                    blue=0, function = 'x**2' ):
        super(PointXFunction, self).__init__(ccs,
            parent, x, y, size, red, green, blue)

        self.function = function
        
        # silently overwrite y so that the point instantly is on the
        # function specified. 
        #self.y = self.x * eval( function )
        self.setPosition()

    def calculatePosition( self, e ):
        # only needs x_move here as y is calculated dependently on x
        x_move = e.pos().x() - self.xOnWidget

        p = CST.toCcsCoord( self.ccs, self.x, self.y, self,
                            self.parent )
        x = p.x() + x_move

        p = CST.fromCcsCoord( self.ccs, x, 0, self, self.parent )
        self.x = p.x()
        self.setPosition()

    def setPosition( self ):
        x = self.x
        self.y = eval(self.function)
        self.setPos ( CST.toCcsCoord(
            self.ccs, self.x, self.y )
        )

    def updateYourself( self, xDelta, yDelta ):
        # point moves relative to parent.
        self.x = self.x + xDelta
        self.setPosition()
       
